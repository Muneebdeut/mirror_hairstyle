import sys
import os

# Add backend directory to path so 'app' imports work smoothly
backend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "backend")
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app.main import app

# Export app for Vercel Serverless Function handler
app = app
