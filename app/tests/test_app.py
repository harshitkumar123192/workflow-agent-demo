import pytest

from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()


def test_health_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json["status"] == "ok"


def test_expenses_start_empty(client):
    response = client.get("/expenses")
    assert response.status_code == 200
    assert response.json == {"expenses": []}


def test_create_expense_success(client):
    response = client.post(
        "/expenses",
        json={"description": "Groceries", "amount": 42.50, "category": "Food"},
    )
    assert response.status_code == 201
    assert response.json == {
        "id": 1,
        "description": "Groceries",
        "amount": 42.50,
        "category": "Food",
    }

    # Verify listed
    list_res = client.get("/expenses")
    assert len(list_res.json["expenses"]) == 1


def test_create_expense_validation(client):
    # Missing description
    res1 = client.post("/expenses", json={"amount": 10, "category": "Food"})
    assert res1.status_code == 400
    assert "description is required" in res1.json["error"]

    # Missing category
    res2 = client.post("/expenses", json={"description": "Lunch", "amount": 10})
    assert res2.status_code == 400
    assert "category is required" in res2.json["error"]

    # Invalid amount (zero or negative)
    res3 = client.post(
        "/expenses",
        json={"description": "Lunch", "amount": -5, "category": "Food"},
    )
    assert res3.status_code == 400
    assert "amount must be a positive number" in res3.json["error"]


def test_spending_summary(client):
    client.post(
        "/expenses",
        json={"description": "Coffee", "amount": 5.50, "category": "Food"},
    )
    client.post(
        "/expenses",
        json={"description": "Lunch", "amount": 15.00, "category": "Food"},
    )
    client.post(
        "/expenses",
        json={"description": "Bus ticket", "amount": 3.00, "category": "Transport"},
    )

    response = client.get("/summary")
    assert response.status_code == 200
    assert response.json == {
        "total": 23.50,
        "by_category": {
            "Food": 20.50,
            "Transport": 3.00,
        },
    }