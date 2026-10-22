# Customer CSV API — test design

| ID | Operation | Input / condition | Expected result |
|---|---|---|---|
| API-01 | POST create | Customer 101 / product 500 / rating 10 | 201, `created`; CSV row persisted |
| API-02 | GET existing | Customer 101 | 200 with records |
| API-03 | POST update | Same customer and product, rating 3 | 200, `updated`; one matching row |
| API-04 | POST out of range | Rating 11 | 400 and no CSV modification |
| API-05 | POST boundaries | Rating 1 and rating 10 | Values accepted |
| API-06 | POST invalid boundary | Rating 0 | 400 per this demo's specification |
| API-07 | POST missing field | Missing product ID | 400, descriptive error |
| API-08 | POST invalid type | `rating: "abc"` | 400, descriptive error |
| API-09 | GET not found | Customer 999999 | 404, error message |
| API-10 | POST duplicate key | Existing customer + product | Update, not duplicate |
| API-11 | POST different product | Existing customer + new product | Insert; existing row unchanged |

## QA findings from requirements review

1. Training notes alternated between rating **1–10** and **0–10**. This demo specifies **1–10**, but a real requirements owner must settle this conflict before production testing.
2. Training examples once treated age as a unique ID; age is not a stable customer identifier. This demo uses explicit `customer_id`.

## Results and evidence integrity

- **Executed:** 6 Python `unittest` storage tests locally, **6 passed**, 22 Oct 2026.
- **Not executed here:** Flask runtime, Postman HTTP collection, Newman or CI workflow.
- Important unverified risks: CSV concurrent writes, malformed JSON, filesystem errors and handling of personal data.

The collection's test scripts specify expected results and must not be represented as completed Postman runs.
