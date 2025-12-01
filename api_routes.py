# api_routes.py

from flask import Blueprint, request, jsonify
from groq import Groq  # OpenAI yerine Groq import ediyoruz
import json
import re

# config.py'den sadece gerekli olanı (anahtar ve database utility'leri) içeri aktar.
from config import Config
from database_utils import load_perfume_database, find_matching_perfumes, highlight_matching_notes

# Blueprint oluşturma: Rotaları organize etmenin Flask'taki yolu
api = Blueprint('api', __name__)

# 🔑 GROQ CLIENT BAŞLATMA
# client objesi, bu dosya yüklendiği anda Config'den alınan anahtarla başlatılır.
try:
    client = Groq(api_key=Config.GROQ_API_KEY)
except Exception as e:
    # Başlatma başarısız olursa, bir placeholder istemci kullanın veya loglayın.
    print(f"ERROR: Groq client could not be initialized globally: {e}") 
    client = None 

@api.route("/analyze_comment", methods=["POST"])
def analyze_comment():
    data = request.json
    text = data.get("text", "")

    # Eğer global client başlatılamadıysa hemen hata döndür
    if client is None:
        return jsonify({"reply": "<h3>Error</h3><p>Groq client could not be established during application startup.</p>"})
    
    if not text:
        return jsonify({"reply": "<h3>Error</h3><p>Please enter a comment.</p>"})
        
    try:
        # 1️⃣ Groq ile notaları çıkar (SADECE İNGİLİZCE)
        system_prompt = """You are a perfume expert. Analyze the user's comment.
Extract the perfume notes from the comment and return them **only in English**.
Your response format must be strictly JSON, containing no other text or explanation. For example:
{
  "notes": ["bergamot", "lavender", "vanilla"]
}
Note: If no notes are found in the text, return an empty list.
"""
        user_prompt = f"Extract perfume notes from this comment: {text}"

        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",  # Groq'ta kullanılabilir model
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=4096,
            temperature=0.6
        )

        raw_output = response.choices[0].message.content.strip()

        # 🧩 JSON yanıtı ayrıştır (SADECE İNGİLİZCE "notes" anahtarı bekleniyor)
        try:
            json_match = re.search(r'\{.*\}', raw_output, re.DOTALL)
            if json_match:
                notes_data = json.loads(json_match.group())
                user_notes_en = notes_data.get("notes", []) # Anahtar "notes" olarak değiştirildi
            else:
                user_notes_en = []
        except Exception as e:
            print(f"JSON Parsing Error: {e}")
            user_notes_en = []

        # 2️⃣ Veritabanını yükle
        database = load_perfume_database()
        if not database:
            return jsonify({"reply": "<h3>Error</h3><p>Perfume database could not be loaded.</p>"})

        # 3️⃣ İngilizce notalarla eşleşme yap
        if not user_notes_en:
             # Yanıt HTML'i İngilizce
             reply_html = f"""
            <h3>Extracted Notes:</h3>
            <p>No valid note information could be retrieved from AI.</p>
            <h3>Result:</h3>
            <p>No matching was performed because no perfume notes were extracted from your comment.</p>
            """
             return jsonify({"reply": reply_html})
        
        matching_perfumes = find_matching_perfumes(user_notes_en, database)

        # 4️⃣ Sonuçları hazırla
        if not matching_perfumes:
            # Yanıt HTML'i İngilizce
            reply_html = f"""
            <h3>Extracted Notes:</h3>
            <p>{', '.join(user_notes_en)}</p>
            <h3>Result:</h3>
            <p>Unfortunately, no perfumes matching the extracted notes were found.</p>
            """
            return jsonify({"reply": reply_html})
        else:
            # Başlangıç notları HTML'i İngilizce
            notes_html = f"""
            <h3>Extracted Notes:</h3>
            <p>{', '.join(user_notes_en)}</p>
            """

            # api_routes.py dosyasındaki 4. adımdaki döngüdeki bölümü bu kod ile değiştirin:

            perfume_items = []
            for perfume, similarity, matched, total in matching_perfumes:
                top_notes = highlight_matching_notes(perfume.get('top_notes', []), user_notes_en)
                heart_notes = highlight_matching_notes(perfume.get('heart_notes', []), user_notes_en)
                base_notes = highlight_matching_notes(perfume.get('base_notes', []), user_notes_en)
                all_notes = highlight_matching_notes(perfume.get('all_notes', []), user_notes_en)

                # Belirtilmemiş notları hariç tutmak için dinamik HTML oluşturma
                notes_rows_html = ""
                
                # Sadece 'Belirtilmemiş' DEĞİLSE ekle (database_utils.py'deki fonksiyondan geliyor)
                if top_notes != 'Belirtilmemiş':
                    notes_rows_html += f"""
                            <div class="note-row">
                                <span class="note-label">Top notes:</span>
                                <span class="note-value">{top_notes}</span>
                            </div>"""
                
                if heart_notes != 'Belirtilmemiş':
                    notes_rows_html += f"""
                            <div class="note-row">
                                <span class="note-label">Heart notes:</span>
                                <span class="note-value">{heart_notes}</span>
                            </div>"""
                
                if base_notes != 'Belirtilmemiş':
                    notes_rows_html += f"""
                            <div class="note-row">
                                <span class="note-label">Base notes:</span>
                                <span class="note-value">{base_notes}</span>
                            </div>"""
                
                # 'All Notes' satırı her zaman gösterilir (boş olsa bile 'Belirtilmemiş' yazar)
                # NOT: All Notes için de aynı kuralı uygulamak isterseniz 'Belirtilmemiş' kontrolünü ekleyin.
                # Varsayılan olarak All Notes'u göstermeye devam ediyoruz:
                notes_rows_html += f"""
                            <div class="note-row">
                                <span class="note-label">All Notes:</span>
                                <span class="note-value">{all_notes}</span>
                            </div>"""


                # Parfüm detay HTML'i İngilizce
                perfume_html = f"""
                <div class="perfume-item">
                    <div class="perfume-image">
                        <img src="/static/perfume.png" alt="Perfume">
                    </div>
                    <div class="perfume-content">
                        <div class="perfume-header">
                            <div class="perfume-title-section">
                                <div class="perfume-name">Perfume: {perfume.get('brand', 'Unknown')} - {perfume.get('fragrance', 'Unknown')}</div>
                            </div>
                            <span class="similarity-badge">Similarity: {matched}/{total}</span>
                        </div>
                        <div class="perfume-notes">
                            {notes_rows_html} 
                        </div>
                    </div>
                </div>
                """
                perfume_items.append(perfume_html)

            return jsonify({"notes_html": notes_html, "perfumes": perfume_items})

    except Exception as e:
        # Groq API hataları için genel hata yakalama
        reply_html = f"<h3>API Error Occurred</h3><p>{str(e)}</p>" 
        return jsonify({"reply": reply_html})