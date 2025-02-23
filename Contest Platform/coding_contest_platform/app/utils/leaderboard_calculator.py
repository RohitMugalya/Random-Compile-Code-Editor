from app.models import User

def calculate_leaderboard():
    """
    Calculate and update the leaderboard based on the total scores of all users.
    """
    # Fetch all users and sort them by total_score in descending order
    users = User.query.order_by(User.total_score.desc()).all()

    # Update ranks (optional: if you want to store ranks in the database)
    for rank, user in enumerate(users, start=1):
        user.rank = rank

    # Commit changes to the database
    from app import db
    db.session.commit()