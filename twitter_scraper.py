import os
import requests
from dotenv import load_dotenv

load_dotenv()

# RapidAPI üzerinden alınacak anahtar
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

# HANGİ APİ'Yİ SEÇECEĞİMİZE GÖRE BU HOST VE ENDPOINT DEĞİŞECEK.
# Şimdilik en popülerlerden biri olan şablonu kullanıyorum.
RAPIDAPI_HOST = "twitter-api45.p.rapidapi.com" 

def fetch_user_tweets(username, limit=5):
    """
    Belirtilen kullanıcının son tweetlerini RapidAPI üzerinden ücretsiz çeker.
    """
    if not RAPIDAPI_KEY:
        print("❌ HATA: RAPIDAPI_KEY bulunamadı. Lütfen .env dosyasına ekleyin.")
        return []
        
    url = f"https://{RAPIDAPI_HOST}/timeline.php"
    
    querystring = {"screenname": username}
    
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST
    }
    
    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status() 
        
        data = response.json()
        
        extracted_tweets = []
        
        # twitter-api45 dönen veri yapısına göre düzenlenmiştir
        # genelde liste döner veya "timeline" objesi içinde döner.
        timeline_data = data.get('timeline', []) if isinstance(data, dict) else data
        
        for item in timeline_data[:limit]:
            # Retweetleri atla, sadece kendi gönderilerini al
            if "tweet" in item:
                tweet_text = item.get("tweet", {}).get("text", "")
            else:
                tweet_text = item.get("text", "")
            
            if tweet_text:
                extracted_tweets.append({
                    "author": username.capitalize(),
                    "username": f"@{username}",
                    "text": tweet_text
                })
                     
        return extracted_tweets
        
    except Exception as e:
        print(f"❌ Tweetler çekilirken hata oluştu: {e}")
        return []

if __name__ == "__main__":
    print("Test amacıyla @fatihaltayli kullanıcısının tweetleri çekiliyor...")
    tweets = fetch_user_tweets("fatihaltayli", limit=2)
    
    if tweets:
        for t in tweets:
            print(f"- {t['text']}")
    else:
        print("Boş liste döndü veya hata alındı.")
