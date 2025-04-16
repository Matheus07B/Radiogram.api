from flask import Blueprint, jsonify

helloworld_blueprint = Blueprint('/helloworld', __name__)

@helloworld_blueprint.route('', methods=['GET'])
def helloworld_fun():
    return jsonify({"Messages": "Hello world"}), 200