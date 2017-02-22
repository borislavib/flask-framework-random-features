# Create dummy secrey key so we can use sessions
SECRET_KEY = '123456790'
#DEBUG=False

DATABASE_FILE = 'file_inet_radio.sqlite'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_FILE
SQLALCHEMY_ECHO = True

DATABASE='db_inet_radio.db'

# Default user admin 
USERNAME='admin'
PASSWORD='admin'
EMAIL_TEST='admin'

# Flask-Security config
#SECURITY_URL_PREFIX = "/admin"
SECURITY_PASSWORD_HASH = "pbkdf2_sha512"
SECURITY_PASSWORD_SALT = "ATGUOHAELKiubahiughaerGOJAEGj"

# Flask-Security URLs, overridden because they don't put a / at the end
SECURITY_LOGIN_URL = "/login/"
SECURITY_LOGOUT_URL = "/logout/"
SECURITY_REGISTER_URL = "/register/"
#
SECURITY_POST_LOGIN_VIEW = "/admin/"
SECURITY_POST_LOGOUT_VIEW = "/admin/"
SECURITY_POST_REGISTER_VIEW = "/admin/"

# Flask-Security features
SECURITY_REGISTERABLE = True
SECURITY_SEND_REGISTER_EMAIL = False

# Download log
DOWNLOAD_LOG='/home/bo/python/inet_radio/static/music/downloaded/log_downloaded.txt'

# Download files
DOWNLOAD_FILES='/home/b/python/_upload/main/inet_radio/static/music'


