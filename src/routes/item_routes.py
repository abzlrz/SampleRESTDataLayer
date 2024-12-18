from flask import Blueprint, request
from controller.item_controller import add_item_controller, update_item_controller

item_routes = Blueprint('item_routes', __name__)

@item_routes.route('/item', methods=['POST'])
def add_item():
    return add_item_controller(request.json)

@item_routes.route('/item/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    return update_item_controller(item_id, request.json)
