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


def test_expenses_pre_seeded(client):
    response = client.get("/expenses")
    assert response.status_code == 200
    expenses = response.json["expenses"]
    assert len(expenses) == 8

    # Verify categories present in starter dataset
    categories = {e["category"] for e in expenses}
    assert categories == {"Food", "Software", "Transport", "Office"}


def test_filter_expenses_by_category(client):
    # Scenario 2: Filtering by a specific category
    response = client.get("/expenses?category=Food")
    assert response.status_code == 200
    expenses = response.json["expenses"]
    assert len(expenses) == 3
    for e in expenses:
        assert e["category"] == "Food"

    # Case-insensitive filtering check if applicable, or exact match
    response_lower = client.get("/expenses?category=food")
    assert response_lower.status_code == 200
    assert len(response_lower.json["expenses"]) == 3

    # Scenario 3: Filtering by a category with no expenses
    response_empty = client.get("/expenses?category=Entertainment")
    assert response_empty.status_code == 200
    assert response_empty.json["expenses"] == []


def test_create_expense_success(client):
    response = client.post(
        "/expenses",
        json={"description": "Notebook", "amount": 12.00, "category": "Office"},
    )
    assert response.status_code == 201
    assert response.json == {
        "id": 9,
        "description": "Notebook",
        "amount": 12.00,
        "category": "Office",
    }

    # Verify count increased from 8 to 9
    list_res = client.get("/expenses")
    assert len(list_res.json["expenses"]) == 9


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
    response = client.get("/summary")
    assert response.status_code == 200
    data = response.json

    assert data["total"] == 293.99
    assert data["by_category"] == {
        "Food": 75.50,
        "Software": 135.00,
        "Transport": 53.50,
        "Office": 29.99,
    }
