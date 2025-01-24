from flask import Blueprint, jsonify

connection_blueprint = Blueprint('/connection', __name__)

@connection_blueprint.route('', methods=['GET'])
def connection_status():
    return jsonify({"Status": "Active"}), 200

@connection_blueprint.route('/v2', methods=['GET'])
def connection_status_v2():
    return jsonify({"Status": "v2 active"}), 200