import requests
import json
import time
from datetime import datetime

# Konfigürasyon
API_URL = "http://127.0.0.1:5000/analyze_comment"
REVIEWS_FILE = "reviews.txt"
MODEL_NAME = "openai/gpt-oss-120b"  # Örnek: "llama-3.1-70b", "mixtral-8x7b", "gemma-7b" vb.
OUTPUT_FILE = f"analysis_results_{MODEL_NAME}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

def extract_perfume_count(response_data):
    """API yanıtından önerilen parfüm sayısını çıkarır"""
    if "perfumes" in response_data:
        return len(response_data["perfumes"])
    return 0

def extract_perfume_names(response_data):
    """API yanıtından parfüm isimlerini çıkarır"""
    perfume_names = []
    if "perfumes" in response_data:
        for perfume_html in response_data["perfumes"]:
            # HTML'den parfüm adını çıkar
            if "Perfume:" in perfume_html:
                start = perfume_html.find("Perfume:") + 9
                end = perfume_html.find("</div>", start)
                if end == -1:
                    end = perfume_html.find("\n", start)
                perfume_name = perfume_html[start:end].strip()
                perfume_names.append(perfume_name)
    return perfume_names

def extract_notes(response_data):
    """API yanıtından çıkarılan notaları alır"""
    notes = []
    if "notes_html" in response_data:
        notes_html = response_data["notes_html"]
        # HTML'den notaları çıkar
        if "<p>" in notes_html:
            start = notes_html.find("<p>") + 3
            end = notes_html.find("</p>", start)
            notes_text = notes_html[start:end].strip()
            if notes_text and notes_text != "No valid note information could be retrieved from AI.":
                notes = [note.strip() for note in notes_text.split(",")]
    return notes

def extract_similarity_scores(response_data):
    """Parfümlerin benzerlik skorlarını çıkarır"""
    scores = []
    if "perfumes" in response_data:
        for perfume_html in response_data["perfumes"]:
            if "Similarity:" in perfume_html:
                start = perfume_html.find("Similarity:") + 11
                end = perfume_html.find("</span>", start)
                score = perfume_html[start:end].strip()
                scores.append(score)
    return scores

def analyze_comment(comment_text):
    """Tek bir yorumu analiz eder"""
    try:
        response = requests.post(
            API_URL,
            json={"text": comment_text},
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"HTTP {response.status_code}: {response.text}"}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def process_reviews():
    """Tüm yorumları işler ve sonuçları toplar"""
    results = []
    
    # Reviews dosyasını oku
    try:
        with open(REVIEWS_FILE, 'r', encoding='utf-8') as f:
            reviews = f.readlines()
    except FileNotFoundError:
        print(f"❌ HATA: {REVIEWS_FILE} dosyası bulunamadı!")
        return
    
    total_reviews = len(reviews)
    print(f"📊 Toplam {total_reviews} yorum bulundu.")
    print(f"⏳ Analiz başlıyor...\n")
    
    # Her yorumu işle
    for idx, review in enumerate(reviews, 1):
        review = review.strip()
        if not review:
            continue
        
        print(f"[{idx}/{total_reviews}] İşleniyor: {review[:50]}...")
        
        # API'ye istek gönder
        response_data = analyze_comment(review)
        
        # Sonuçları yapılandır
        result = {
            "review_number": idx,
            "original_comment": review,
            "extracted_notes": extract_notes(response_data),
            "suggested_perfume_count": extract_perfume_count(response_data),
            "perfume_names": extract_perfume_names(response_data),
            "similarity_scores": extract_similarity_scores(response_data),
            "timestamp": datetime.now().isoformat()
        }
        
        # Hata varsa ekle
        if "error" in response_data:
            result["error"] = response_data["error"]
        
        results.append(result)
        
        # İlerleme raporu
        print(f"   ✓ Çıkarılan notalar: {', '.join(result['extracted_notes']) if result['extracted_notes'] else 'Yok'}")
        print(f"   ✓ Önerilen parfüm sayısı: {result['suggested_perfume_count']}")
        print()
        
        # Rate limiting için kısa bekleme
        time.sleep(0.5)
    
    # Sonuçları JSON dosyasına kaydet
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Analiz tamamlandı!")
    print(f"📁 Sonuçlar '{OUTPUT_FILE}' dosyasına kaydedildi.")
    
    # Özet istatistikler
    print("\n" + "="*50)
    print("📊 ÖZET İSTATİSTİKLER")
    print("="*50)
    print(f"Toplam analiz edilen yorum: {len(results)}")
    print(f"Toplam çıkarılan nota sayısı: {sum(len(r['extracted_notes']) for r in results)}")
    print(f"Toplam önerilen parfüm: {sum(r['suggested_perfume_count'] for r in results)}")
    print(f"Ortalama parfüm önerisi/yorum: {sum(r['suggested_perfume_count'] for r in results) / len(results):.2f}")
    
    # En çok önerilen parfümler (varsa)
    all_perfumes = []
    for r in results:
        all_perfumes.extend(r['perfume_names'])
    
    if all_perfumes:
        from collections import Counter
        top_perfumes = Counter(all_perfumes).most_common(5)
        print(f"\n🏆 En Çok Önerilen 5 Parfüm:")
        for perfume, count in top_perfumes:
            print(f"   {count}x - {perfume}")
    
    print("="*50)

if __name__ == "__main__":
    print("🚀 PerfumeAI Batch Analyzer")
    print("="*50)
    print(f"API URL: {API_URL}")
    print(f"Input: {REVIEWS_FILE}")
    print(f"Output: {OUTPUT_FILE}")
    print("="*50 + "\n")
    
    process_reviews()