from flask import Flask, render_template
from flask_cors import CORS

# models
from models.db import db

# routes
from routes.dataport_bp import dataport_bp
from routes.manage_device_bp import manage_device_bp
from routes.people_counting_bp import people_counting_bp

# config
from configs import config

# init worker
from controllers import worker_controller

# create application
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.SQLALCHEMY_TRACK_MODIFICATIONS
app.config['SECRET_KEY'] = config.SECRET_KEY


# Basic Auth
app.config['BASIC_AUTH_USERNAME'] = config.BASIC_AUTH_USERNAME
app.config['BASIC_AUTH_PASSWORD'] = config.BASIC_AUTH_PASSWORD
app.config['BASIC_AUTH_FORCE'] = config.BASIC_AUTH_FORCE

# init database
db.app = app
db.init_app(app)

# register routes
app.register_blueprint(dataport_bp, url_prefix='/')
app.register_blueprint(manage_device_bp, url_prefix='/manage_device')
app.register_blueprint(people_counting_bp, url_prefix='/people_counting')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    import logging
    logging.basicConfig(filename='logs.log', level=logging.DEBUG)

    db.create_all()
    worker_controller.init()
    # app.debug = config.DEBUG
    # app.debug = True
    # app.run(host="192.168.1.2", port=5000)
    app.run(host="0.0.0.0", port=5000, debug=True)
    # app.run(host="0.0.0.0", debug=True)
