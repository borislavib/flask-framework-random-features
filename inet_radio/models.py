import flask_admin
from flask_admin.contrib import sqla

from flask_admin.contrib import fileadmin

from flask_admin import helpers as admin_helpers

from flask_admin import BaseView, expose

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required, current_user

from flask_security.utils import encrypt_password



from datetime import datetime

app = Flask(__name__)
app.config.from_pyfile('config.py')


db = SQLAlchemy(app)



# Define models for many-to-many
roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

# Roles 
class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name

# Create User table
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    share_favourites = db.Column(db.Integer, server_default="1") # , nullable=False
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    def __str__(self):
        return self.email


# Create model for the Favourites table 
class Favourites(db.Model):
    __tablename__ = 'favourites'
    id = db.Column(db.Integer(), primary_key=True)
    song_name = db.Column(db.String(255))
    pub_date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('Favourites', lazy='dynamic'))

    def __init__(self, song_name, pub_date=None, user_id=None):
        self.song_name = song_name
        if pub_date is None:
            self.pub_date = datetime.utcnow()
        self.user_id = user_id



# Create customized model view class
class UserModelView(sqla.ModelView):
    column_exclude_list = ('password', 'confirmed_at')
    column_exclude_list = ('password', 'confirmed_at', 'user_id')

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('superuser'):
            return True

        return False

    def _handle_view(self, name, **kwargs):

        #Override builtin _handle_view in order to redirect users when a view is not accessible.
        if not self.is_accessible():
            #if current_user.is_authenticated:
            if current_user.is_authenticated and current_user.is_active:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))



#file_path = os.path.join(os.path.dirname(__file__), 'static/music')


# Administrative views
class FileView(fileadmin.FileAdmin):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('superuser'):
            return True

        return False

    def _handle_view(self, name, **kwargs):

        #Override builtin _handle_view in order to redirect users when a view is not accessible.
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))

    # Pass additional parameters to 'path' to FileUploadField constructor
    form_args = {
        'path': {
            'label': 'File'
        }
    }


user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)




#Populate examples in database
def build_sample_db():
    import string
    import random

    db.drop_all()
    db.create_all()

    with app.app_context():
        user_role = Role(name='user')
        super_user_role = Role(name='superuser')
        db.session.add(user_role)
        db.session.add(super_user_role)
        db.session.commit()

        # Default admin
        test_user = user_datastore.create_user(
            first_name=app.config['USERNAME'],
            email=app.config['EMAIL_TEST'],
            password=encrypt_password(app.config['PASSWORD']),
            share_favourites=0,
            active=1,
            roles=[user_role, super_user_role]
        )

        first_names = [
            'Petar', 'Peter', 'Yana', 'Kalina', 'Evgeni', 'Evstati', 'Vladimir', 'Panko'
        ]
        last_names = [
            'Ivanov', 'Petrov', 'Ivanova', 'Ivanova', 'Pekov', 'Evstatiev', 'Ivanilov', 'Takov'
        ]

        for i in range(len(first_names)):
            tmp_email = first_names[i].lower() + "." + last_names[i].lower() + "@batko.com"
            tmp_pass = ''.join(random.choice(string.ascii_lowercase + string.digits) for i in range(10))
            user_datastore.create_user(
                first_name=first_names[i],
                last_name=last_names[i],
                email=tmp_email,
                share_favourites=1,
                password=encrypt_password(tmp_pass),
                roles=[user_role, ]
            )
        user_datastore.create_user(
            first_name='Panko',
            last_name='Ivanov',
            email='panko',
            share_favourites=1,
            password=encrypt_password('panko'),
            roles=[user_role, ]
        )
        db.session.commit()
    return


