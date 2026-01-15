"""
Configuration du frontend Flet
"""
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration de l'API
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
API_TIMEOUT = int(os.getenv("API_TIMEOUT", "30"))

# Configuration de l'application
APP_NAME = "Budget App"
APP_VERSION = "2.0.0"
APP_WINDOW_WIDTH = 1200
APP_WINDOW_HEIGHT = 800
