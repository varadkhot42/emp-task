from flask import request, jsonify
from app.db import get_db
import uuid
from functools import wraps

TOKENS = {}  # token -> user dict


# ---------------- AUTH DECORATOR ---------------- #

def auth_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        header = request.headers.get("Authorization")

        if not header or not header.startswith("Bearer "):
            return jsonify({"error": "Missing token"}), 401

        token = header.split(" ")[1]

        user = TOKENS.get(token)
        if not user:
            return jsonify({"error": "Invalid token"}), 401

        request.user = user
        return fn(*args, **kwargs)

    return wrapper


# ---------------- ROUTES ---------------- #

def register_routes(app):

    # ---------- LOGIN ---------- #

    @app.route("/login", methods=["POST"])
    def login():
        data = request.json

        conn = get_db()
        cur = conn.cursor()

        cur.execute(
            "SELECT id, username, role FROM users WHERE username=%s AND password=%s",
            (data["username"], data["password"]),
        )

        row = cur.fetchone()
        cur.close()
        conn.close()

        if not row:
            return {"error": "Invalid credentials"}, 401

        token = str(uuid.uuid4())

        TOKENS[token] = {
            "id": row[0],
            "username": row[1],
            "role": row[2],
        }

        return {"token": token, "role": row[2]}

    # ---------- CREATE TASK ---------- #

    @app.route("/tasks", methods=["POST"])
    @auth_required
    def create_task():
        user = request.user

        if user["role"] != "admin":
            return {"error": "Only admin can create tasks"}, 403

        data = request.json

        conn = get_db()
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO tasks (title, description, status, created_by, assigned_to)
            VALUES (%s,%s,%s,%s,%s)
            RETURNING id
            """,
            (
                data["title"],
                data.get("description", ""),
                "OPEN",
                user["id"],
                data["assigned_to"],
            ),
        )

        task_id = cur.fetchone()[0]
        conn.commit()

        cur.close()
        conn.close()

        return {"message": "Task created", "task_id": task_id}

    # ---------- LIST TASKS ---------- #

    @app.route("/tasks", methods=["GET"])
    @auth_required
    def list_tasks():
        user = request.user

        conn = get_db()
        cur = conn.cursor()

        if user["role"] == "admin":
            cur.execute("SELECT * FROM tasks")
        else:
            cur.execute("SELECT * FROM tasks WHERE assigned_to=%s", (user["id"],))

        rows = cur.fetchall()
        cols = [d[0] for d in cur.description]

        cur.close()
        conn.close()

        return jsonify([dict(zip(cols, r)) for r in rows])

    # ---------- UPDATE TASK ---------- #

    @app.route("/tasks/<int:task_id>", methods=["PUT"])
    @auth_required
    def update_task(task_id):
        user = request.user
        data = request.json

        conn = get_db()
        cur = conn.cursor()

        cur.execute(
            "SELECT assigned_to FROM tasks WHERE id=%s",
            (task_id,),
        )

        row = cur.fetchone()

        if not row:
            return {"error": "Task not found"}, 404

        assigned_to = row[0]

        if user["role"] != "admin" and assigned_to != user["id"]:
            return {"error": "Not allowed"}, 403

        cur.execute(
            """
            UPDATE tasks
            SET title=%s, description=%s, status=%s
            WHERE id=%s
            """,
            (
                data["title"],
                data["description"],
                data["status"],
                task_id,
            ),
        )

        conn.commit()
        cur.close()
        conn.close()

        return {"message": "Task updated"}

    # ---------- DELETE TASK ---------- #

    @app.route("/tasks/<int:task_id>", methods=["DELETE"])
    @auth_required
    def delete_task(task_id):
        user = request.user

        if user["role"] != "admin":
            return {"error": "Only admin can delete"}, 403

        conn = get_db()
        cur = conn.cursor()

        cur.execute("DELETE FROM tasks WHERE id=%s", (task_id,))
        conn.commit()

        cur.close()
        conn.close()

        return {"message": "Task deleted"}
