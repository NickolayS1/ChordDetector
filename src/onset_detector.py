import numpy as np
from typing import Optional, List


class OnsetDetector:
    def __init__(self,
                 sample_rate: int = 44100,
                 hop_size: int = 1102,
                 min_magnitude: float = 0.012,
                 duration: float = 0.25,
                 threshold: float = 0.5,
                 frame_size: int = 2205) -> None:
        """
        Onset detection system for audio signals.

        Args:
            sample_rate: Sampling rate in Hz (default: 44100)
            hop_size: Number of samples between frames (default: 1102 ≈ 50% overlap)
            min_magnitude: Minimum magnitude threshold for valid onsets (default: 0.012)
            duration: Analysis window duration in seconds (default: 0.25s)
            threshold: Energy difference threshold for onset detection (default: 0.5)
            frame_size: Number of samples per frame (default: 2205 ≈ 50ms)
        """
        self.sample_rate: int = sample_rate
        self.threshold: float = threshold
        self.hop_size: int = hop_size
        self.frame_size: int = frame_size
        self.buffer_size: int = int(sample_rate * duration)
        self.min_magnitude: float = min_magnitude

    def compute_energy(self, frame: np.ndarray) -> float:
        """
        Calculate energy of a signal frame.

        Args:
            frame: Audio signal segment

        Returns:
            Energy value (sum of squared samples)
        """
        return float(np.sum(frame ** 2))

    def detect_onset(self, audio_data: np.ndarray) -> Optional[int]:
        """
        Detect first valid onset in audio signal.

        Args:
            audio_data: Mono audio signal array

        Returns:
            Sample index of first valid onset, or None if not found
        """
        # Frame the audio signal
        frames: List[np.ndarray] = []
        for i in range(0, min(self.buffer_size - self.frame_size + 1, len(audio_data)), self.hop_size):
            frame = audio_data[i:i + self.frame_size]
            frames.append(frame)

        # Compute frame energies
        energies: List[float] = [self.compute_energy(frame) for frame in frames]

        # Detect candidate onsets
        onset_frames: List[int] = []
        for i in range(1, len(energies)):
            if (energies[i] - energies[i - 1]) > self.threshold:
                onset_frames.append(i)

        # Validate onsets with magnitude check
        window_size: int = 220  # ~10ms window at 44.1kHz
        for frame_idx in onset_frames:
            center_sample = frame_idx * self.hop_size + self.frame_size // 2
            start = max(0, center_sample - window_size // 2)
            end = min(len(audio_data), center_sample + window_size // 2)

            window: np.ndarray = audio_data[start:end]
            magnitude: float = np.mean(np.abs(window))

            if magnitude > self.min_magnitude:
                return center_sample  # Return first valid onset

        return None
