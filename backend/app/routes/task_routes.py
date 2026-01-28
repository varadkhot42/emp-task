from flask import Blueprint, jsonify
from app.utils.db import get_db_connection

task_bp = Blueprint("tasks", __name__)

@task_bp.route("/tasks", methods=["GET"])
def list_tasks():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, title, description, status FROM tasks")
    rows = cur.fetchall()

    tasks = []
    for r in rows:
        tasks.append({
            "id": r[0],
            "title": r[1],
            "description": r[2],
            "status": r[3]
        })

    cur.close()
    conn.close()
    return jsonify(tasks)
