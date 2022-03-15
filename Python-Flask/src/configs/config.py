from base64 import b64encode
import os

SECRET_KEY = os.urandom(32)
# print(int.from_bytes(SECRET_KEY, "big"))

random_bytes = os.urandom(64)
token = b64encode(random_bytes).decode('utf-8')

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database
SQLALCHEMY_DATABASE_URI = 'sqlite:///database.sqlite3'

# Turn off the Flask-SQLAlchemy event system and warning
SQLALCHEMY_TRACK_MODIFICATIONS = False


# Basic Auth
BASIC_AUTH_USERNAME = "admin"
BASIC_AUTH_PASSWORD = "public"
BASIC_AUTH_FORCE = True

# Camera People Counting
X_ACCRESS_TOKENS = [
    "Hr+nDkzo9rj9mm7oPtErLa0Ge/FLnrYhEBh0ZPFq6mIsblUt6/o2bO4Qvzm19HdN991qggwbNVq7fiqy76FwOw=="
]

openHour = 8
openMinute = 00
closeHour = 20
closeMinute = 00

# clear data
hour_interval = "00"    # every midnight

strapiServer = "https://0857-58-136-2-49.ngrok.io/"
current_counting_api = strapiServer + "occupations"
occupation_history_api = strapiServer + "occupation-histories"