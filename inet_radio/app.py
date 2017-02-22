#!/usr/bin/env python

import os

from sqlite3 import dbapi2 as sqlite3

# Flask 
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

# Database, ORM
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func


# Security 
from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required, current_user

from flask_security.utils import encrypt_password


# Admin related 
import flask_admin
from flask_admin.contrib import sqla

from flask_admin.contrib import fileadmin

from flask_admin import helpers as admin_helpers

from flask_admin import BaseView, expose


# flask-socketio
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect

# Donwload file
from youtubedl import ytdl, validate_url

from datetime import datetime

###
# Define models

from models import User, Role, Favourites, roles_users , UserModelView, \
        FileView, build_sample_db

###
# forms
from forms import EditForm

###
# Main instance of the app
app = Flask(__name__)

# Set up config
app.config.from_pyfile('config.py')

# DB
db = SQLAlchemy(app)

# Chat 
async_mode = None
socketio = SocketIO(app, async_mode=async_mode)
thread = None

###



# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


###



# Create admin
admin = flask_admin.Admin(
    app,
    #'Example: Auth',
    'Admin and registration',
    base_template='my_master.html',
    template_mode='bootstrap3',
)


###

# Set up admin 
#file_path = os.path.join(os.path.dirname(__file__), 'static/music')
path = os.path.join(os.path.dirname(__file__), 'static/music')
# Add model views
admin.add_view(UserModelView(Role, db.session))
admin.add_view(UserModelView(User, db.session))
#admin.add_view(FileView(path, '/home/bo/python/main/inet_radio/static/music', name='Files'))
admin.add_view(FileView(path, app.config['DOWNLOAD_FILES'], name='Files'))





###

# define a context processor for merging flask-admin's template context into the
# flask-security views.
@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template='my_master.html', #admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
        get_url=url_for
    )


###

# Add/delete favourite song 0
@app.route('/favourites', methods = ['GET', 'POST'])
@login_required
def favourites():
    the_songs = Favourites.query.filter(Favourites.user_id == current_user.get_id()).all()

    if request.method == 'POST':
        if request.form['action'] == 'Add':
            if not request.form['name_song'] or len(request.form['name_song']) > 255:
                flash('Please add author and name of song between 0 and 255 characters. ', 'error')
            else:
                song = Favourites(request.form['name_song'], None, current_user.get_id() )

                db.session.add(song)
                db.session.commit()
                flash('Record was successfully added')
                return redirect(url_for('index'))
        if request.form['action'] == 'Del':
            if request.form['id_song'] and request.form['id_song'].isdigit:
                song_id = request.form['id_song']
                res = Favourites.query.filter_by(id=song_id).delete(synchronize_session='fetch')

                if res == 0:
                    flash('No such song.')
                else:
                    flash('Record was deleted. ')

                db.session.commit()
                return redirect(url_for('index'))
    return render_template('favourites.html',  songs = the_songs, title='Favourites' )


# Download image from freesound.org

@app.route('/download', methods = ['GET', 'POST'])
@login_required
def download():
   
    if request.method == 'POST':
        if not request.form['name']:
            flash('Please enter URL in the field', 'error')
        elif not validate_url(request.form['name']):
            flash('Please enter freesound.org web')
        else:
            result = ytdl(request.form['name'])
            if result:
                flash("Successfully downloaded.")

                #with open(logfile, "a") as log:
                with open(app.config['DOWNLOAD_LOG'], "a") as log:
                    log.write("\n")
                    log.write(current_user.email)
                    log.write("\t" + request.form['name'])
                return redirect(url_for('music'))
            else:
                flash("Error downloading. Try again", 'error')
    return render_template('download.html', title='Download')

# 
@app.route('/rating')
def rating():
    fav_songs_ = db.session.query(
             Favourites.song_name,
             func.count(Favourites.song_name).label('count')
    ).group_by(Favourites.song_name).order_by(func.count(Favourites.song_name).desc()).all()
    return render_template('rating.html', fav_songs= fav_songs_,title='Rating')



# Check user and eventually favourites 
@app.route('/user/<int:id>')
def user(id):

    usrs = db.session.query(
             User.first_name,
             User.last_name,
             User.email,
             User.share_favourites
    ).filter_by(id = id).all()

    favs = db.session.query(
            Favourites.song_name,
            Favourites.pub_date
    ).filter_by(user_id = id).all()

    return render_template('user.html', users= usrs, favourites=favs, title='User')


#Check all favourites 
@app.route('/users')
def users():
    usrs = db.session.query(
             User.id,
             User.first_name,
             User.last_name,
             User.email,
             User.share_favourites
    ).all()

    return render_template('users.html', users= usrs, title='Users')



# Edit user profile
@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    form = EditForm()

    form.email.data = current_user.email
    form.first_name.data = current_user.first_name
    form.last_name.data = current_user.last_name
    form.share_favourites.data = current_user.share_favourites

    if request.method == 'POST':
        if len(request.form['first_name']) < 255 and len(request.form['last_name']) < 255:

            usr = User.query.filter_by(id = current_user.get_id()).first()
            usr.first_name = request.form['first_name']
            usr.last_name = request.form['last_name']

            if 'share_favourites' in request.form:
                usr.share_favourites = 1
            else:
                usr.share_favourites = 0

            db.session.add(usr)
            db.session.commit()

            flash('Your changes have been saved.')
            #
            return redirect(url_for('users'))
        else:
            flash('Please, fill the form correctly: up to 255 characters for each field.')
    return render_template('edit.html', form=form)


# Listen to sound 
@app.route('/music', methods = ['GET'])
def music():
    #music_dir = '/home/borislav/python/main/inet_radio/static/music'
    music_dir = app.config['DOWNLOAD_FILES']
    music_files = [f for f in os.listdir(music_dir) if f.endswith('mp3')]
    return render_template("music.html", songs=music_files)

# Main page
@app.route('/')
def index():
    return render_template('index.html',title='Main')


###
# Error handling 

@app.errorhandler(404)
def page_not_found(error):
    return 'This page does not exist. Please, check again.<br/>', 404


@app.errorhandler(500)
def server_error(error):
    return 'Server error', 500

###

# Chat page
@app.route('/chat')
@login_required
def chat():
    global thread
    if thread is None:
        thread = socketio.start_background_task(target=background_thread)
    return render_template('chat.html', async_mode=socketio.async_mode, title='Chat')


def background_thread():
    #Example of how to send server generated events to clients.
    count = 0
    while True:
        socketio.sleep(10)
        count += 1




def len_150(message):
    if len(message) > 150:
        message = message[:150]
    return message


@socketio.on('msg event', namespace='/test')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1

    if current_user.is_authenticated:
        emit('my response',
                {'data': '{0}: {1}'.format(current_user.email, message['data']),
                   'count': session['receive_count']},
                    broadcast=True)
    else:
        emit('my response',
                {'data': message['data'], 'count': session['receive_count']})


# Send to all in chat 
@socketio.on('broadcast event', namespace='/test')
def test_broadcast_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    message['data'] = len_150(message['data'])

    if current_user.is_authenticated:
        emit('my response',
                {'data': '{0}: {1}'.format(current_user.email, message['data']),
                   'count': session['receive_count']},
                    broadcast=True)
    else:
        emit('my response',
                {'data': message['data'], 'count': session['receive_count']},
                broadcast=True)


@socketio.on('join', namespace='/test')
def join(message):
    join_room(message['room'])

    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': session['receive_count']})


@socketio.on('leave', namespace='/test')
def leave(message):

    leave_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': session['receive_count']})

# Send message in a room 
@socketio.on('room event', namespace='/test')
def send_room_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    message['data'] = len_150(message['data'])

    emit('my response',
            {'data': '{0} : Room<{1}> : {2}'.format(current_user.email, message['room'], message['data']),
                   'count': session['receive_count']},
        room=message['room'])

@socketio.on('disconnect request', namespace='/test')
def disconnect_request():
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': 'Disconnected!', 'count': session['receive_count']})
    disconnect()


@socketio.on('my ping', namespace='/test')
def ping_pong():
    emit('my pong')


@socketio.on('connect', namespace='/test')
def test_connect():
    emit('my response', {'data': 'Connected', 'count': 0})


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected', request.sid)


###

if __name__ == '__main__':
    # Build a sample db on the fly, if one does not exist yet.
    app_dir = os.path.realpath(os.path.dirname(__file__))
    database_path = os.path.join(app_dir, app.config['DATABASE_FILE'])
    if not os.path.exists(database_path):
        build_sample_db()

    socketio.run(app,
                debug=True,
                host="0.0.0.0",
                use_reloader=True,
                port=5000)
