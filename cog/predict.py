import cog
from cog import BaseModel, BasePredictor, Input, Path, File
from typing import Dict
from pathlib import Path
import tempfile
import torch
import torchaudio
import librosa
import subprocess
import os
import soundfile as sf
from scipy.io.wavfile import write as write_wav
from pydub import AudioSegment

SAMPLE_RATE = 16000
device = "cpu"
if torch.cuda.is_available():
    device = "cuda"
elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
    device = "mps"
print(f"Mars5 device: {device}")


class Predictor(cog.BasePredictor):
    def setup(self):
        self.mars5, self.config_class = torch.hub.load(
            'Camb-ai/mars5-tts', 'mars5_english',  device=device, trust_repo=True)
        print(">>>>> Model Loaded")

    def predict(
        self,
        testMode: str = cog.Input(
            description="Run in test mode (without inference)", choices=["true", "false"], default="false"),
        text: str = cog.Input(description="Text to synthesize", default="Hi there, I'm your new voice clone, powered by Mars5."),
        ref_audio_file: cog.Path = cog.Input(
            description='Reference audio file to clone from <= 10 seconds', default="https://replicate.delivery/pbxt/L9a6SelzU0B2DIWeNpkNR0CKForWSbkswoUP69L0NLjLswVV/voice_sample.wav"),
        ref_audio_transcript: str = cog.Input(
            description='Text in the reference audio file', default="Hi there. I'm your new voice clone. Try your best to upload quality audio.")
    ) -> cog.Path:

        if (testMode == 'false'):
            # Load the reference audio
            wav, sr = librosa.load(ref_audio_file, sr=self.mars5.sr, mono=True)
            wav = torch.from_numpy(wav)

            # configuration for the TTS model
            deep_clone = True
            cfg = self.config_class(
                deep_clone=deep_clone, rep_penalty_window=100, top_k=100, temperature=0.7, freq_penalty=3)

            # Generate the synthesized audio
            print(f">>> Running inference")
            ar_codes, wav_out = self.mars5.tts(
                text, wav, ref_audio_transcript, cfg=cfg)
            print(f">>>>> Done with inference")

            output_path = Path(tempfile.mkdtemp()) / "output.wav"
            mp3_output_path = Path(tempfile.mkdtemp()) / "output.mp3"

            write_wav(output_path, self.mars5.sr, wav_out.numpy())

            # now convert the file stored at output_path to mp3
            compressed = AudioSegment.from_wav(output_path)
            compressed.export(mp3_output_path)
            output = mp3_output_path
        if (testMode == 'true'):
            output = Path(os.getcwd() + "/voice_sample.wav")            

        return cog.Path(output)
