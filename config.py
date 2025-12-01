import os

#BURAYA KENDİ API ANAHTARINIZI KOYUN, YOUR API KEY HERE
GROQ_API_KEY_VALUE = '...' 


# NOT: Bu yolu kendi sisteminize göre güncellemeyi unutmayın!
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PERFUME_DATABASE_PATH = os.path.join(BASE_DIR, 'perfume_database_20250904_201308.json')

class Config:
    # SECRET_KEY değeri hala çevre değişkeninden alınabilir.
    SECRET_KEY = os.environ.get('SECRET_KEY', 'cokgizlibirkey')
    
    DEBUG = True  # Geliştirme ortamı için True
    
    # Doğrudan koda gömülü anahtar değerini kullanıyoruz.
    GROQ_API_KEY = GROQ_API_KEY_VALUE
        
    PERFUME_DATABASE_PATH = PERFUME_DATABASE_PATH