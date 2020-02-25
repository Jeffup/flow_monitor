from flask import Flask
# from flask-bootstrap import *
from flask_script import Manager

from App import create_app

app, socketio = create_app()

# manager =  Manager(app = app)

if __name__ == '__main__':
    # manager.run()
    socketio.run(app)