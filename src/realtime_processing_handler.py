import time
import numpy as np
from typing import List, Optional, Tuple, Type
from PySide6.QtCore import QObject, Signal

from src.chord_templates import chromatic_vectors
from src.chord_recognizer import ChordRecognizer
from src.onset_detector import OnsetDetector
from src.processing_handler import ProcessingHandler
from src.logger_config import *
from src.realtime_audio_handler import RealtimeAudioHandler


class AudioSignals(QObject):
    """Signal container for audio processing results."""
    chord_detected = Signal(list)  # Emits List[Tuple[str, float]]


def _handle_processing_error(error: Exception) -> None:
    """Handle exceptions during audio processing."""
    logging.critical(
        "Critical processing error",
        exc_info=error,
        extra={'error_type': type(error).__name__}
    )


class RealtimeProcessingHandler:
    """Real-time audio processing pipeline for chord detection."""

    def __init__(self,
                 recorder: Type[RealtimeAudioHandler],
                 sample_rate: int = 44100,
                 sleep_time: float = 0.12,
                 chromatic_threshold: float = 0.1):
        """
        Initialize audio processing pipeline.

        Args:
            recorder: RealtimeAudioHandler instance providing audio data
            sample_rate: Sampling rate in Hz (default: 44100)
            sleep_time: Idle time between processing cycles (default: 0.12s)
            chromatic_threshold: Minimum magnitude threshold for chromatic analysis
        """
        self.sample_rate: int = sample_rate
        self.recorder: Type[RealtimeAudioHandler] = recorder
        self.sleep_time: float = sleep_time
        self.chromatic_threshold: float = chromatic_threshold

        self.onset_detector: OnsetDetector = OnsetDetector()
        self.processing_handler: ProcessingHandler = ProcessingHandler(sample_rate=sample_rate)
        self.chord_recognizer: ChordRecognizer = ChordRecognizer()
        self.signals: AudioSignals = AudioSignals()

    def start_processing(self) -> None:
        """Begin continuous audio processing loop."""
        logging.info("Realtime Processing begin")
        while self.recorder.is_recording:
            self._process_audio_chunk()

    def _process_audio_chunk(self) -> None:
        """Process single audio chunk from the recorder queue."""
        try:
            if self.recorder.queue.empty():
                logging.debug("Queue empty, sleeping")
                time.sleep(self.sleep_time)
                return

            audio_chunk: np.ndarray = self._get_audio_chunk()
            logging.debug(f"Chunk received - shape: {audio_chunk.shape}")
            if audio_chunk is None:
                return

            onset_offset: Optional[int] = self.onset_detector.detect_onset(audio_chunk)
            if onset_offset is None:
                logging.debug("No onset detected")
                return
            logging.info(f"Onset detected at offset: {onset_offset}")
            concatenated_audio: np.ndarray = self._collect_post_onset_audio(
                audio_chunk[onset_offset:],
                num_additional_chunks=2
            )

            chords: List[Tuple[str, float]] = self.processing_handler.analyze_audio(concatenated_audio)
            self.signals.chord_detected.emit(chords)

        except Exception as e:
            logging.error("Processing error", exc_info=True)
            _handle_processing_error(e)

    def _get_audio_chunk(self) -> Optional[np.ndarray]:
        """Retrieve and validate audio chunk from queue."""
        try:
            chunk = self.recorder.queue.get_nowait()
            return np.squeeze(chunk).astype(np.float32)
        except self.recorder.queue.Empty:
            return None
        except Exception as e:
            logging.error("Processing error", exc_info=True)
            _handle_processing_error(e)
            return None

    def _collect_post_onset_audio(self,
                                  initial_audio: np.ndarray,
                                  num_additional_chunks: int) -> np.ndarray:
        """Collect post-onset audio samples for analysis."""
        audio_buffer = [initial_audio]
        collected = 0

        while collected < num_additional_chunks and self.recorder.is_recording:
            if self.recorder.queue.empty():
                logging.debug("Cannot concatenate buffs yet. Queue empty, sleeping.")
                time.sleep(self.sleep_time)
                continue

            chunk = self._get_audio_chunk()
            if chunk is not None:
                logging.info(f"{collected}th chunk received - shape: {chunk.shape}")
                audio_buffer.append(chunk)
                collected += 1

        return np.concatenate(audio_buffer, axis=0)
