import os
import hashlib
from flask import Flask, request, jsonify, send_file
import subprocess

app = Flask(__name__)

MODEL_PATH = "models/pt_BR/pt_BR-edresson-low.onnx"
CONFIG_PATH = "models/pt_BR/pt_BR-edresson-low.onnx.json"
AUDIO_CACHE_DIR = "audio_cache"
os.makedirs(AUDIO_CACHE_DIR, exist_ok=True)

def text_to_filename(text):
    # Cria um hash MD5 do texto para nomear o arquivo
    return hashlib.md5(text.encode('utf-8')).hexdigest() + ".wav"

@app.route("/tts", methods=["POST"])
def tts():
    data = request.json
    text = data.get("text")
    if not text:
        return jsonify({"error": "Missing 'text'"}), 400

    audio_file = os.path.join(AUDIO_CACHE_DIR, text_to_filename(text))

    if not os.path.exists(audio_file):
        # Se o áudio não existir, gera ele com o Piper
        command = [
            "python3", "piper/piper.py",
            "--model", MODEL_PATH,
            "--config", CONFIG_PATH,
            "--output_file", audio_file
        ]

        try:
            subprocess.run(command, input=text.encode(), check=True)
        except subprocess.CalledProcessError as e:
            return jsonify({"error": "Piper failed", "details": str(e)}), 500

    # Retorna o arquivo já gerado/cached
    return send_file(audio_file, mimetype="audio/wav")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


