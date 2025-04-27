import firebase_admin
from firebase_admin import credentials, firestore
import os
import json
from dotenv import load_dotenv

# Only load .env file in development
if os.getenv('VERCEL_ENV') != 'production':
    load_dotenv()

def initialize_firebase():
    """Initialize Firebase Admin SDK"""
    try:
        # Check if app is already initialized
        firebase_admin.get_app()
    except ValueError:
        try:
            # First try to get the service account from environment variable
            service_account_info = json.loads(os.getenv('FIREBASE_SERVICE_ACCOUNT', '{}'))
            
            if not service_account_info:
                # If env var is not set, try to load from local file (development only)
                if os.path.exists('firebase-service-account.json'):
                    with open('firebase-service-account.json', 'r') as f:
                        service_account_info = json.load(f)
                else:
                    raise ValueError("No Firebase credentials found")

            # Fix private key if necessary
            if 'private_key' in service_account_info:
                service_account_info['private_key'] = service_account_info['private_key'].replace('\\n', '\n')

            cred = credentials.Certificate(service_account_info)
            firebase_admin.initialize_app(cred)
        except Exception as e:
            print(f"Error initializing Firebase: {str(e)}")
            raise

def get_db():
    """Get Firestore client"""
    return firestore.client()

def get_db_ref():
    """Get a reference to the database"""
    return firestore.client() # Changed from db.reference('/') as it's not defined 