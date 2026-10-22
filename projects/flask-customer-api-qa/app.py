"""Educational Flask API. Not production-ready."""
import os
from pathlib import Path
from flask import Flask, jsonify, request
from storage import ValidationError, find_customer, upsert_customer


def create_app(csv_path=None):
    app = Flask(__name__)
    data_file = Path(csv_path or os.environ.get("CUSTOMER_CSV_PATH", Path(__file__).parent / "customers.csv"))

    @app.get("/customers/<int:customer_id>")
    def get_customer(customer_id):
        try:
            rows = find_customer(data_file, customer_id)
        except ValidationError as exc:
            return jsonify(error=str(exc)), 400
        if not rows:
            return jsonify(error="Customer not found"), 404
        return jsonify(customer_id=customer_id, records=rows), 200

    @app.post("/add_customer")
    def add_customer():
        if not request.is_json:
            return jsonify(error="Content-Type must be application/json"), 415
        try:
            row, updated = upsert_customer(data_file, request.get_json(silent=True))
        except ValidationError as exc:
            return jsonify(error=str(exc)), 400
        return jsonify(action="updated" if updated else "created", customer=row), 200 if updated else 201

    return app


if __name__ == "__main__":
    create_app().run(debug=False, port=5000)
