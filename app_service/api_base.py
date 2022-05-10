from flask import request
from flask import jsonify
from flask import make_response
from app_service.app import app


# Welcome API
@app.route("/")
def helloworld():
    return "Welcome"