import os
import json
import uuid
from flask import Flask, render_template, request, session, jsonify
from google import genai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "clave-secreta-super-segura")

API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

DATA_FILE = "chats.json"

def load_chats():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_chats(chats):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(chats, f, indent=2, ensure_ascii=False)

@app.route('/')
def index():
    chat_id = session.get("chat_id")
    chats = load_chats()
    history = chats.get(chat_id, []) if chat_id else []
    return render_template('index.html', chat_id=chat_id, history=history)

@app.route('/chat/select/all', methods=['GET'])
def get_all_chats():
    chats = load_chats()
    return jsonify(chats)

@app.route('/chat/select/<chat_id>', methods=['GET'])
def select_chat(chat_id):
    chats = load_chats()
    if chat_id in chats:
        return jsonify(chats[chat_id])
    return jsonify([]), 404

@app.route('/chat/new', methods=['POST'])
def new_chat():
    chat_id = str(uuid.uuid4())
    session['chat_id'] = chat_id  # guardamos solo el id en sesión

    chats = load_chats()
    chats[chat_id] = []
    save_chats(chats)
    return jsonify({"chat_id": chat_id})

@app.route('/chat/send/<chat_id>', methods=['POST'])
def send_message(chat_id):
    prompt = request.json.get('prompt')
    chats = load_chats()

    if chat_id not in chats:
        chats[chat_id] = []

    chats[chat_id].append({"role": "user", "content": prompt})

    try:
        contents = [msg['content'] for msg in chats[chat_id]]
        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=contents
        )
        respuesta_texto = response.text
    except Exception as e:
        respuesta_texto = f"Error: {str(e)}"

    chats[chat_id].append({"role": "bot", "content": respuesta_texto})

    save_chats(chats)

    return jsonify(chats[chat_id])

if __name__ == '__main__':
    app.run(debug=True)
