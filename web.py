import sys, os
import logging
import time
C = os.path.abspath(os.path.dirname(__file__))

logging.basicConfig(filename=os.path.join(C, "run_server.log"), level=logging.INFO, format="%(asctime)s -- %(name)s -- %(levelname)s -- %(message)s")

from pyaccess_server import app

sys.path.append(C)
from pyaccess_server import views
app.register_blueprint(views)

from cheroot.wsgi import Server as WSGIServer, PathInfoDispatcher

d = PathInfoDispatcher({'/': app})
server = WSGIServer(('0.0.0.0', 5000), d)

if __name__ == '__main__':
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()