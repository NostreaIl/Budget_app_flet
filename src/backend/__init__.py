"""
Backend FastAPI - API REST pour Budget App
"""
from src.backend.main import app
from src.backend.config import API_VERSION, API_TITLE

__version__ = API_VERSION
__all__ = ['app', '__version__']
