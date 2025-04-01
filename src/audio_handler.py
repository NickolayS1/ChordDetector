import sounddevice as sd
import numpy as np
import soundfile as sf
from scipy.signal import resample
from typing import Union
from src.logger_config import *


class AudioHandler:
    """Handles audio recording, playback, importing, and exporting."""

    def __init__(self, sample_rate: int = 44100, duration: float = 1.0, device: Union[int, str] = 0):
        """
        Initialize AudioHandler with audio parameters.

        Args:
            sample_rate: Sampling rate in Hz (default: 44100)
            duration: Recording duration in seconds (default: 1.0)
            device: Audio device index or name (default: 0)
        """
        self.sample_rate = sample_rate
        self.duration = duration
        self.device = device

    def record_audio(self) -> np.ndarray:
        """Record audio and return normalized float32 numpy array."""
        logging.info(f"Recording for {self.duration} seconds...")
        recording = sd.rec(
            int(self.sample_rate * self.duration),
            samplerate=self.sample_rate,
            channels=1,
            device=self.device,
            dtype='float32'
        )
        sd.wait()
        audio_data = recording.flatten()
        audio_data = self.normalize_audio(audio_data)
        self._log_audio_stats(audio_data)
        return audio_data

    def play_audio(self, audio_data: np.ndarray) -> None:
        """Play audio data using the instance's sample rate."""
        logging.info(f"Playing current recording")
        sd.play(audio_data, samplerate=self.sample_rate)
        sd.wait()

    def import_audio(self, file_path: str) -> np.ndarray:
        """Import and process audio file (WAV format supported)."""
        logging.info(f"Importing from {file_path}")
        audio_data, original_sr = sf.read(file_path, dtype='float32')

        # Convert to mono if stereo
        if audio_data.ndim > 1:
            audio_data = np.mean(audio_data, axis=1)

        # Resample if needed
        if original_sr != self.sample_rate:
            num_samples = int(len(audio_data) * self.sample_rate / original_sr)
            audio_data = resample(audio_data, num_samples)

        audio_data = self.normalize_audio(audio_data)
        self._log_audio_stats(audio_data)
        return audio_data

    def export_audio(self, audio_data: np.ndarray, file_path: str) -> None:
        """Export audio data to WAV file with proper validation."""
        file_path = self._validate_file_extension(file_path)
        sf.write(file_path, audio_data, self.sample_rate)
        logging.info(f"Exported audio to {file_path}")

    def normalize_audio(self, audio_data: np.ndarray) -> np.ndarray:
        """Normalize audio to [-1, 1] range."""
        max_amp = np.max(np.abs(audio_data))
        if max_amp > 1e-8:  # Avoid division by zero
            audio_data = audio_data / max_amp
        return audio_data

    @staticmethod
    def _validate_file_extension(file_path: str) -> str:
        """Ensure file has .wav extension."""
        if not file_path.lower().endswith('.wav'):
            return f"{file_path}.wav"
        return file_path

    @staticmethod
    def _log_audio_stats(audio_data: np.ndarray) -> None:
        """Print audio statistics for debugging."""
        logging.debug(f"Audio stats - "
                      f"Max: {np.max(audio_data):.2f}, "
                      f"Min: {np.min(audio_data):.2f}, "
                      f"Mean: {np.mean(audio_data):.2f}")
