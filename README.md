# 🌸 Fragrance Discovery Platform

AI-powered perfume recommendation system. Analyzes user preferences and suggests the most suitable perfumes from the database.

## 📝 About the Project

This project allows users to describe the perfume notes they're looking for in natural language and find the most suitable perfumes through artificial intelligence.

**Example:** "I want a perfume with fresh citrus notes for summer" → The system extracts the notes and recommends matching perfumes from the database.

## 🚀 Installation and Running

### 1. Install Required Libraries

### 2. Get Groq API Key

- Go to [Groq Console](https://console.groq.com)
- Create a free account
- Copy your API key
- Paste it into the `GROQ_API_KEY_VALUE` section in `config.py`

### 3. Add Database File

Place the `perfume_database_20250904_201308.json` file in the project root directory.

### 4. Start the Application

```bash
python app.py
```

### 5. Open in Your Browser

```
http://127.0.0.1:5000
```

## 🛠️ Technologies Used

- **Backend:** Flask (Python)
- **AI:** Groq API (qwen/qwen3-32b model)
- **Frontend:** HTML, CSS, JavaScript
- **Database:** JSON

## ⚙️ Features

- Note extraction using natural language processing
- Intelligent matching algorithm
- Similarity scoring
- Performance optimization with pagination
- Modern and user-friendly interface

## 👥 Development Team

- [@cerennceyhan](https://github.com/cerennceyhan)
- [@ilaydabalal](https://github.com/ilaydabalal)

# 🌸 Fragrance Discovery Platform

Yapay zeka destekli parfüm öneri sistemi. Kullanıcının tercihlerini analiz eder ve veritabanından en uygun parfümleri önerir.

## 📝 Proje Hakkında

Bu proje, kullanıcıların aradıkları parfüm notalarını doğal dille yazabilmelerini ve yapay zeka aracılığıyla en uygun parfümleri bulmalarını sağlar.

**Örnek:** "Yaz için ferah narenciye notaları olan bir parfüm istiyorum" → Sistem notaları çıkarır ve veritabanından eşleşen parfümleri önerir.

## 🚀 Kurulum ve Çalıştırma

### 1. Gerekli Kütüphaneleri Yükleyin

### 2. Groq API Anahtarı Alın

- [Groq Console](https://console.groq.com) adresine gidin
- Ücretsiz hesap oluşturun
- API anahtarınızı kopyalayın
- `config.py` dosyasındaki `GROQ_API_KEY_VALUE` kısmına yapıştırın

### 3. Veritabanı Dosyasını Ekleyin

`perfume_database_20250904_201308.json` dosyasını proje ana dizinine koyun.

### 4. Uygulamayı Başlatın

```bash
python app.py
```

### 5. Tarayıcınızda Açın

```
http://127.0.0.1:5000
```


## 🛠️ Kullanılan Teknolojiler

- **Backend:** Flask (Python)
- **AI:** Groq API (qwen/qwen3-32b model)
- **Frontend:** HTML, CSS, JavaScript
- **Veritabanı:** JSON

## ⚙️ Özellikler

- Doğal dil işleme ile nota çıkarımı
- Akıllı eşleştirme algoritması
- Benzerlik skorlaması
- Sayfalama ile performans optimizasyonu
- Modern ve kullanıcı dostu arayüz

## 👥 Geliştirici Ekibi

- [@cerennceyhan](https://github.com/cerennceyhan)
- [@ilaydabalal](https://github.com/ilaydabalal)
