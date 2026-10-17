import os

# API anahtarı koda yazılmaz; GROQ_API_KEY ortam değişkeninden okunur.
# Set your key via the GROQ_API_KEY environment variable.
GROQ_API_KEY_VALUE = os.environ.get('GROQ_API_KEY', '')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PERFUME_DATABASE_PATH = os.path.join(BASE_DIR, 'perfume_database_20250904_201308.json')

class Config:
    # Üretimde mutlaka SECRET_KEY ortam değişkeni tanımlayın; varsayılan yalnızca yerel geliştirme içindir.
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-only-change-me')
    
    # Geliştirme ortamı için varsayılan True; üretimde FLASK_DEBUG=false verin.
    DEBUG = os.environ.get('FLASK_DEBUG', 'true').lower() in ('1', 'true', 'yes')
    
    GROQ_API_KEY = GROQ_API_KEY_VALUE
        
    PERFUME_DATABASE_PATH = PERFUME_DATABASE_PATH