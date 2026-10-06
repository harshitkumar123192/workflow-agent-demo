from flask import Flask, jsonify, request


def create_app():
    app = Flask(__name__)

    # Pre-seeded sample data across multiple categories
    expenses = [
        {"id": 1, "description": "Team lunch", "amount": 45.00, "category": "Food"},
        {"id": 2, "description": "Coffee meeting", "amount": 8.50, "category": "Food"},
        {"id": 3, "description": "Team snacks", "amount": 22.00, "category": "Food"},
        {"id": 4, "description": "Cloud server hosting", "amount": 120.00, "category": "Software"},
        {"id": 5, "description": "Domain registration", "amount": 15.00, "category": "Software"},
        {"id": 6, "description": "Train ticket", "amount": 18.50, "category": "Transport"},
        {"id": 7, "description": "Airport taxi", "amount": 35.00, "category": "Transport"},
        {"id": 8, "description": "Monitor stand", "amount": 29.99, "category": "Office"},
    ]
    next_id = 9

    @app.get("/")
    def index():
        return jsonify({"service": "expense-tracker", "status": "ok"})

    @app.get("/expenses")
    def list_expenses():
        return jsonify({"expenses": expenses})

    @app.post("/expenses")
    def create_expense():
        nonlocal next_id
        body = request.get_json(silent=True) or {}

        description = body.get("description")
        category = body.get("category")
        amount = body.get("amount")

        if not isinstance(description, str) or not description.strip():
            return jsonify({"error": "description is required"}), 400

        if not isinstance(category, str) or not category.strip():
            return jsonify({"error": "category is required"}), 400

        if not isinstance(amount, (int, float)) or amount <= 0:
            return jsonify({"error": "amount must be a positive number"}), 400

        expense = {
            "id": next_id,
            "description": description.strip(),
            "amount": round(float(amount), 2),
            "category": category.strip(),
        }
        next_id += 1
        expenses.append(expense)
        return jsonify(expense), 201

    @app.get("/summary")
    def spending_summary():
        by_category = {}
        total = 0.0

        for item in expenses:
            cat = item["category"]
            amt = item["amount"]
            by_category[cat] = round(by_category.get(cat, 0.0) + amt, 2)
            total = round(total + amt, 2)

        return jsonify({"total": total, "by_category": by_category})

    return app