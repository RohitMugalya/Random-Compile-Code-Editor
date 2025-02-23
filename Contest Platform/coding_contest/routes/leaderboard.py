from flask import Blueprint, render_template, session, jsonify
import json
import os

leaderboard_bp = Blueprint("leaderboard", __name__)

LEADERBOARD_FILE = "data/leaderboard.json"

def load_leaderboard():
    """Loads leaderboard data from a JSON file."""
    if os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_leaderboard(leaderboard):
    """Saves leaderboard data to a JSON file."""
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(leaderboard, f, indent=4)

@leaderboard_bp.route("/leaderboard")
def view():
    """Displays the leaderboard page."""
    leaderboard = sorted(load_leaderboard(), key=lambda x: (-x["points"], x["submissions"]))
    return render_template("leaderboard.html", leaderboard=enumerate(leaderboard, start=1))

@leaderboard_bp.route("/update_leaderboard", methods=["POST"])
def update_leaderboard():
    """Updates the leaderboard with the latest submission."""
    if "username" not in session:
        return jsonify({"message": "User not logged in"}), 403

    data = session["username"]
    new_score = int(session.get("latest_score", 0))  # Default score to 0
    total_tests = int(session.get("latest_total_tests", 1))

    leaderboard = load_leaderboard()
    user_entry = next((user for user in leaderboard if user["name"] == data), None)

    if user_entry:
        user_entry["points"] += new_score
        user_entry["submissions"] += 1
    else:
        leaderboard.append({"name": data, "points": new_score, "submissions": 1})

    save_leaderboard(leaderboard)
    return jsonify({"message": "Leaderboard updated successfully!"})
