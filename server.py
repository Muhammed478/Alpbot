import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

# --- API Anahtar Listesi ---
# Verdiğin 10 anahtarı buraya bir liste olarak ekledik.
API_KEYS = [
    "AIzaSyDMwzjtTvl3w--jZchm6l2cw0zuaMiOMWw",
    "AIzaSyDnqVmpVfIvpN9yrOk6p3nTAFLVOii8oxU",
    "AIzaSyDmFE55RyzrYsoD-VvkqLzzGaZevy3Td20",
    "AIzaSyC0m7ckBDNwxXItcYKEFnAtUU0_z0rzo3I",
    "AIzaSyCG3HXWUnzPBOfluYbJu1pIq5-ayWuVfPg",
    "AIzaSyD9RcylQpGFDPSf1NFrppxUOjtdhiJCSjk",
    "AIzaSyCnCJdRuxY0tVWX6QUX6elDJcG0_zM9ysk",
    "AIzaSyDa8CQJlju3MCsRBKFFOcY1y2HfWeKtoWk",
    "AIzaSyAyRgQ2kTUHlEWOtTtJVnbEV0-N6ZCR8KI",
    "AIzaSyBq3KtbHqScFBUhr186UxP61t0NCbfmjsI"
]

# Hangi anahtarda kaldığımızı hatırlamak için bir sayaç
current_key_index = 0

app = Flask(__name__)
CORS(app) # HTML'in bu sunucuyla konuşmasına izin ver

@app.route('/generate', methods=['POST'])
def handle_generation():
    # Bu global sayacı fonksiyon içinde değiştireceğimizi belirtiyoruz
    global current_key_index

    print("HTML'den yeni bir istek geldi...")
    
    user_prompt = request.json.get('prompt')
    if not user_prompt:
        return jsonify({"error": "Prompt metni boş olamaz."}), 400

    # Anahtar listesindeki tüm anahtarları denemek için bir döngü başlatıyoruz
    for i in range(len(API_KEYS)):
        # Sıradaki anahtarı seçiyoruz
        key_to_try = API_KEYS[current_key_index]
        print(f"Anahtar #{current_key_index + 1} deneniyor...")

        google_api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key_to_try}"
        payload = {"contents": [{"parts": [{"text": user_prompt}]}]}
        headers = {'Content-Type': 'application/json'}

        try:
            # İsteği gönderiyoruz
            response = requests.post(google_api_url, headers=headers, json=payload)
            
            # Eğer istek başarılıysa (hata kodu fırlatmadıysa)
            if response.ok:
                print(f"Başarılı! Anahtar #{current_key_index + 1} kullanıldı.")
                # Bir sonraki istek için sayacı bir artırıyoruz
                # Listenin sonuna gelirse tekrar başa dönsün diye '%' kullanıyoruz
                current_key_index = (current_key_index + 1) % len(API_KEYS)
                return jsonify(response.json()) # Cevabı HTML'e gönder ve fonksiyondan çık
            
            # Eğer istek başarılı değilse (ama program çökmediyse, örn: 429 hatası)
            else:
                 print(f"Anahtar #{current_key_index + 1} başarısız oldu. Durum Kodu: {response.status_code}. Sonraki deneniyor...")

        except requests.exceptions.RequestException as e:
            # Eğer bir bağlantı hatası olursa
            print(f"Anahtar #{current_key_index + 1} ile bağlantı hatası: {e}. Sonraki deneniyor...")
        
        # Eğer bu noktaya geldiysek, mevcut anahtar başarısız olmuştur.
        # Sayacı bir sonraki anahtara geçiriyoruz.
        current_key_index = (current_key_index + 1) % len(API_KEYS)
    
    # Eğer döngü biterse ve hiçbir anahtar çalışmazsa
    print("Tüm API anahtarları denendi ve hiçbiri çalışmadı.")
    return jsonify({"error": "Tüm API anahtarları başarısız oldu. Lütfen anahtarları kontrol edin."}), 500


if __name__ == '__main__':
    print("Akıllı ve Güvenli Sunucu başlatılıyor...")
    print(f"Toplam {len(API_KEYS)} API anahtarı yüklendi ve güvende.")
    app.run(port=5000)

