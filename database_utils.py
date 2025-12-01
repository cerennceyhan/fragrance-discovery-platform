import json
from config import Config

# Veritabanını yükle
def load_perfume_database():
    """Veritabanı JSON dosyasını yükler."""
    path = Config.PERFUME_DATABASE_PATH
    try:
        with open(path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"HATA: Veritabanı dosyası bulunamadı: {path}")
        return []
    except Exception as e:
        print(f"HATA: Veritabanı yüklenirken hata: {e}")
        return []

# Notaları normalize et
def normalize_note(note):
    """Parfüm notalarını küçük harfe dönüştürür ve noktalama işaretlerini kaldırır."""
    return note.lower().strip().replace(',', '').replace('.', '')

# Eşleşen notaları renklendir
def highlight_matching_notes(notes_list, user_notes):
    """
    Parfüm notaları listesindeki, kullanıcının aradığı notaları HTML ile vurgular.
    """
    if not notes_list:
        return 'Belirtilmemiş'
    
    user_notes_normalized = [normalize_note(note) for note in user_notes]
    highlighted_notes = []
    
    for note in notes_list:
        note_normalized = normalize_note(note)
        matched = False
        
        for user_note in user_notes_normalized:
            # Tam eşleşme veya içerikte geçme kontrolü
            if user_note in note_normalized or note_normalized in user_note:
                matched = True
                break
        
        if matched:
            highlighted_notes.append(f'<span style="color: red; font-weight: bold;">{note}</span>')
        else:
            highlighted_notes.append(note)
    
    return ', '.join(highlighted_notes)

# Benzerlik hesapla
def calculate_similarity(user_notes, perfume):
    """
    Kullanıcı notları ile parfüm notaları arasındaki benzerliği hesaplar.
    (Artık sadece İngilizce notalar beklenir ve Türkçe çeviri kontrolü kaldırılmıştır.)
    """
    user_notes_normalized = [normalize_note(note) for note in user_notes]
    perfume_notes_normalized = [normalize_note(note) for note in perfume['all_notes']]
    
    common_notes = set()
    
    for user_note in user_notes_normalized:
        for perfume_note in perfume_notes_normalized:
            # Sadeleştirilmiş İngilizce Eşleşme (tam eşleşme ve içerik eşleşmesi)
            # Türkçe-İngilizce çeviri kontrolü kaldırıldı.
            if user_note == perfume_note or \
               (user_note in perfume_note) or (perfume_note in user_note):
                common_notes.add(user_note)
                break  # Bu notanın birden fazla kez sayılmasını engelle

    matched_count = len(common_notes)
    total_count = len(user_notes_normalized)
    
    if total_count == 0:
        return 0, 0, 0
    
    similarity_score = matched_count / total_count
    return similarity_score, matched_count, total_count

# Eşleşen parfümleri bul
def find_matching_perfumes(user_notes, database):
    """
    Verilen notalara göre veritabanındaki parfümleri puanlar ve en iyi eşleşenleri döndürür.
    """
    scored_perfumes = []
    
    for perfume in database:
        similarity, matched, total = calculate_similarity(user_notes, perfume)
        if similarity > 0:
            scored_perfumes.append((perfume, similarity, matched, total))
    
    # Benzerlik puanına göre sırala
    scored_perfumes.sort(key=lambda x: x[1], reverse=True)
    return scored_perfumes