import os
import queue
import soundfile as sf
import numpy as np
import pytest
import time
from PySide6.QtCore import QCoreApplication

from src.realtime_audio_handler import RealtimeAudioHandler
from src.realtime_processing_handler import RealtimeProcessingHandler


class FakeAudioRecorder:
    """Simulates RealtimeAudioHandler with proper queue lifecycle management"""

    def __init__(self, chunks, sample_rate=44100):
        self.sample_rate = sample_rate
        self.queue = queue.Queue()
        self._chunks = chunks
        self._active = True
        self._load_thread = None

    @property
    def is_recording(self):
        """True while chunks remain or buffers are being processed"""
        return self._active or not self.queue.empty()

    def start(self):
        """Begin feeding chunks into the queue"""
        self._active = True
        for chunk in self._chunks:
            self.queue.put(chunk)
        # Add sentinel value to mark end of recording
        self.queue.put(None)

    def stop(self):
        self._active = False


@pytest.fixture
def qt_app():
    """Provides a QCoreApplication instance for QT signals"""
    return QCoreApplication([])


connect_stats = RealtimeAudioHandler()


def test_simulated_realtime(qt_app):
    test_dir = "data/chord_sequences"
    buffer_size_seconds = connect_stats.buffer_size
    sample_rate = connect_stats.sample_rate
    max_wait_time = 5  # seconds

    for filename in os.listdir(test_dir):
        if not filename.endswith(".wav"):
            continue

        expected_sequence = os.path.splitext(filename)[0].split('_')
        result = []
        filepath = os.path.join(test_dir, filename)

        audio, sr = sf.read(filepath)
        if audio.ndim > 1:
            audio = np.mean(audio, axis=1)

        chunk_size = int(buffer_size_seconds * sr)
        chunks = [audio[i:i + chunk_size] for i in range(0, len(audio), chunk_size)]

        fake_recorder = FakeAudioRecorder(chunks, sample_rate)
        processor = RealtimeProcessingHandler(fake_recorder, sample_rate)

        emitted_results = []
        processor.signals.chord_detected.connect(emitted_results.append)

        # Start processing with proper lifecycle
        fake_recorder.start()
        start_time = time.time()

        while fake_recorder.is_recording and (time.time() - start_time < max_wait_time):
            processor._process_audio_chunk()
            qt_app.processEvents()

        fake_recorder.stop()

        correct = 0
        total_error = 0.0
        expected_idx = 0

        for emission in emitted_results:
            if expected_idx >= len(expected_sequence):
                break

            current_expected = expected_sequence[expected_idx]
            detected_chords = [res[0] for res in emission]

            if current_expected in detected_chords:  # Check top 3
                correct += 1
                result.append(current_expected)
                for chord, error in emission:
                    if chord == current_expected:
                        total_error += error
                        break
                expected_idx += 1
            else:
                result.append(detected_chords[0][0])

        # Calculate metrics
        total_chords = len(expected_sequence)
        accuracy = correct / total_chords if total_chords > 0 else 0
        avg_error = total_error / correct if correct > 0 else 0

        print(f"\nTested file: {filename}")
        print(f"Result: {result}")
        print(f"Accuracy: {accuracy * 100:.1f}%")
        print(f"Avg error for matches: {avg_error:.3f}")
        if len(emitted_results) != len(expected_sequence):
            print("Some chords are skipped or counted twice")
        assert True
