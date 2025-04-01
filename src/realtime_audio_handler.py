import sounddevice as sd
import queue
import numpy as np
from typing import Optional, Any
from src.logger_config import *


class RealtimeAudioHandler:
    """Real-time audio recording class with buffer management."""

    queue = None
    is_recording = None

    def __init__(self,
                 sample_rate: int = 44100,
                 buffer_size_seconds: float = 0.25,
                 max_queue_size: int = 20):
        """
        Initialize audio recorder with buffer management.

        Args:
            sample_rate: Audio sampling rate in Hz (default: 44100)
            buffer_size_seconds: Duration of each audio chunk in seconds (default: 0.25)
            max_queue_size: Maximum number of audio chunks to buffer (default: 20)
        """
        self.sample_rate: int = sample_rate
        self.buffer_size: float = buffer_size_seconds
        self.chunk_size: int = int(sample_rate * buffer_size_seconds)
        self.queue: queue.Queue[np.ndarray] = queue.Queue(maxsize=max_queue_size)
        self.is_recording: bool = False
        self.stream: Optional[sd.InputStream] = None

    def start(self) -> None:
        """Start audio recording stream."""
        if self.stream is None or not self.stream.active:
            self.stream = sd.InputStream(
                callback=self._callback,
                blocksize=self.chunk_size,
                channels=1,
                samplerate=self.sample_rate,
                dtype='float32'
            )
            self.is_recording = True
            self.stream.start()
            logging.info("Audio stream started")

    def stop(self) -> None:
        """Stop audio recording stream and clear buffer."""
        if self.stream is not None and self.stream.active:
            self.stream.stop()
            self.is_recording = False
            self.queue.queue.clear()
        logging.info("Audio stream stopped")

    def _callback(self,
                  indata: np.ndarray,
                  frames: int,
                  time: Any,
                  status: sd.CallbackFlags) -> None:
        """
        Audio callback handler for real-time processing.

        Args:
            indata: Input audio data as numpy array
            frames: Number of frames in the current block
            time: Timestamp information (unused)
            status: PortAudio status flags
        """
        if status:
            logging.debug(f'PortAudio status: {status}')

        if self.is_recording:
            audio_chunk = indata.copy()
            try:
                self.queue.put_nowait(audio_chunk)
            except queue.Full:
                # does not happen on practice
                logging.debug(f'Recording queue is full')
                if not self.queue.empty():
                    self.queue.get_nowait()
                self.queue.put_nowait(audio_chunk)

    def get_audio_chunk(self) -> Optional[np.ndarray]:
        """Retrieve the oldest audio chunk from buffer, or None if empty."""
        try:
            return self.queue.get_nowait() if not self.queue.empty() else None
        except queue.Empty:
            return None
