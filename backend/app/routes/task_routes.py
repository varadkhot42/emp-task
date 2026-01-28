from flask import Blueprint, request, jsonify
from app.utils.db import get_db_connection

task_bp = Blueprint("tasks", __name__)

# -----------------------------
# GET all tasks
# -----------------------------
@task_bp.route("/tasks", methods=["GET"])
def get_tasks():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, title, description, status FROM tasks")
    rows = cur.fetchall()

    cur.close()
    conn.close()

    tasks = []
    for row in rows:
        tasks.append({
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "status": row[3]
        })

    return jsonify(tasks), 200


# -----------------------------
# CREATE task
# -----------------------------
@task_bp.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()

    title = data.get("title")
    description = data.get("description")
    status = data.get("status", "PENDING")

    if not title:
        return {"error": "Title is required"}, 400

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO tasks (title, description, status)
        VALUES (%s, %s, %s)
        RETURNING id
        """,
        (title, description, status)
    )

    task_id = cur.fetchone()["id"]
    conn.commit()

    cur.close()
    conn.close()

    return {
        "message": "Task created",
        "task_id": task_id
    }, 201


# -----------------------------
# UPDATE task
# -----------------------------
@task_bp.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.get_json()

    title = data.get("title")
    description = data.get("description")
    status = data.get("status")

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE tasks
        SET title = %s,
            description = %s,
            status = %s
        WHERE id = %s
        """,
        (title, description, status, task_id)
    )

    if cur.rowcount == 0:
        cur.close()
        conn.close()
        return {"error": "Task not found"}, 404

    conn.commit()
    cur.close()
    conn.close()

    return {"message": "Task updated"}, 200


# -----------------------------
# DELETE task
# -----------------------------
@task_bp.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM tasks WHERE id = %s", (task_id,))

    if cur.rowcount == 0:
        cur.close()
        conn.close()
        return {"error": "Task not found"}, 404

    conn.commit()
    cur.close()
    conn.close()

    return {"message": "Task deleted"}, 200
