from flask import Blueprint, request, jsonify, session
import subprocess
import tempfile
import os
import pandas as pd
from config import config

contest_bp = Blueprint("contest", __name__)

# Supported file extensions for each language
LANGUAGE_EXTENSIONS = {
    "python": ".py",
    "cpp": ".cpp",
    "java": ".java",
    "c": ".c"
}

# Command templates for execution
RUN_COMMANDS = {
    "python": ["python3"],
    "cpp": ["g++", "-o", "prog", "prog.cpp", "&&", "./prog"],
    "java": ["javac", "prog.java", "&&", "java", "prog"],
    "c": ["gcc", "-o", "prog", "prog.c", "&&", "./prog"]
}

@contest_bp.route("/submit", methods=["POST"])
def submit():
    if "username" not in session:
        return jsonify({"message": "User not logged in"}), 403

    data = request.get_json()
    code = data.get("code", "")
    language = data.get("language", "")

    if language not in LANGUAGE_EXTENSIONS:
        return jsonify({"message": "Unsupported language"}), 400

    # Load question test cases
    try:
        df = pd.read_excel(config.EXCEL_FILE)
        question_data = df.sample(n=1).iloc[0]  # Pick a random question
        test_cases = [(question_data[f"Input {i}"], str(question_data[f"Expected Output {i}"])) 
                      for i in range(1, len(question_data)//2 + 1) if f"Input {i}" in question_data]
        points = question_data["Points"]
    except Exception as e:
        print(f"Error loading questions: {e}")
        return jsonify({"message": "Error loading question"}), 500

    # Run and validate the code
    score, total_tests = execute_and_score(code, language, test_cases)

    return jsonify({
        "message": f"Code submitted successfully! {score}/{total_tests} test cases passed.",
        "score": score,
        "total_tests": total_tests,
        "points_awarded": (score / total_tests) * points if total_tests > 0 else 0
    })

def execute_and_score(code, language, test_cases):
    """Executes code in a temporary file and scores based on test cases."""
    ext = LANGUAGE_EXTENSIONS[language]
    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = os.path.join(temp_dir, f"prog{ext}")

        # Write code to file
        with open(file_path, "w") as f:
            f.write(code)

        if language == "java":
            class_name = extract_java_class_name(code)
            if not class_name:
                return 0, len(test_cases)
            file_path = os.path.join(temp_dir, f"{class_name}.java")

        # Execute test cases
        score = 0
        for test_input, expected_output in test_cases:
            result = run_code(file_path, language, test_input, temp_dir)
            if result.strip() == expected_output.strip():
                score += 1

        return score, len(test_cases)

def run_code(file_path, language, test_input, temp_dir):
    """Executes the given code file with the specified test input."""
    command = RUN_COMMANDS[language]
    command = [c.replace("prog", os.path.splitext(os.path.basename(file_path))[0]) for c in command]

    try:
        process = subprocess.run(command, input=test_input, text=True, capture_output=True, cwd=temp_dir, shell=True)
        return process.stdout.strip()
    except Exception as e:
        print(f"Execution error: {e}")
        return ""

def extract_java_class_name(code):
    """Extracts the Java class name from the code (assuming it has a class)."""
    for line in code.split("\n"):
        if line.strip().startswith("public class"):
            return line.split()[2].strip("{}")
    return None
