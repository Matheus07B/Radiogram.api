from flask import Blueprint, jsonify

connection_blueprint = Blueprint('/connection', __name__)

@connection_blueprint.route('', methods=['GET'])
def connection_status():
    return jsonify({"Status": "Active"}), 200