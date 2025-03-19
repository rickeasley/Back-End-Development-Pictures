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
    # verifying there is data to search
    if data:
        return jsonify(data), 200
    # if no data, returning 404 status code
    return {"message": "Data not found"}, 404

######################################################################
# GET A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    # making sure data is there to query
    if data:
        # searching to see if the id is present in the data
        for picture in data:
            if int(picture['id']) == id:
                return jsonify(picture), 200
    # id was not found, sending 404 status code
    return jsonify({"error": "ID not found"}), 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    # getting the json data sent through POST
    req_data = request.get_json()

    # making sure data is present
    if not req_data:
        return jsonify({"error": "Missing required data"}), 400

    # Check if ID already exists
    for pic in data:
        if pic['id'] == req_data['id']:
            return jsonify({"Message": f"picture with id {req_data['id']} already present"}), 302

    try:
        # Add to data dictionary
        data.append(req_data)
    except NameError:
        return jsonify({"effor": "unexpected error"}), 500
    
    #successfully added
    return jsonify(req_data), 201


######################################################################
# UPDATE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    update_data = request.get_json()
    if not update_data:
        return jsonify({"error": "Invalid data sent."}), 400

    for picture in data:
        if picture['id'] == id:
            picture.update(update_data)
            return jsonify({"message": f"Picture wiht id {id} successfully updated"}), 200
    
    return jsonify({"message": "picture not found"}), 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    if not id:
        return jsonify({"error": "Invalid input"}), 400

    for picture in data:
        if picture['id'] == id:
            del data[id]
            return '', 204

    return jsonify({"message": "picture not found"}), 404

