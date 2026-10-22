import tempfile
import unittest
from pathlib import Path
from storage import ValidationError, find_customer, load_data, upsert_customer


class CustomerStoreTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / "customers.csv"
        self.valid = {"customer_id": 101, "product_id": 500, "product_type": "shirt", "rating": 10}

    def tearDown(self):
        self.tmp.cleanup()

    def test_create_and_persist(self):
        row, updated = upsert_customer(self.path, self.valid)
        self.assertFalse(updated)
        self.assertEqual(row["rating"], 10)
        self.assertEqual(len(find_customer(self.path, 101)), 1)

    def test_update_without_duplicate(self):
        upsert_customer(self.path, self.valid)
        _, updated = upsert_customer(self.path, dict(self.valid, rating=3))
        self.assertTrue(updated)
        self.assertEqual(len(load_data(self.path)), 1)
        self.assertEqual(find_customer(self.path, 101)[0]["rating"], 3)

    def test_same_customer_different_product_is_new_row(self):
        upsert_customer(self.path, self.valid)
        upsert_customer(self.path, dict(self.valid, product_id=501))
        self.assertEqual(len(find_customer(self.path, 101)), 2)

    def test_rating_boundaries(self):
        for bad in [0, 11, -1, 100]:
            with self.subTest(rating=bad), self.assertRaises(ValidationError):
                upsert_customer(self.path, dict(self.valid, rating=bad))
        for allowed in [1, 10]:
            upsert_customer(self.path, dict(self.valid, rating=allowed))
            self.assertEqual(find_customer(self.path, 101)[0]["rating"], allowed)

    def test_missing_field_and_wrong_type(self):
        with self.assertRaises(ValidationError):
            upsert_customer(self.path, {"customer_id": 101})
        for invalid in ["abc", 2.5, True]:
            with self.subTest(value=invalid), self.assertRaises(ValidationError):
                upsert_customer(self.path, dict(self.valid, rating=invalid))

    def test_unknown_customer(self):
        self.assertEqual(find_customer(self.path, 999), [])


if __name__ == "__main__":
    unittest.main()
