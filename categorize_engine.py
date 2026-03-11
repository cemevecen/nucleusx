import os
from google import genai
from dotenv import load_dotenv
from database import init_db, save_tweet
from twitter_scraper import fetch_user_tweets

# .env dosyasındaki anahtarları yükler
load_dotenv()

# Veritabanını kullanıma hazır hale getir (Yoksa oluşturur)
init_db()

# Yeni Google GenAI kütüphanesi başlatımı
client = genai.Client()

def categorize_tweet(tweet_text):
    """Tweet metnini alır ve Gemini yapay zekası yardımıyla kategorize eder."""
    
    prompt = f"""
    Sen, NucleusX gibi bir haber toplayıcı (aggregator) için çalışan baş editörsün.
    Aşağıdaki tweet metnini oku ve onu bu 4 kategoriden sadece BİRİNE yerleştir:
    Kategoriler: Spor, Ekonomi, Teknoloji, Eğlence
    
    Eğer tweet alakasızsa veya anlaşılmıyorsa "Diğer" de.
    SADECE kategorinin adını yaz. Başka hiçbir açıklama yapma.
    
    Tweet: "{tweet_text}"
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        print(f"⚠️ Gemini hatası: {e}")
        return "Bilinmeyen Kategori"

# Tarayacağımız Örnek Haber / Gazeteci Hesapları
target_accounts = ["fatihaltayli", "yagosabuncuoglu", "shiftdelete", "boxofficeturkey"]

if __name__ == "__main__":
    print("-" * 50)
    print("🚀 AI Haber Sınıflandırıcı Motoru Başlıyor...")
    print("-" * 50)
    
    for username in target_accounts:
        print(f"\n📡 {username} hesabından tweetler çekiliyor...")
        tweets = fetch_user_tweets(username, limit=3)
        
        if not tweets:
            print(f"🔍 {username} için yeni tweet bulunamadı veya bir hata oluştu.")
            continue
            
        for tweet in tweets:
            print(f"\n👤 GÖNDEREN: {tweet['author']} ({tweet['username']})")
            print(f"📝 TWEET: {tweet['text'][:100]}...") # Uzun tweetleri keserek basıyoruz
            
            # Yapay Zeka Devreye Girer
            kategori = categorize_tweet(tweet['text'])
            
            # Veritabanına kaydet
            save_tweet(tweet['author'], tweet['username'], tweet['text'], kategori)
            
            print(f"🏷️ ATANAN KATEGORİ: [{kategori}]")
    
    print("\n" + "-" * 50)
    print("✅ Analiz Tamamlandı! Tüm veriler NucleusX veritabanına işlendi.")
