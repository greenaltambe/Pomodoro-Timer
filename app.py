from flask import Flask, render_template, redirect, request, url_for, session
from helper import engine, User, FocusSession
from sqlalchemy.orm import sessionmaker
from functools import wraps
from flask import request, jsonify
from datetime import datetime

app = Flask(__name__)
app.secret_key = "INDIA"

# Setup the database
Session = sessionmaker(bind=engine)  # Session factory for database sessions


# Ensures that login is required for all routes
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect(
                url_for("login", message="Please log in to access this page")
            )
        return f(*args, **kwargs)

    return decorated_function


@app.route("/focus_data", methods=["POST"])
def focus_data():
    if "user_id" not in session:
        return jsonify({"status": "error", "message": "User not logged in"}), 401

    data = request.json
    total_focus_time = data["totalFocusTime"]
    focus_start_time = datetime.fromtimestamp(data["focusStartTime"] / 1000.0)

    db_session = Session()

    try:
        new_session = FocusSession(
            user_id=session["user_id"],
            start_time=focus_start_time,
            duration=total_focus_time,
        )
        db_session.add(new_session)
        db_session.commit()
        app.logger.info(
            f"New focus session added - User ID: {session['user_id']}, Start time: {focus_start_time}, Duration: {total_focus_time} seconds"
        )
        return jsonify({"status": "success"}), 200
    except Exception as e:
        db_session.rollback()
        app.logger.error(f"Error updating focus time: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        db_session.close()


@app.route("/")
@login_required
def index():
    return render_template("index.html")


# Register new user
@app.route("/register", methods=["GET", "POST"])
def register():
    message = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if password != confirm_password:
            message = "Passwords do not match"
        else:
            db_session = Session()
            try:
                existing_user = (
                    db_session.query(User).filter_by(username=username).first()
                )
                if existing_user:
                    message = "User already exists"
                else:
                    new_user = User(username=username)
                    new_user.set_password(password)
                    db_session.add(new_user)
                    db_session.commit()
                    return redirect(url_for("login", message="Registered successfully"))
            finally:
                db_session.close()

    return render_template("register.html", message=message)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        db_session = Session()

        try:
            user = db_session.query(User).filter_by(username=username).first()
            if user and user.check_password(password):
                session["user_id"] = user.id
                return redirect(url_for("index", message="Logged in successfully"))
            else:
                return redirect(url_for("login", message="Invalid credentials"))

        except Exception as e:
            app.logger.error(f"Error logging in: {str(e)}")
        finally:
            db_session.close()

    message = request.args.get("message")
    return render_template("login.html", message=message)


@app.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    db_session = Session()
    user_data_table = (
        db_session.query(FocusSession).filter_by(user_id=session["user_id"]).all()
    )
    return render_template("dashboard.html", user_data_table=user_data_table)


@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("login", message="Logged out successfully"))


if __name__ == "__main__":
    app.run(debug=True)
