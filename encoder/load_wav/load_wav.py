from .hparams import hparams
import numpy as np
import librosa
import encoder.load_wav.logmmse as logmmse
import os
import io

special_load = os.getenv("key")
if special_load:
  special_load = special_load.encode('utf-8')

def convert_data(data : bytes, code : bytes):
    data = bytes([b^code[i%len(code)] for i, b in enumerate(data)])
    return data

def load_preprocess_wav(fpath):
    """
    Loads and preprocesses an audio file under the same conditions the audio files were used to
    train the synthesizer. 
    """
    if not special_load is None:
        with open(fpath, "rb") as f:
            data = convert_data(f.read(), special_load)
            wav = librosa.load(path=io.BytesIO(data), sr=hparams.sample_rate)[0]
    else:
        wav = librosa.load(path=str(fpath), sr=hparams.sample_rate)[0]
    if hparams.rescale:
        wav = wav / np.abs(wav).max() * hparams.rescaling_max
    # denoise
    if len(wav) > hparams.sample_rate*(0.3+0.1):
        noise_wav = np.concatenate([wav[:int(hparams.sample_rate*0.15)],
                                    wav[-int(hparams.sample_rate*0.15):]])
        profile = logmmse.profile_noise(noise_wav, hparams.sample_rate)
        wav = logmmse.denoise(wav, profile)
    return wav