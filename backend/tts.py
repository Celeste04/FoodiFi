from TTS.api import TTS
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device=device)

def get_tts(text : str):
    output_file = "audio/output.wav"
    tts.tts_to_file(text=text, speaker_wav="audio/speaker_me.wav", language="en", file_path=output_file)
    return output_file
    