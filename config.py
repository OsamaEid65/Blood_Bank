import os

class Config:
    SECRET_KEY = 'Osama'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/profile_images')

# Additional configurations if needed
