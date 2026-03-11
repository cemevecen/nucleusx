import sqlite3
from datetime import datetime

DB_NAME = "nucleusx.db"

def init_db():
    """Veritabanını ve gerekli tabloları oluşturur."""
    print(f"🗄️ Veritabanı kontrol ediliyor: {DB_NAME}")
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Haber/Tweet tablosu oluşturuluyor
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tweets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            author TEXT,
            username TEXT,
            content TEXT,
            category TEXT,
            media_url TEXT,
            processed_at TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def tweet_exists(username, content):
    """Aynı tweetin daha önce kaydedilip edilmediğini kontrol eder."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM tweets WHERE username = ? AND content = ?', (username, content))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def save_tweet(author, username, content, category, media_url=None):
    """Analiz edilen tweeti veritabanına kaydeder."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute('''
        INSERT INTO tweets (author, username, content, category, media_url, processed_at)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (author, username, content, category, media_url, now))
    
    conn.commit()
    conn.close()

def get_recent_tweets(limit=10):
    """Son kaydedilen tweetleri getirir."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT author, username, content, category, processed_at, media_url 
        FROM tweets 
        ORDER BY processed_at DESC 
        LIMIT ?
    ''', (limit,))
    
    results = cursor.fetchall()
    conn.close()
    return results

# Dosya ilk kez çalıştırıldığında veritabanını kur
if __name__ == "__main__":
    init_db()
    print("✅ Veritabanı başarıyla kuruldu!")
