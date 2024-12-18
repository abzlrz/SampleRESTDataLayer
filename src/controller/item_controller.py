from models.item_model import Item
from flask import jsonify

def add_item_controller(request_data):
    try:
        name = request_data.get('name')
        description = request_data.get('description')
        location = request_data.get('location')
        ppu = request_data.get('ppu')
        uom = request_data.get('uom')
        status = "active"
        
        if not name or not description or not location or not ppu or not uom:
            return jsonify({"error": "Missing required fields"}), 400
        
        new_item = Item.add_item(name, description, location, ppu, uom, status)

        return jsonify(
            {
                "name": new_item.name,
                "description": new_item.location,
                "ppu": new_item.ppu,
                "uom": new_item.uom,
                "status": new_item.status
            }
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def update_item_controller(request_data):
    try:
        name = request_data.get('name')
        description = request_data.get('description')
        location = request_data.get('location')
        ppu = request_data.get('ppu')
        uom = request_data.get('uom')

        update_item = Item.update_item(name, description, location, ppu, uom)

        return jsonify(
            {
                "name": update_item.name,
                "description": update_item.location,
                "ppu": update_item.ppu,
                "uom": update_item.uom
            }
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500