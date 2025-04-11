import os
from typing import Dict, Any
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore, auth


secret_env_path = "/secrets/app-env-vars.json"
if os.path.exists(secret_env_path):
    import json
    with open(secret_env_path) as f:
        secret_vars = json.load(f)
    os.environ.update(secret_vars)

load_dotenv()

class Settings(BaseSettings):
    # Firebase configuration
    FIREBASE_PROJECT_ID: str = os.getenv("FIREBASE_PROJECT_ID", "")
    FIREBASE_CREDENTIALS: str = os.getenv("FIREBASE_CREDENTIALS", "")
    FIREBASE_WEB_API_KEY: str = os.getenv("FIREBASE_WEB_API_KEY", "")
    FIREBASE_DATABASE_URL: str = os.getenv("FIREBASE_DATABASE_URL", "")
    
    # API settings
    API_DEBUG: bool = os.getenv("API_DEBUG", "False").lower() in ("true", "1", "t")
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    
    # Event settings
    DEFAULT_EVENT_RADIUS_KM: float = 10.0
    MAX_EVENTS_PER_REQUEST: int = 100
    
    # Recommendation settings
    MIN_MATCH_PERCENTAGE: int = 25
    
    model_config = {
        "env_file": ".env",
        "extra": "ignore"  # Allow extra fields from .env
    }

settings = Settings()

# Firebase initialization
firebase_creds_path = settings.FIREBASE_CREDENTIALS or "/secrets/firebase-adminsdk.json"
if not os.path.exists(firebase_creds_path):
    raise RuntimeError(f"Firebase credentials not found at: {firebase_creds_path}")

cred = credentials.Certificate(firebase_creds_path)
firebase_admin.initialize_app(cred, {
    'databaseURL': settings.FIREBASE_DATABASE_URL
})

# 4. Firestore client
db = firestore.client()

__all__ = ['db', 'settings']
