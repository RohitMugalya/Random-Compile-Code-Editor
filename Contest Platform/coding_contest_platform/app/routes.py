import random
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models import User, Question, Submission
from app.forms import JoinContestForm, SubmitCodeForm
from app.utils.code_evaluator import evaluate_code
from app.utils.leaderboard_calculator import calculate_leaderboard
from app import db

# Create a Blueprint for the routes
main_bp = Blueprint('main', __name__)

# Route for the home page
@main_bp.route('/', methods=['GET', 'POST'])
def index():
    form = JoinContestForm()
    if form.validate_on_submit():
        # Get the user's name from the form
        name = form.name.data

        # Check if the user already exists in the database
        user = User.query.filter_by(name=name).first()
        if not user:
            # Create a new user if they don't exist
            user = User(name=name)
            db.session.add(user)
            db.session.commit()

        # Redirect to the code playground
        return redirect(url_for('main.playground', user_id=user.id))

    return render_template('index.html', form=form)

# Route for the code playground
@main_bp.route('/playground/<int:user_id>', methods=['GET', 'POST'])
def playground(user_id):
    # Fetch the user from the database
    user = User.query.get(user_id)
    if not user:
        flash('User not found!', 'danger')
        return redirect(url_for('main.index'))

    # Fetch a random question from the database
    question = Question.query.order_by(db.func.random()).first()
    if not question:
        flash('No questions available!', 'danger')
        return redirect(url_for('main.index'))

    # Create an instance of the SubmitCodeForm
    form = SubmitCodeForm()

    # Generate shuffled line numbers (1 to 60)
    shuffled_lines = list(range(1, 61))
    random.shuffle(shuffled_lines)

    # Store the shuffled mapping in the session for later use
    session['shuffled_lines'] = shuffled_lines

    return render_template('playground.html', user=user, question=question, form=form, shuffled_lines=shuffled_lines)

# Route for submitting code
@main_bp.route('/submit/<int:user_id>/<int:question_id>', methods=['POST'])
def submit_code(user_id, question_id):
    # Fetch the user and question from the database
    user = User.query.get_or_404(user_id)
    question = Question.query.get_or_404(question_id)

    # Debugging: Print the form data
    print("Form Data:", request.form)

    # Get the submitted code
    code = request.form.get('code')
    if not code:
        flash('No code submitted!', 'danger')
        return redirect(url_for('main.playground', user_id=user.id))

    # Debugging: Print the submitted code
    print("Submitted Code:", code)

    # Get the shuffled mapping from the session
    shuffled_lines = session.get('shuffled_lines', list(range(1, 61)))

    # Split the code into lines
    code_lines = code.split('\n')

    # Debugging: Print the code lines
    print("Code Lines:", code_lines)

    # Reorder the lines using the shuffled mapping
    reordered_code_lines = []
    for line_num in range(len(code_lines)):
        original_line_num = shuffled_lines[line_num] - 1  # Convert to 0-based index
        if original_line_num < len(code_lines):
            reordered_code_lines.append((original_line_num, code_lines[original_line_num]))

    # Sort the lines by the original line numbers
    reordered_code_lines.sort(key=lambda x: x[0])
    reordered_code = '\n'.join([line[1] for line in reordered_code_lines])

    # Debugging: Print the reordered code
    print("Reordered Code:", reordered_code)

    # Get the selected language
    language = request.form.get('language')
    if not language:
        flash('No language selected!', 'danger')
        return redirect(url_for('main.playground', user_id=user.id))

    # Evaluate the reordered code
    result, passed_test_cases = evaluate_code(reordered_code, language, question)

    # Calculate the score
    score = (passed_test_cases / len(question.test_cases)) * question.points

    # Update the user's total score
    user.total_score += score
    db.session.commit()

    # Render the submit.html template
    return render_template('submit.html',
                           user=user,
                           result=result,
                           passed_test_cases=passed_test_cases,
                           total_test_cases=len(question.test_cases),
                           score=score)

# Route for the leaderboard
@main_bp.route('/leaderboard')
def leaderboard():
    # Fetch all users sorted by their total score
    users = User.query.order_by(User.total_score.desc()).all()
    return render_template('leaderboard.html', users=users)