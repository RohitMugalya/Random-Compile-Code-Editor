#!/bin/bash

# Define base directory
PROJECT_NAME="coding_contest"
mkdir -p $PROJECT_NAME

# Create main files
touch $PROJECT_NAME/{app.py,config.py,requirements.txt,run.py}

# Create subdirectories
mkdir -p $PROJECT_NAME/static/css
mkdir -p $PROJECT_NAME/static/js
mkdir -p $PROJECT_NAME/templates
mkdir -p $PROJECT_NAME/uploads
mkdir -p $PROJECT_NAME/data
mkdir -p $PROJECT_NAME/models
mkdir -p $PROJECT_NAME/routes
mkdir -p $PROJECT_NAME/utils

# Create static files
touch $PROJECT_NAME/static/css/style.css
touch $PROJECT_NAME/static/js/script.js

# Create template files
touch $PROJECT_NAME/templates/{index.html,playground.html,leaderboard.html}

# Create an empty Excel file for questions
touch $PROJECT_NAME/data/questions.xlsx

# Create model files
touch $PROJECT_NAME/models/{user.py,submission.py}

# Create route files
touch $PROJECT_NAME/routes/{main.py,contest.py,leaderboard.py}

# Create utility scripts
touch $PROJECT_NAME/utils/{code_execution.py,scoring.py,excel_parser.py}

echo "Project structure for '$PROJECT_NAME' created successfully!"
