from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from auth import register_user, authenticate_user
from session_manager import (
    generate_session_token,
    revoke_session_token,
    verify_session_token,
)
import config

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = config.JWT_SECRET_KEY
jwt = JWTManager(app)


@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data["username"]
    password = data["password"]

    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400

    if register_user(username, password):
        return jsonify({"message": "User created successfully"}), 201
    else:
        return jsonify({"message": "User already exists"}), 400


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data["username"]
    password = data["password"]

    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400

    if authenticate_user(username, password):
        access_token = generate_session_token(username)
        return jsonify(
            {"message": "You can now access your tasks", "access_token": access_token}
        ), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401


@app.route("/tasks", methods=["GET"])
@jwt_required()
def get_tasks():
    if not verify_session_token(request.headers.get("Authorization").split(" ")[1]):
        return jsonify({"message": "Invalid session token"}), 401

    username = get_jwt_identity()
    # Some example tasks, you would replace this with calls to wherever the actual tasks are stored.
    tasks = {
        "tasks": [
            {
                "task_name": "Email TAs",
                "priority": "High",
                "category": "School",
                "status": "pending",
                "dueDate": "2025-02-10",
            },
            {
                "task_name": "Finish project report",
                "priority": "Medium",
                "category": "Work",
                "status": "in-progress",
                "dueDate": "2024-12-01",
            },
            {
                "task_name": "Grocery shopping",
                "priority": "Low",
                "category": "Personal",
                "status": "pending",
                "dueDate": "2023-11-15",
            },
            {
                "task_name": "Plan vacation",
                "priority": "Medium",
                "category": "Leisure",
                "status": "not-started",
                "dueDate": "2024-06-20",
            },
        ]
    }

    return jsonify({"username": username, "tasks": tasks}), 200


@app.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    username = get_jwt_identity()
    session_token = request.headers.get("Authorization").split(" ")[1]
    revoke_session_token(session_token)
    message = f"{username}, Logged out successfully"
    return jsonify({"message": message}), 200


if __name__ == "__main__":
    app.run(debug=True)
