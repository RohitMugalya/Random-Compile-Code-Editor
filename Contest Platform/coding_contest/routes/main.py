from flask import Blueprint, render_template, request, redirect, url_for, session
import pandas as pd
from config import config

main_bp = Blueprint("main", __name__)

@main_bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form.get("username")
        if username:
            session["username"] = username  # Store username in session
            return redirect(url_for("main.playground"))
    return render_template("index.html")

@main_bp.route("/playground")
def playground():
    if "username" not in session:
        return redirect(url_for("main.index"))  # Redirect if no username

    # Load a question from the Excel file
    try:
        df = pd.read_excel(config.EXCEL_FILE)
        question_data = df.sample(n=1).iloc[0]  # Pick a random question
        question = question_data["Question"]
        points = question_data["Points"]
    except Exception as e:
        print(f"Error loading questions: {e}")
        question, points = "Error loading question.", 0

    return render_template("playground.html", question=question, points=points)
