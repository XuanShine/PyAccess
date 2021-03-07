import sys, os, time
C = os.path.abspath(os.path.dirname(__file__))
import requests
import socket

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

######################################
#### Application Factory Function ####
######################################

def create_app(config_filename=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///history.db"
    db.init_app(app)

    return app

import schedule

# init all
init_GPIO = schedule.every().hour.do(lock_door.init_GPIO).tag("init")
init_GPIO.run()
init_lamp = schedule.every().hour.do(lock_door.init_lamp).tag("init")
init_lamp.run()
schedule.clear("init")