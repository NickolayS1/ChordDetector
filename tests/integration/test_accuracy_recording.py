import os
import time
import soundfile as sf
import numpy as np
import pytest

from src.processing_handler import ProcessingHandler


@pytest.fixture
def processor():
    return ProcessingHandler()


def test_chord_accuracy(processor):
    test_dir = "data/chord_sounds"
    total = 0
    correct = 0
    total_error = 0.0
    total_time = 0.0

    print('\nTest info')
    for filename in os.listdir(test_dir):
        if filename.endswith(".wav"):
            guitar_type = 'classical'
            expected_chord = (os.path.splitext(filename)[0].split("_"))[0]
            if len(os.path.splitext(filename)[0].split("_") ) > 1:
                guitar_type = (os.path.splitext(filename)[0].split("_"))[1]
            filepath = os.path.join(test_dir, filename)

            # Load and process audio
            audio, _ = sf.read(filepath)
            if audio.ndim > 1:
                audio = np.mean(audio, axis=1)

            start_time = time.time()
            results = processor.analyze_audio(audio)
            processing_time = time.time() - start_time
            for chord, error in results:
                if chord == expected_chord:
                    correct += 1
                    total_error += error
                    print(f"Got {chord}, expected {expected_chord}. Guitar type = {guitar_type}")
                    break
            else:
                print(f"Got {results[0][0]}, expected {expected_chord}. Guitar type = {guitar_type}")
            total += 1
            total_time += processing_time

    accuracy = correct / total if total > 0 else 0
    avg_error = total_error / total if total > 0 else 0
    avg_time = total_time / total if total > 0 else 0

    print(f"\nAccuracy: {accuracy * 100:.1f}%")
    print(f"Average Error: {avg_error:.3f}")
    print(f"Average Processing Time: {avg_time:.5f}s")
    assert accuracy > 0.6
