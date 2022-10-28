from pathlib import Path
import numpy as np
from .audio import load_wav_to_mel
from .inference import load_model
from .inference import embed_frames_batch

load_model(Path("./encoder/saved_models/pretrained.pt"), "cpu")

def generate_emb(path):
    mel = load_wav_to_mel(path)
    emb = embed_frames_batch(mel[None, ...])[0]
    np.save(path+".emb", emb)
