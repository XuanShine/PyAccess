from datetime import datetime

from bottle import run, template, Bottle, Response, route
from bottle import jinja2_view

import lock_door

pyaccess = Bottle()


@pyaccess.route("/help")
def help():
    return """
    "/"
    "/get_state/<relai_ch>" 
    "/turn/<state>/<relai_ch>
    """


@pyaccess.route("/get_state/<relai_ch>")
def get_state(relai_ch):
    return


@pyaccess.route("/")
@jinja2_view("index.html")
def index():
    list_relais = {
        1: "porte entrée (allumé = vérouillée, éteint = dévérouillée)",
        2: "lumières enseignes",
        3: "lumières out-receptions (30s pour s’éteindre)",
        4: "lumières porches (extérieur)",
        5: "lumières in-reception",
        6: "lumières banque",
        7: "lumières salle petit-déj buffet",
        8: "lumières salle petit-déj tables",
    }
    state_relais = {relai: lock_door.is_on(relai) for relai in list_relais.keys()}
    return {"list_relais":list_relais, "state_relais":state_relais}


@pyaccess.route("/turn/<state>/<relai_ch>")
def turn(state, relai_ch):
    lock_door.turn(state, int(relai_ch))
    resp = Response(f"{datetime.now().strftime('%H:%M:%S')} {relai_ch} : {state}")
    resp.set_header('Access-Control-Allow-Origin', '*')
    return resp

lock_door.init_GPIO()

from cheroot.wsgi import Server as WSGIServer, PathInfoDispatcher
d = PathInfoDispatcher({"/": pyaccess})
server = WSGIServer(("0.0.0.0", 8080), d)

if __name__ == "__main__":
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()

