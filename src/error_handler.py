from flask import jsonify


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv["message"] = self.message
        return rv


from multiprocessing.connection import Listener
from array import array

address = ("localhost", 6000)

with Listener(address, authkey=b"secret password") as listener:
    with listener.accept() as conn:
        print("connection accepted from", listener.last_accepted)

        conn.send([2.25, None, "junk", float])

        conn.send_bytes(b"hello")

        conn.send_bytes(array("i", [42, 1729]))


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.BaseConfiguration")
    app.secret_key = app.config.get("SECRET_KEY")
    app.register_blueprint(main.bp)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html"), 404

    return app
