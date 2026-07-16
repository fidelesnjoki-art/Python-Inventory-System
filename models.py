from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class InventoryItem(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    name =db.Column(db.String(100), nullable = False)
    barcode = db.Column(db.String(50), unique = True)
    description = db.Column(db.String(200))
    brand = db.Column(db.String(100))
    image = db.Column(db.String(200))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "barcode": self.barcode,
            "description": self.description,
            "brand": self.brand,
            "image": self.image
        }
