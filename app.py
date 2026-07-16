from flask import Flask, request, jsonify
from api import get_product_by_barcode
from models import db, InventoryItem

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/items', methods=['POST'])
def add_item():
    data = request.get_json()
    barcode = data.get('barcode')
    product = get_product_by_barcode(barcode)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    new_item = InventoryItem(
        name=product.get('name'),
        barcode=product.get('barcode'),
        description=product.get('description'),
        brand=product.get('brand'),
        image=product.get('image')
    )
    db.session.add(new_item)
    db.session.commit()
    return jsonify({"message": "Item added"}), 201

@app.route('/items', methods=['GET'])
def get_items():
    barcode = request.args.get('barcode')
    if not barcode:
        return jsonify({"error": "please provide a barcode"}), 400
    product = get_product_by_barcode(barcode)
    if product:
        return jsonify(product)
    else:
        return jsonify({"error": "Product not found"}), 404
    
   
    
@app.route('/items/<int:id>', methods=['PUT'])
def update_item(id):
    item = InventoryItem.query.get_or_404(id)
    data = request.get_json()
    item.quantity = data.get('quantity', item.quantity)
    db.session.commit()
    return jsonify({"message": "Item updated"})

@app.route('/items/<int:id>', methods=['DELETE'])
def delete_item(id):
    item = InventoryItem.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Item deleted"})

@app.route('/items', methods=['GET'])
def get_all_items():
     items = InventoryItem.query.all()
     return jsonify([item.to_dict() for item in InventoryItem.query.all()])



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)