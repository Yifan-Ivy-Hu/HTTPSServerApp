"""kvpair development configuration. source of this file: https://eecs485staff.github.io/p2-insta485-serverside/setup_flask.html"""

import pathlib

# Root of this application, useful if it doesn't occupy an entire domain
APPLICATION_ROOT = '/'

# Secret key for encrypting cookies
SECRET_KEY = b'\xf4\xc82\xd9\xe7+\xf7BA\x92\x8aM>\xc7\x87\xeeQ@\x9d\xd9\t\x824b'
SESSION_COOKIE_NAME = 'login'

# File Upload to fileupload/uploads/
KVPAIR_ROOT = pathlib.Path(__file__).resolve().parent.parent
UPLOAD_FOLDER = KVPAIR_ROOT/'var'/'uploads'
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

# Database file is var/kvpair.sqlite3
DATABASE_FILENAME = KVPAIR_ROOT/'var'/'kvpair.sqlite3'
