# Udatracker — Order Management System

A minimal Order Tracking REST API built with Flask, developed using
strict Test-Driven Development (TDD).

## Project Structure
```
.
├── backend
│   ├── __init__.py
│   ├── app.py
│   ├── in_memory_storage.py
│   ├── order_tracker.py
│   ├── requirements.txt
│   └── tests
│       ├── __init__.py
│       ├── test_api.py
│       └── test_order_tracker.py
├── frontend
│   ├── css
│   │   └── style.css
│   ├── index.html
│   └── js
│       └── script.js
├── pytest.ini
└── README.md
```

## Setup
```bash
# Clone repository
git clone https://github.com/udacity/cd14599-project-starter
cd cd14599-project-starter/starter

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt
```

## Dependencies
```
black==26.3.1
blinker==1.9.0
click==8.3.1
coverage==7.13.5
flake8==7.3.0
flask==3.1.2
iniconfig==2.3.0
itsdangerous==2.2.0
jinja2==3.1.6
markupsafe==3.0.3
mccabe==0.7.0
mypy-extensions==1.1.0
packaging==26.0
pathspec==1.0.4
platformdirs==4.9.4
pluggy==1.6.0
pycodestyle==2.14.0
pyflakes==3.4.0
pygments==2.20.0
pytest==8.4.1
pytest-cov==7.1.0
pytest-flake8==1.3.0
pytokens==0.4.1
werkzeug==3.1.7
```

## Code Style

This project uses [Black](https://black.readthedocs.io/) for automatic
code formatting and [flake8](https://flake8.pycqa.org/) for PEP8
compliance checks.
```bash
# Format code automatically
black backend/

# Check PEP8 (runs automatically with pytest via pytest-flake8)
flake8 backend/
```

## Running Tests
```bash
# All tests (unit + integration + flake8 + coverage)
pytest

# Unit tests only
pytest backend/tests/test_order_tracker.py

# Integration tests only
pytest backend/tests/test_api.py
```

## Running the Application
```bash
python -m backend.app
```

Open `http://127.0.0.1:5000` in your browser.

## API Reference

### Add Order
```bash
curl -X POST http://127.0.0.1:5000/api/orders \
  -H "Content-Type: application/json" \
  -d '{"order_id": "ORD001", "item_name": "Laptop", "quantity": 1, "customer_id": "CUST001"}'
```

### Get Order by ID
```bash
curl http://127.0.0.1:5000/api/orders/ORD001
```

### Update Order Status
```bash
curl -X PUT http://127.0.0.1:5000/api/orders/ORD001/status \
  -H "Content-Type: application/json" \
  -d '{"new_status": "shipped"}'
```

### List All Orders
```bash
curl http://127.0.0.1:5000/api/orders
```

### Filter Orders by Status
```bash
curl http://127.0.0.1:5000/api/orders?status=pending
```

Valid status values: `pending`, `processing`, `shipped`,
`delivered`, `cancelled`

## Reflection

- **Design decision:** `OrderTracker` is fully decoupled from Flask —
  it only knows about storage, not HTTP. This made unit testing trivial
  with mock storage and kept the API layer thin.

- **Testing insight:** Writing `test_update_order_status_invalid_status`
  first revealed that status validation must happen before the storage
  lookup — a detail easy to miss without TDD. The failing test drove
  the correct implementation order.

- **Next step:** Add a DELETE endpoint and persistent storage
  (e.g. SQLite) so orders survive server restarts.