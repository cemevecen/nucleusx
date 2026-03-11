import os
from google import genai
from dotenv import load_dotenv
from database import init_db, save_tweet, tweet_exists
import time
from twitter_scraper import fetch_user_tweets

# .env dosyasındaki anahtarları yükler
load_dotenv()

# Veritabanını kullanıma hazır hale getir (Yoksa oluşturur)
init_db()

# Yeni Google GenAI kütüphanesi başlatımı
# Cloud ortamında (Streamlit) secrets'tan okumak için düzenlendi
api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

try:
    if api_key:
        client = genai.Client(api_key=api_key)
    else:
        client = None
        print("⚠️ Uyarı: GEMINI_API_KEY bulunamadı.")
except Exception as e:
    client = None
    print(f"❌ NucleusX Gemini Client Hatası: {e}")

def get_fallback_category(text):
    """AI hata verdiğinde anahtar kelimelerle kategori tahmini yapar."""
    text = text.lower()
    keywords = {
        "Ekonomi": ["dolar", "euro", "faiz", "enflasyon", "zam", "asgari", "maai", "bakanlık", "vergi"],
        "Finans": ["borsa", "hisse", "temettü", "kripto", "bitcoin", "altın", "btc", "eth", "yatırım"],
        "Spor": ["gol", "maç", "skor", "futbol", "basketbol", "fenerbahçe", "galatasaray", "beşiktaş", "transfer"],
        "Teknoloji": ["iphone", "apple", "android", "yazılım", "yapay zeka", "ai", "internet", "google", "çip"],
        "Eğlence": ["film", "dizi", "netflix", "sinema", "oyuncu", "magazin", "ünlü"],
        "Müzik": ["şarkı", "albüm", "konser", "klip", "single", "sanatçı", "spotify"],
        "Dünya": ["savaş", "abd", "rusya", "israil", "gazze", "nato", "avrupa", "bm"],
        "Ülke Gündemi": ["siyaset", "seçim", "meclis", "parti", "istifa", "belediye", "trt", "aa"]
    }
    
    for cat, words in keywords.items():
        if any(word in text for word in words):
            return cat
    return "Ülke Gündemi" # Varsayılan kategori

def categorize_tweet(tweet_text):
    """Tweet metnini alır ve Gemini yapay zekası yardımıyla kategorize eder."""
    
    if not client:
        return get_fallback_category(tweet_text)
    
    prompt = f"""Metni oku ve şu kategorilerden birini seç: Ekonomi, Finans, Spor, Teknoloji, Eğlence, Müzik, Dünya, Ülke Gündemi. Sadece kategori ismini yaz.
    Metin: "{tweet_text}" """
    
    try:
        response = client.models.generate_content(
            model='gemini-flash-latest',
            contents=prompt
        )
        res = response.text.strip().replace("[", "").replace("]", "").replace(".", "")
        if res in ["Ekonomi", "Finans", "Spor", "Teknoloji", "Eğlence", "Müzik", "Dünya", "Ülke Gündemi"]:
            return res
        return get_fallback_category(tweet_text)
    except Exception as e:
        print(f"⚠️ Gemini hatası (Fallback kullanılıyor): {e}")
        return get_fallback_category(tweet_text)

def run_categorization_process():
    """Tüm hedef hesaplardan tweetleri çeker, kategorize eder ve kaydeder."""
    target_accounts = [
        # Ülke Gündemi
        "pusholder", "ajans_muhbir",
        # Dünya
        "bbcturkce", "euronews_tr",
        # Ekonomi
        "ozgurdemirtas", "temelanaliz",
        # Finans
        "borsagundem", "ParaAnaliz",
        # Teknoloji
        "shiftdelete", "webteknoloji",
        # Spor
        "yagosabuncuoglu", "sporx",
        # Eğlence
        "boxofficeturkey", "raninitv",
        # Müzik
        "MuzikOnair", "PopBizde"
    ]
    
    print("-" * 50)
    print("🚀 NucleusX AI Haber Sınıflandırıcı Motoru Başlıyor...")
    print("-" * 50)
    
    for username in target_accounts:
        # Streamlit'e o an taranan hesabı bildirelim
        yield f"📡 {username} hesabından tweetler çekiliyor..."
        
        tweets = fetch_user_tweets(username, limit=5) # 10 çok yavaşlattığı için 5 ideal
        
        if not tweets:
            print(f"🔍 {username} için yeni tweet bulunamadı veya bir hata oluştu.")
            continue
            
        for tweet in tweets:
            # 1. Mükerrer Kontrolü (İçeriğin ilk 50 karakteri üzerinden daha esnek kontrol)
            # Sadece tam eşleşme yerine kullanıcı adı + kısa özet kontrolü
            if tweet_exists(tweet['username'], tweet['text']):
                print(f"⏩ {tweet['username']} için bu tweet zaten işlenmiş, atlanıyor.")
                continue

            print(f"\n👤 GÖNDEREN: {tweet['author']} ({tweet['username']})")
            print(f"📝 TWEET: {tweet['text'][:100]}...") # Uzun tweetleri keserek basıyoruz
            
            # 2. Rate Limiting (Ücretsiz Planı Korumak İçin)
            # 16 hesap taranacağı için RPM (istek başına dakika) sınırına takılmamak adına 
            # 1.5 - 2 saniye idealdir.
            time.sleep(2) 

            # Yapay Zeka Devreye Girer
            kategori = categorize_tweet(tweet['text'])

            # Veritabanına kaydet (Resim varsa ekle)
            save_tweet(tweet['author'], tweet['username'], tweet['text'], kategori, media_url=tweet.get('media_url'))
            yield f"✅ {tweet['username']}: [{kategori}]"
    
    print("\n" + "-" * 50)
    print("✅ Analiz Tamamlandı! Tüm veriler NucleusX veritabanına işlendi.")

if __name__ == "__main__":
    init_db()
    for status in run_categorization_process():
        print(status)
