import torch
import soundfile as sf
from TTS.tts.models.vits import Vits
from TTS.utils.audio import AudioProcessor
from TTS.utils.io import load_config
import os
import hashlib

class PiperTTS:
    def __init__(self, model_path, config_path):
        self.config = load_config(config_path)
        self.model = Vits.init_from_config(self.config)
        cp = torch.load(model_path, map_location=torch.device("cpu"))
        self.model.load_state_dict(cp["model"])
        self.model.eval()
        self.ap = AudioProcessor(**self.config.audio)
        self.cache_dir = "audio_cache"
        os.makedirs(self.cache_dir, exist_ok=True)

    def text_to_filename(self, text):
        return hashlib.md5(text.encode('utf-8')).hexdigest() + ".wav"

    def synthesize(self, text: str) -> str:
        filename = self.text_to_filename(text)
        filepath = os.path.join(self.cache_dir, filename)
        if os.path.exists(filepath):
            return filepath
        tokens = self.model.tokenizer.text_to_ids(text)
        tokens = torch.LongTensor(tokens).unsqueeze(0)
        with torch.no_grad():
            wav = self.model.inference(tokens)[0]
        wav = self.ap.inv_preemphasis(wav)
        wav = wav.cpu().numpy()
        sf.write(filepath, wav, self.ap.sample_rate)
        return filepath

