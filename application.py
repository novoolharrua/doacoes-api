# from flask import Flask, jsonify, request, abort, make_response, url_for
# from flask_cors import CORS
#
# from endpoints.status import blueprint as status_bp
# from endpoints.regions import blueprint as regions_bp
# from endpoints.events import blueprint as events_bp
# from endpoints.institutions import blueprint as institutions_bp
# from endpoints.infos import blueprint as infos_bp
#
# app = Flask(__name__)
# CORS(app)
#
#
# ####################################################################
# # Main
# ####################################################################
#
# if __name__ == "__main__":
#     app.register_blueprint(status_bp)
#     app.register_blueprint(regions_bp)
#     app.register_blueprint(events_bp)
#     app.register_blueprint(institutions_bp)
#     app.register_blueprint(infos_bp)
#     app.run(debug=False, port=8080, host='0.0.0.0', use_reloader=False)


from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"