from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    if data:
        return jsonify(data), 200
    
    return {"message": "Data not found"}, 404

######################################################################
# GET A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    if data:
        for picture in data:
            if int(picture['id']) == id:
                return jsonify(picture), 200
    
    return jsonify({"error": "ID not found"}), 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["POST"])
def create_picture():
    if id in data:
        return jsonify({"Message": f"picture with id {picture['id']} already exists"}), 302
    
    new_pic = request.get_json()
    if not new_pic:
        return jsonify({"error": "Invalid or missing JSON data"}), 400

    try:
        data.append(new_pic)
    except NameError:
        return {"error": "Data not defined"}, 500
    
    return {"message": f"{new_pic['id']} successfully created"}, 200


######################################################################
# UPDATE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    pass

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    pass
