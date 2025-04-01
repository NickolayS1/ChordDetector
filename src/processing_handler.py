from typing import Dict, List, Tuple
import numpy as np
from chord_recognizer import ChordRecognizer


class ProcessingHandler:
    """Processes audio signals for chord recognition and frequency analysis."""

    # Class-level constants
    NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    MIDI_RANGE = (28, 76)  # D2 (28) to E6 (76)
    A4_FREQUENCY = 440.0
    D2_THRESHOLD = 73.0  # Minimum frequency for analysis

    def __init__(self,
                 sample_rate: int = 44100,
                 magnitude_threshold: float = 40.0,
                 top_n_peaks: int = 300):
        """
        Initialize audio processor with analysis parameters.

        Args:
            sample_rate: Audio sampling rate (default: 44100 Hz)
            magnitude_threshold: Minimum magnitude for peak consideration
            top_n_peaks: Maximum number of frequency peaks to analyze
        """
        self.sample_rate = sample_rate
        self.magnitude_threshold = magnitude_threshold
        self.top_n_peaks = top_n_peaks

    def analyze_audio(self, audio_data: np.ndarray) -> List[Tuple[str, float]]:
        """
        Full analysis pipeline for chord recognition.

        Args:
            audio_data: Mono audio signal array

        Returns:
            List of (chord_name, error) tuples
        """
        frequencies, spectrum = self._perform_fft(audio_data)
        peaks_freq, peaks_mag = self._detect_significant_peaks(frequencies, spectrum)
        note_profile = self._create_note_profile(peaks_freq, peaks_mag)
        root_candidates = self._find_root_candidates(note_profile)
        chromatic_vector = self._build_chromatic_vector(note_profile)

        recognizer = ChordRecognizer()
        return self._match_chords(root_candidates, chromatic_vector, recognizer)

    def _perform_fft(self, audio_data: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Perform FFT analysis and return frequency bins and spectrum."""
        fft_result = np.fft.fft(audio_data)
        frequencies = np.fft.fftfreq(len(audio_data), 1 / self.sample_rate)
        return frequencies, fft_result

    def _detect_significant_peaks(self,
                                  frequencies: np.ndarray,
                                  spectrum: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Identify significant frequency peaks above threshold."""
        magnitudes = np.abs(spectrum)
        valid_mask = (frequencies >= self.D2_THRESHOLD) & (magnitudes > self.magnitude_threshold)

        valid_freqs = frequencies[valid_mask]
        valid_mags = magnitudes[valid_mask]

        sort_indices = np.argsort(valid_mags)[::-1]
        return valid_freqs[sort_indices[:self.top_n_peaks]], valid_mags[sort_indices[:self.top_n_peaks]]

    def _frequency_to_note(self, frequency: float) -> str:
        """Convert frequency to musical note notation (e.g., 'A4')."""
        note_number = 12 * np.log2(frequency / self.A4_FREQUENCY) + 69
        note_number = int(np.round(note_number))
        return f"{self.NOTES[note_number % 12]}{note_number // 12 - 1}"

    def _create_note_profile(self, frequencies: np.ndarray, magnitudes: np.ndarray) -> Dict[str, float]:
        """Create normalized note magnitude profile."""
        note_profile = {note: 0.0 for note in self.NOTES}

        for freq, mag in zip(frequencies, magnitudes):
            note = self._frequency_to_note(freq)[:-1]  # Remove octave
            if note in note_profile:
                note_profile[note] += mag

        total = sum(note_profile.values())
        return {note: mag / total for note, mag in note_profile.items()} if total > 0 else note_profile

    def _find_root_candidates(self, note_profile: Dict[str, float],
                              threshold: float = 0.1) -> List[str]:
        """Identify top 3 root note candidates based on magnitude."""
        filtered = {note: mag for note, mag in note_profile.items() if mag > threshold}
        sorted_notes = sorted(filtered.items(), key=lambda x: (-x[1], x[0]))
        return [note for note, _ in sorted_notes[:3]]

    def _build_chromatic_vector(self, note_profile: Dict[str, float]) -> Dict[str, float]:
        """Construct and normalize chromatic vector with adjustments."""
        chromatic = {note: 0.0 for note in self.NOTES}
        for note, mag in note_profile.items():
            if note in chromatic:
                chromatic[note] += mag


        total = sum(chromatic.values())
        return {note: mag / total for note, mag in chromatic.items()} if total > 0 else chromatic

    def _match_chords(self,
                      root_candidates: List[str],
                      chromatic_vector: Dict[str, float],
                      recognizer: 'ChordRecognizer') -> List[Tuple[str, float]]:
        """Match chromatic vector to chords for each root candidate. Sorts by confidence."""
        results = []
        for root in root_candidates:
            chord, error = recognizer.find_chord(root, chromatic_vector)
            results.append((chord, error))
        results.sort(key=lambda x: x[1])
        return results
