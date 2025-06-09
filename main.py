from fastapi import FastAPI, HTTPException
from piper_infer import PiperTTS
from pydantic import BaseModel

app = FastAPI()

MODEL_PATH = "models/pt_BR/pt_BR-edresson-low.onnx"
CONFIG_PATH = "models/pt_BR/pt_BR-edresson-low.onnx.json"

tts = PiperTTS(MODEL_PATH, CONFIG_PATH)

class TTSRequest(BaseModel):
    text: str

@app.post("/tts")
def tts_api(req: TTSRequest):
    text = req.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Missing 'text' field")
    try:
        audio_path = tts.synthesize(text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS synthesis failed: {str(e)}")
    return {
        "audio_file": audio_path
    }






