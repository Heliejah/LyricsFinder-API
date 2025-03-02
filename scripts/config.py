import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    GENIUS_API_KEY = os.getenv('GENIUS_API_KEY', '8d24ecac8a15b24a3936bc2969a13e66')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    PORT = int(os.getenv('PORT', 5000))
    DEBUG = FLASK_ENV == 'development'
