from flask import Flask, request, jsonify
import requests
from models import db, InventoryItem

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

def get_product_by_barcode(barcode):
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 1:
                product = data.get('product', {})
                return {
                    "barcode": barcode,
                    "name": product.get('product_name', 'Unknown'),
                    "brand": product.get('brands', 'Unknown'),
                    "description": product.get('generic_name', ''),
                    "image": product.get('image_url', '')
                }
    except requests.RequestException:
        return None

    return None

@app.route('/items', methods=['GET'])
def get_items():
    items = InventoryItem.query.all()
    return jsonify([item.to_dict() for item in items])

@app.route('/items/search', methods=['GET'])
def search_item():
    barcode = request.args.get('barcode')
    if not barcode:
        return jsonify({"error": "Barcode is required"}), 400
    
    product = get_product_by_barcode(barcode)
    if product:
        return jsonify(product)
    return jsonify({"error": "Product not found"}), 404


@app.route('/items', methods=['POST'])
def add_item():
    data = request.json
    barcode = data.get('barcode')
    quantity = data.get('quantity', 1)
    
    if not barcode:
        return jsonify({"error": "Barcode is required"}), 400
    
    existing = InventoryItem.query.filter_by(barcode=barcode).first()
    if existing:
        existing.quantity += quantity  # Add to stock
        db.session.commit()
        return jsonify({
            "status": "updated", 
            "message": f"Quantity now {existing.quantity}", 
            "data": existing.to_dict()
        }), 200
    
    product = get_product_by_barcode(barcode)
    if not product:
        return jsonify({"error": "Product not found in OpenFoodFacts"}), 404
    
    new_item = InventoryItem(
        barcode=product['barcode'],
        name=product['name'],
        brand=product['brand'],
        description=product['description'],
        image=product['image'],
        quantity=quantity
    )
    db.session.add(new_item)
    db.session.commit()
    
    return jsonify({
        "status": "success", 
        "message": "New item added", 
        "data": new_item.to_dict()
    }), 201

@app.route('/items/<int:id>', methods=['PUT'])
def update_item(id):
    data = request.json
    item = InventoryItem.query.get(id)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    
    item.quantity = data.get('quantity', item.quantity) 
    db.session.commit()
    return jsonify({"status": "success", "message": "Quantity updated", "data": item.to_dict()}), 200


@app.route('/items/<int:id>', methods=['DELETE'])
def delete_item(id):
    item = InventoryItem.query.get(id)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    
    db.session.delete(item)
    db.session.commit()
    return jsonify({"status": "success", "message": "Item deleted"}), 200


if __name__ == '__main__':
    app.run(debug=True, port=5001)