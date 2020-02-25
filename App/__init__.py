from flask import Flask
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO

from App.ext import init_socket
from App.views import init_route


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret!'
    # async_mode = None
    Bootstrap(app)
    # load the router by lazying
    init_route(app)

    socketio = SocketIO(app)
    init_socket(socketio)

    # app.register_blueprint(blue)

    return app, socketio