from flask import render_template

def register_pages(app):

    @app.route("/")
    def login_page():
        return render_template("login.html")

    @app.route("/admin")
    def admin_page():
        return render_template("admin.html")

    @app.route("/emp")
    def emp_page():
        return render_template("emp.html")
