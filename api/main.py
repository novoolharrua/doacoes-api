from flask import Flask, jsonify, request, abort, make_response
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


####################################################################
# Main
####################################################################

if __name__ == "__main__":

    app.run(debug=False, port=8080, host='0.0.0.0', use_reloader=False)