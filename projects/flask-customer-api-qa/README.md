# Customer Data API — Postman, Flask & CSV QA Practice

**Independent learning portfolio implementation**, created after completing Postman/API testing coursework. This is a new demonstration project, not a copy of a completed Coursera lab and not commercial experience.

## Purpose
Show a QA approach to a tiny API: clarify data rules, design positive and negative test cases, write assertions, validate CSV persistence and detect duplicate records.

**Architecture:** `Postman → Flask endpoints → pandas validation/persistence → customers.csv → JSON response`

## API contract

| Method | Endpoint | Expected behavior |
|---|---|---|
| GET | `/customers/<customer_id>` | 200 + records; 404 if not found |
| POST | `/add_customer` | 201 for new customer-product pair; 200 for update |
| POST | `/add_customer` | 400 for invalid data; 415 if request is not JSON |

Example request body:

```json
{"customer_id":101,"product_id":500,"product_type":"shirt","rating":10}
```

The demo uses **(customer_id, product_id)** as its record identity and validates ratings as **1–10**. The course notes inconsistently specify **0–10** elsewhere; see [Test Cases](TEST_CASES.md) for the QA clarification.

## Run locally

Requires Python 3.10+:

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Server URL: `http://127.0.0.1:5000`. Import the [Postman collection](postman/Customer_API.postman_collection.json) and run requests in numbered order against a **fresh** local `customers.csv`. The first POST gives 201; repeated identical keys update and return 200.

To run the Python unit tests:

```bash
python -m unittest discover -s tests -v
```

## Portfolio contents

- [QA test scenarios and verification status](TEST_CASES.md)
- [Postman collection with HTTP assertions](postman/Customer_API.postman_collection.json)
- [Flask HTTP API](app.py)
- [pandas storage and validation](storage.py)
- [Python tests](tests/test_storage.py)

**Verified on 22 October 2026:** six Python storage test methods passed locally. **Not yet verified:** Flask HTTP execution and the Postman/Newman collection against the server. The included Postman assertions are designed checks, not claimed passing evidence.

## Scope and limitations

This is educational code, not a production system. CSV updates are not concurrency-safe, no authentication is implemented and no real customer data should be used. Testing and documenting assumptions are the focus. My eight years of quality assurance experience come from electronics manufacturing; this software QA project is independent learning work.

[GitHub profile](https://github.com/hilal-mueyyitoglu) · [LinkedIn](https://www.linkedin.com/in/hilal-mueyyitoglu/)
