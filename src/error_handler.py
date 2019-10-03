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
        rv['message'] = self.message
        return rv
        
def create_app():
    app = Flask(__name__)
    app.config.from_object('config.BaseConfiguration')
    app.secret_key = app.config.get('SECRET_KEY')
    app.register_blueprint(main.bp)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    return app        
