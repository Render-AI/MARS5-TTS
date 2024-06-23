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
        text: str = cog.Input(description="Text to synthesize"),
        ref_audio_file: cog.Path = cog.Input(
            description='Reference audio file to clone from <= 10 seconds', default="https://www.renderai.com/audio/examples/bob-example-1.mp3"),
        ref_audio_transcript: str = cog.Input(
            description='Text in the reference audio file', default="Space: the final frontier. These are the voyages of the starship enterprise. It's five year misssion: to explore strange new worlds; to seek out new life and new civilizations; to boldly go where no man has gone before.")
    ) -> File:

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

            write_wav('output.wav', self.mars5.sr, wav_out.numpy())

            # now convert the file stored at output_path to mp3
            compressed = AudioSegment.from_wav('output.wav')
            compressed.export("output.mp3")
            output = 'output.mp3'
        if (testMode == 'true'):
            output = 'voice_sample.wav'

        return File(output)
