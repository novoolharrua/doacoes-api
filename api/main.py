from flask import Flask, jsonify, request, abort, make_response, url_for
from flask_cors import CORS

from endpoints.status import blueprint as status_bp
from endpoints.regions import blueprint as regions_bp

app = Flask(__name__)
CORS(app)


####################################################################
# Main
####################################################################

if __name__ == "__main__":
    app.register_blueprint(status_bp)
    app.register_blueprint(regions_bp)
    app.run(debug=False, port=8080, host='0.0.0.0', use_reloader=False)