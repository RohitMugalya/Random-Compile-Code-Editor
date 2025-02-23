from flask import Flask
from config import config
from routes.main import main_bp
from routes.contest import contest_bp
from routes.leaderboard import leaderboard_bp

app = Flask(__name__)
app.config.from_object(config)  # Load configurations

# Register Blueprints (modular route handling)
app.register_blueprint(main_bp)
app.register_blueprint(contest_bp)
app.register_blueprint(leaderboard_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=app.config["DEBUG"])
