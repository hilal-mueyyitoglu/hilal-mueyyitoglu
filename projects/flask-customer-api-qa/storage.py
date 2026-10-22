"""CSV persistence and validation for an educational demo (not production storage)."""
from pathlib import Path
import pandas as pd

COLUMNS = ["customer_id", "product_id", "product_type", "rating"]


class ValidationError(ValueError):
    pass


def validate_customer(payload):
    if not isinstance(payload, dict):
        raise ValidationError("JSON object required")
    missing = [field for field in COLUMNS if field not in payload]
    if missing:
        raise ValidationError("Missing required fields: " + ", ".join(missing))
    try:
        customer_id = int(payload["customer_id"])
        product_id = int(payload["product_id"])
        rating = int(payload["rating"])
    except (TypeError, ValueError, OverflowError):
        raise ValidationError("customer_id, product_id and rating must be integers")
    if any(isinstance(payload[k], bool) for k in ("customer_id", "product_id", "rating")):
        raise ValidationError("Boolean values are not valid integer IDs or ratings")
    for k, n in (("customer_id", customer_id), ("product_id", product_id), ("rating", rating)):
        if str(payload[k]).strip() != str(n):
            raise ValidationError(f"{k} must be a whole number")
    if customer_id <= 0 or product_id <= 0:
        raise ValidationError("IDs must be positive")
    if not 1 <= rating <= 10:
        raise ValidationError("rating must be between 1 and 10")
    kind = payload["product_type"]
    if not isinstance(kind, str) or not kind.strip():
        raise ValidationError("product_type must be a nonempty string")
    return {"customer_id": customer_id, "product_id": product_id, "product_type": kind.strip(), "rating": rating}


def load_data(csv_path):
    path = Path(csv_path)
    if not path.exists():
        return pd.DataFrame(columns=COLUMNS)
    return pd.read_csv(path, dtype={"customer_id": int, "product_id": int, "product_type": str, "rating": int})


def find_customer(csv_path, customer_id):
    if not isinstance(customer_id, int) or customer_id <= 0:
        raise ValidationError("customer_id must be a positive integer")
    df = load_data(csv_path)
    return df[df["customer_id"] == customer_id].to_dict(orient="records")


def upsert_customer(csv_path, payload):
    row = validate_customer(payload)
    df = load_data(csv_path)
    matches = (df["customer_id"] == row["customer_id"]) & (df["product_id"] == row["product_id"])
    updated = bool(matches.any())
    if updated:
        df.loc[matches, "product_type"] = row["product_type"]
        df.loc[matches, "rating"] = row["rating"]
    else:
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    path = Path(csv_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    return row, updated
