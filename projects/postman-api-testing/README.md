# Postman API Testing Portfolio

## Project Overview

This project demonstrates hands-on API testing using Postman and JavaScript assertions.

The objective is to validate HTTP responses, verify JSON data, and explore API behavior with different input values.

## Tools and Technologies

- Postman
- JavaScript
- REST API
- JSON
- Postman Echo API
- GitHub

## Test Scenarios

| Test ID | HTTP Method | Test Scenario | Result |
|---|---|---|---|
| TC-01 | GET | Verify HTTP 200 status code | PASS |
| TC-02 | GET | Validate response URL | PASS |
| TC-03 | POST | Verify successful POST response | PASS |
| TC-04 | POST | Validate returned JSON data | PASS |
| TC-05 | POST | Verify invalid input is echoed correctly | PASS |

## Test Execution Summary

- Total API Requests: 3
- Total Automated Tests: 5
- Passed: 5
- Failed: 0

All five assertions passed during execution in Postman.

## Testing Techniques

- Positive Testing
- Invalid Input Testing
- HTTP Status Code Validation
- Response Body Validation
- JavaScript Assertions

**Note:** Postman Echo reflects submitted data without enforcing application-specific validation rules. The invalid-input scenario verifies echo behavior, not rejection of invalid data.

## How to Run

1. Install Postman.
2. Import the Postman Collection JSON file.
3. Open the collection.
4. Run the GET and POST requests.
5. Review the results in the Test Results section.

## Learning Outcomes

Through this project, I practiced creating API requests, validating HTTP response codes, writing JavaScript assertions, verifying JSON responses, and documenting test execution results.

This project is part of my ongoing transition from manufacturing quality assurance to software quality assurance.
