# Python Inventory System

A simple Flask-based inventory management application that stores products in a SQLite database and enriches them with product information from OpenFoodFacts using a barcode.

## Features

- View all inventory items
- Search product details by barcode
- Add a new item or increase quantity
- Update item quantity
- Delete an item

## Project Structure

- app.py - Flask routes and barcode lookup logic
- models.py - SQLAlchemy model for inventory items
- requirements.txt - Python dependencies
- instance/ - SQLite database folder


## API Endpoints

### Get all items
curl http://127.0.0.1:5000/items

### Search product by barcode
curl "http://127.0.0.1:5000/items/search?barcode=3017620422003"

### Add or update an item
curl -X POST http://127.0.0.1:5000/items \
  -H "Content-Type: application/json" \
  -d '{"barcode":"3017620422003","quantity":3}'

### Update quantity
curl -X PUT http://127.0.0.1:5000/items/1 \
  -H "Content-Type: application/json" \
  -d '{"quantity":5}'

### Delete an item

curl -X DELETE http://127.0.0.1:5001/items/1

