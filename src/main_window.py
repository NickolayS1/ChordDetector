import sys
import threading
from pathlib import Path
from typing import ClassVar, Dict, List, Optional, Tuple, cast, Type

import numpy as np
from PySide6.QtCore import QSize, Qt, Signal, QObject
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import (QApplication, QFileDialog, QLabel, QMainWindow,
                               QMessageBox, QWidget)
from PySide6.QtUiTools import QUiLoader

from audio_handler import AudioHandler
from chord_templates import chromatic_vectors
from chord_recognizer import ChordRecognizer
from processing_handler import ProcessingHandler
from realtime_audio_handler import RealtimeAudioHandler
from realtime_processing_handler import RealtimeProcessingHandler
import icons.rc_icons
from logger_config import *
from window_ui import Ui_MainWindow

# Constants
DEFAULT_CHORD_ICON_PATH = Path("chord_positions/Blank-0.svg")
CHORD_IMAGES_DIR = Path("chord_positions")
CHORD_IMAGE_SIZE = QSize(160, 400)


class ProcessingSignals(QObject):
    chord_detected = Signal(list)  # List[Tuple[str, str]]


class MainWindow(QMainWindow):
    CONFIDENCE_COLORS: ClassVar[Dict[str, str]] = {
        "Great confidence": "#20B2AA",
        "High confidence": "#80ff80",
        "Moderate confidence": "#FFD700",
        "Low confidence": "#FFA500",
        "Extremely low confidence": "#FF0000"
    }

    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_MainWindow()
        self.audio_handler: AudioHandler
        self.processing_handler: ProcessingHandler
        self.chord_recognizer: ChordRecognizer
        self.recorder: Type[RealtimeAudioHandler]
        self.processor: RealtimeProcessingHandler
        self.recorded_audio: Optional[np.ndarray] = None
        self.imported_audio: Optional[np.ndarray] = None
        self.processing_thread: Optional[threading.Thread] = None
        self.directions: List[int] = [0, 0, 0]
        self.chord_labels: List[Tuple[QLabel, QLabel, QLabel]] = []
        self.realtime_running: bool = False

        self.setup_ui()
        self.initialize_components()
        self.setup_connections()

    def setup_ui(self) -> None:
        """Initialize the UI components and set default images."""
        self.ui.setupUi(self)
        default_icon = QIcon(str(DEFAULT_CHORD_ICON_PATH))
        for label in [self.ui.chord_pic, self.ui.chord_pic_2, self.ui.chord_pic_3]:
            cast(QLabel, label).setPixmap(default_icon.pixmap(CHORD_IMAGE_SIZE))

    def initialize_components(self) -> None:
        """Initialize application components and state."""
        self.audio_handler = AudioHandler(duration=4)
        self.processing_handler = ProcessingHandler()
        self.chord_recognizer = ChordRecognizer()
        self.recorder = RealtimeAudioHandler()
        self.processor = RealtimeProcessingHandler(self.recorder)

        self.chord_labels = [
            (self.ui.chord_pic, self.ui.label_name, self.ui.label_conf),
            (self.ui.chord_pic_2, self.ui.label_name_2, self.ui.label_conf_2),
            (self.ui.chord_pic_3, self.ui.label_name_3, self.ui.label_conf_3)
        ]

        self._setup_chord_buttons()
        self.processor.signals.chord_detected.connect(self.update_realtime_chord)

    def _setup_chord_buttons(self) -> None:
        """Connect chord navigation buttons to their handlers."""
        button_mappings = [
            (self.ui.bck_btn_1_chord, 0, -1),
            (self.ui.fwd_btn_1_chord, 0, 1),
            (self.ui.bck_btn_2_chord, 1, -1),
            (self.ui.fwd_btn_2_chord, 1, 1),
            (self.ui.bck_btn_3_chord, 2, -1),
            (self.ui.fwd_btn_3_chord, 2, 1),
        ]
        for btn, idx, direction in button_mappings:
            btn.clicked.connect(lambda _, i=idx, d=direction: self.switch_chord_position(i, d))

    def setup_connections(self) -> None:
        """Connect UI signals to their respective slots."""
        self.ui.rtime_btn.clicked.connect(self.toggle_realtime)
        self.ui.rec_btn.clicked.connect(self.record_audio)
        self.ui.play_btn.clicked.connect(self.play_recorded_audio)
        self.ui.imp_btn.clicked.connect(self.import_audio)
        self.ui.exp_btn.clicked.connect(self.export_audio)

    def toggle_realtime(self) -> None:
        """Toggle real-time chord detection state."""
        self.realtime_running = not self.realtime_running
        self.ui.rtime_btn.setText(
            "Stop Realtime Detection"
            if self.realtime_running
            else "Start Realtime Detection"
        )
        self.start_realtime() if self.realtime_running else self.stop_realtime()

    def start_realtime(self) -> None:
        """Start real-time processing thread."""
        logging.info("Start realtime\n")
        self.recorder.start()
        self.processing_thread = threading.Thread(
            target=self.processor.start_processing,
            daemon=True
        )
        self.processing_thread.start()

    def stop_realtime(self) -> None:
        """Stop real-time processing and clean up resources."""
        logging.info("Stop realtime\n")
        self.recorder.stop()
        if self.processing_thread and self.processing_thread.is_alive():
            self.processing_thread.join(timeout=2)

    def update_realtime_chord(self, chords_data: List[Tuple[str, float]]) -> None:
        """Update UI with real-time chord detection results."""
        self.update_chord_display(chords_data)

    def update_chord_display(self, chords: List[Tuple[str, float]]) -> None:
        """Update all chord displays with new detection results."""
        for i, (chord, error) in enumerate(chords):
            self.directions[i] = 0
            confidence: str = self._evaluate_confidence(error)
            label_pix, label_name, label_conf = self.chord_labels[i]
            self._set_chord_label(label_name, label_conf, chord, confidence, i)
            logging.info(f"Updated {i}th chord to {chord} with {confidence}")

    def _set_chord_label(
            self,
            name_label: QLabel,
            conf_label: QLabel,
            chord: str,
            confidence: str,
            index: int
    ) -> None:
        """Update individual chord display with name, confidence, and image."""
        name_label.setText(chord)
        self._set_confidence_style(conf_label, confidence)
        self._update_chord_image(chord, index)
    def _evaluate_confidence(self, error: float) -> str:
        """
        Evaluate confidence level based on error score.

        Args:
            error: Error value between 0 (perfect) and 1 (worst)

        Returns:
            Confidence level description
        """
        if error <= 0.15:
            return "Great confidence"
        if 0.15 < error < 0.4:
            return "High confidence"
        if 0.4 <= error < 0.6:
            return "Moderate confidence"
        if 0.6 <= error <= 0.75:
            return "Low confidence"
        if error > 0.75:
            return "Extremely low confidence"

    def _set_confidence_style(self, label: QLabel, confidence: str) -> None:
        """Set confidence label text and color based on confidence level."""
        label.setText(confidence)
        label.setStyleSheet(
            f"color: {self.CONFIDENCE_COLORS.get(confidence, '#000000')};"
            "font-weight: bold;"
        )

    def _update_chord_image(self, chord: str, index: int) -> None:
        """Update chord image based on detected chord."""
        if chord == "N/A":
            icon_path = DEFAULT_CHORD_ICON_PATH
        else:
            root = self._get_chord_root(chord)
            icon_path = CHORD_IMAGES_DIR / root / f"{chord}-0.svg"
            if not icon_path.exists():
                icon_path = DEFAULT_CHORD_ICON_PATH

        self.chord_labels[index][0].setPixmap(
            QIcon(str(icon_path)).pixmap(CHORD_IMAGE_SIZE)
        )

    @staticmethod
    def _get_chord_root(chord: str) -> str:
        """Extract root note from chord name."""
        if len(chord) == 1:
            return chord
        return (chord[:2] if chord[1] == '#' else chord[0]) if chord else ""

    def get_chords_type_count(self, chord_name: str) -> int:
        """Count available variations for a chord type."""
        root = self._get_chord_root(chord_name)
        chord_dir = CHORD_IMAGES_DIR / root
        return sum(1 for _ in chord_dir.glob(f"{chord_name}-*.svg"))

    def switch_chord_position(self, index: int, direction: int) -> None:
        """Cycle through different chord diagram variations."""
        logging.info(f"Switch {index}th chord position")
        chord_name = self.chord_labels[index][1].text()
        if (count := self.get_chords_type_count(chord_name)) <= 1:
            return

        self.directions[index] = (self.directions[index] + direction) % count
        icon = QIcon(str(
            CHORD_IMAGES_DIR /
            self._get_chord_root(chord_name) /
            f"{chord_name}-{self.directions[index]}.svg"
        ))
        self.chord_labels[index][0].setPixmap(icon.pixmap(CHORD_IMAGE_SIZE))

    def record_audio(self) -> None:
        """Handle audio recording and processing."""
        logging.info("Record audio\n")
        if self.realtime_running:
            self.stop_realtime()
        self.ui.imp_btn.setText('Import Audio')
        self.ui.rtime_btn.setText("Start Realtime Detection")
        self.recorded_audio = self.audio_handler.record_audio()
        self._process_and_display_recorded()

    def play_recorded_audio(self) -> None:
        """Play the currently recorded audio."""
        if self.recorded_audio is None:
            QMessageBox.warning(self, "Warning", "No recordings to play")
            logging.warning("User tried to play empty audio")
            return
        self.audio_handler.play_audio(self.recorded_audio)

    def import_audio(self) -> None:
        """Import audio file and process it."""
        if self.realtime_running:
            self.stop_realtime()

        if file_path := QFileDialog.getOpenFileName(
                self, "Import WAV File", "", "WAV Files (*.wav)"
        )[0]:
            self.imported_audio = self.audio_handler.import_audio(file_path)
            self.ui.imp_btn.setText(f'Imported {Path(file_path).name}')
            self._process_and_display_imported()

    def export_audio(self) -> None:
        """Export recorded audio to file."""
        if self.recorded_audio is None:
            QMessageBox.warning(self, "Warning", "No audio to export")
            logging.warning("User tried to export empty audio")
            return

        if file_path := QFileDialog.getSaveFileName(
                self, "Save Recorded Audio", "", "WAV Files (*.wav)"
        )[0]:
            try:
                self.audio_handler.export_audio(self.recorded_audio, file_path)
                QMessageBox.information(self, "Success", "Audio exported successfully")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Export failed: {str(e)}")
                logging.critical(f"Export failed: {str(e)}")

    def _process_and_display_imported(self) -> None:
        """Process and display results for imported audio."""
        if self.imported_audio is None:
            QMessageBox.critical(self, "Error", "No imported audio to process")
            logging.critical(f"No imported audio to process")
            return
        self._process_audio(self.imported_audio)

    def _process_and_display_recorded(self) -> None:
        """Process and display results for recorded audio."""
        if self.recorded_audio is None:
            QMessageBox.critical(self, "Error", "No recorded audio to process")
            logging.critical(f"No recorded audio to process")
            return
        self._process_audio(self.recorded_audio)

    def _process_audio(self, audio_data: np.ndarray) -> None:
        """Common processing logic for audio data."""
        chords_and_error: List[Tuple[str, float]] = self.processing_handler.analyze_audio(audio_data)
        self.update_chord_display(chords_and_error)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
