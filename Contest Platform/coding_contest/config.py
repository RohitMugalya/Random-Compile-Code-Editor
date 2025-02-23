import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")  # Change for production
    UPLOAD_FOLDER = "uploads"  # Directory to store uploaded files (if needed)
    ALLOWED_LANGUAGES = ["python", "cpp", "java", "c"]  # Supported languages
    EXCEL_FILE = "data/questions.xlsx"  # Path to questions file
    DEBUG = True  # Enable debugging mode

class ProductionConfig(Config):
    DEBUG = False  # Disable debugging in production

class DevelopmentConfig(Config):
    DEBUG = True  # Enable debugging for development

# Select config based on environment
config = DevelopmentConfig if os.getenv("FLASK_ENV") == "development" else ProductionConfig
