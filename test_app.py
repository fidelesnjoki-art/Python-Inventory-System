import unittest

from app import InventoryItem, create_app, db


class InventorySearchTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app(
            {
                "TESTING": True,
                "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            }
        )
        self.client = self.app.test_client()

        with self.app.app_context():
            item = InventoryItem(
                name="Coke Zero",
                barcode="1234567890123",
                description="Sugar-free soda",
                brand="Coca-Cola",
                quantity=5,
                image="",
            )
            db.session.add(item)
            db.session.commit()

    def test_search_by_name_is_case_insensitive(self):
        response = self.client.get("/items/search-name?name=coke")

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(any(item["name"] == "Coke Zero" for item in data))

    def test_search_by_barcode_returns_saved_item(self):
        response = self.client.get("/items/search-barcode?barcode=1234567890123")

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["barcode"], "1234567890123")


if __name__ == "__main__":
    unittest.main()
