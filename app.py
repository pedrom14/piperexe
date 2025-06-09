import os
import hashlib
from flask import Flask, request, jsonify, send_file
import subprocess

app = Flask(__name__)

# Caminhos dos modelos
MODEL_PATH = "models/pt_BR/pt_BR-edresson-low.onnx"
CONFIG_PATH = "models/pt_BR/pt_BR-edresson-low.onnx.json"

# Diretório onde os áudios serão salvos
AUDIO_CACHE_DIR = "audio_cache"
os.makedirs(AUDIO_CACHE_DIR, exist_ok=True)

# Função para transformar o texto em um nome de arquivo
def text_to_filename(text):
    return hashlib.md5(text.encode('utf-8')).hexdigest() + ".wav"

@app.route("/tts", methods=["POST"])
def tts():
    data = request.json
    text = data.get("text")
    
    if not text:
        return jsonify({"error": "Missing 'text'"}), 400

    audio_file = os.path.join(AUDIO_CACHE_DIR, text_to_filename(text))

    # Se o áudio ainda não existir, gera com o Piper
    if not os.path.exists(audio_file):
        command = [
            "python3", "piper/piper.py",
            "--model", MODEL_PATH,
            "--config", CONFIG_PATH,
            "--output_file", audio_file
        ]

        try:
            result = subprocess.run(
                command,
                input=text.encode(),
                capture_output=True,
                text=True,
                check=True
            )
        except subprocess.CalledProcessError as e:
            return jsonify({
                "error": "Piper failed",
                "details": e.stderr  # Mostra o erro real do Piper
            }), 500

    # Retorna o áudio já gerado
    return send_file(audio_file, mimetype="audio/wav")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)




