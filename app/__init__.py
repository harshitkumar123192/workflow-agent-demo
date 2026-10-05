from flask import Flask, jsonify, request


def create_app():
    app = Flask(__name__)
    tasks = []
    next_id = 1

    @app.get("/")
    def index():
        return jsonify({"service": "workflow-agent-demo", "status": "ok"})

    @app.get("/tasks")
    def list_tasks():
        return jsonify({"tasks": tasks})

    @app.post("/tasks")
    def create_task():
        nonlocal next_id
        body = request.get_json(silent=True) or {}
        title = body.get("title")
        if not isinstance(title, str) or not title.strip():
            return jsonify({"error": "title is required"}), 400

        task = {"id": next_id, "title": title.strip(), "completed": False}
        next_id += 1
        tasks.append(task)
        return jsonify(task), 201

    return app