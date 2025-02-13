from flask import Flask, render_template, request, jsonify, session
import cv2
import numpy as np
import face_recognition
import base64
import json
from models.database import save_user, verify_user

app = Flask(__name__)
app.secret_key = 'super_secret_key'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        image_data = data.get('image')

        if not image_data:
            return jsonify({"success": False, "message": "Aucune image reçue"}), 400

        # Convertir l'image Base64 en numpy array
        image_bytes = base64.b64decode(image_data.split(',')[1])
        np_arr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        # Encoder le visage
        encodings = face_recognition.face_encodings(img)
        if encodings:
            save_user(username, password, encodings[0])  # Sauvegarde l'encodage facial
            return jsonify({"success": True, "message": "Inscription réussie"}), 200
        else:
            return jsonify({"success": False, "message": "Aucun visage détecté"}), 400

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        image_data = data.get('image')

        if not image_data:
            return jsonify({"success": False, "message": "Aucune image reçue"}), 400

        # Convertir l'image Base64 en numpy array
        image_bytes = base64.b64decode(image_data.split(',')[1])
        np_arr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        # Encoder le visage
        encodings = face_recognition.face_encodings(img)
        if not encodings:
            return jsonify({"success": False, "message": "Aucun visage détecté"}), 400

        # Vérifier utilisateur en passant seulement username et password
        valid_password, stored_encoding = verify_user(username, password)

        if not valid_password:
            return jsonify({"success": False, "message": "Mot de passe incorrect"}), 401

        if stored_encoding is None:
            return jsonify({"success": False, "message": "Utilisateur non trouvé"}), 404

        # Comparer l'encodage du visage
        matches = face_recognition.compare_faces([stored_encoding], encodings[0])

        if matches[0]:
            session['user'] = username
            return jsonify({"success": True, "message": "Connexion réussie"}), 200
        else:
            return jsonify({"success": False, "message": "Visage non reconnu"}), 401

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return f"Bienvenue {session['user']} !"
    return "Accès refusé, veuillez vous connecter."

@app.route('/logout')
def logout():
    session.pop('user', None)
    return "Déconnecté avec succès."

if __name__ == '__main__':
    app.run(debug=True)
