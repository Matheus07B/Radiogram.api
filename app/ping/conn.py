from flask import Blueprint, jsonify

from . import connection_blueprint

@connection_blueprint.route('/conn', methods=['GET'])
def connection_status():
    return jsonify({"Status": "Active"}), 200
