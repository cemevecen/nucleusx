# 🚀 NucleusX AI | Haber Havuzu

NucleusX, Twitter (X) üzerinden güncel haberleri toplayan ve Google Gemini AI kullanarak kategorize eden modern bir haber aggregator uygulamasıdır.

## ✨ Özellikler
- 📡 **Canlı Veri:** RapidAPI aracılığıyla gerçek zamanlı tweet çekme.
- 🤖 **AI Sınıflandırma:** Gemini 1.5 Flash ile haberleri Spor, Ekonomi, Teknoloji ve Eğlence olarak ayırma.
- 💎 **Glassmorphism UI:** Modern ve şık Streamlit arayüzü.
- 📊 **İstatistikler:** Hangi kategoride kaç haber olduğunu anlık görme.

## 🛠 Kurulum

1. Depoyu klonlayın:
   ```bash
   git clone https://github.com/cemevecen/nucleusx.git
   cd nucleusx
   ```

2. Bağımlılıkları yükleyin:
   ```bash
   pip install -r requirements.txt
   ```

3. `.env` dosyanızı oluşturun ve anahtarları ekleyin:
   ```env
   GEMINI_API_KEY=your_key_here
   RAPIDAPI_KEY=your_key_here
   ```

4. Uygulamayı çalıştırın:
   ```bash
   streamlit run app.py
   ```

## ☁️ Streamlit Cloud Dağıtımı

Streamlit Cloud üzerinde çalıştırırken **Settings > Secrets** kısmına aşağıdaki anahtarları eklemeyi unutmayın:

```toml
GEMINI_API_KEY = "your_key"
RAPIDAPI_KEY = "your_key"
```

## 📜 Lisans
Bu proje Antigravity AI tarafından geliştirilmiştir.
