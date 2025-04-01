from typing import Dict, Tuple
import numpy as np
from src.chord_templates import chromatic_vectors


class ChordRecognizer:
    """Recognizes musical chords using chromatic vector analysis and cosine similarity."""

    # Class-level constants for note ordering
    NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

    def __init__(self):
        """
        Initialize chord recognizer with template vectors.
        """
        self.templates = chromatic_vectors

    def find_chord(self, root_note: str, input_vector: Dict[str, float]) -> Tuple[str, float]:
        """
        Find best matching chord for given root note and chromatic vector.

        Args:
            root_note: The root note to match (e.g., 'C', 'G#')
            input_vector: Chromatic profile of the input signal

        Returns:
            Tuple of (best_matching_chord, error_score)
        """
        best_match = None
        max_similarity = -np.inf

        # Filter templates by root note
        candidate_chords = {name: vec for name, vec in self.templates.items()
                            if name.startswith(root_note)}

        for chord_name, template in candidate_chords.items():
            similarity = self._cosine_similarity(template, input_vector)
            if similarity > max_similarity:
                max_similarity = similarity
                best_match = chord_name

        error = 1.0 - max_similarity if best_match else 1.0
        return best_match, error

    @staticmethod
    def _cosine_similarity(template: Dict[str, float],
                           input_vector: Dict[str, float]) -> float:
        """Calculate cosine similarity between two chromatic vectors."""
        # Convert dictionaries to ordered vectors
        vec1 = np.array([template.get(note, 0.0) for note in ChordRecognizer.NOTES])
        vec2 = np.array([input_vector.get(note, 0.0) for note in ChordRecognizer.NOTES])

        dot_product = np.dot(vec1, vec2)
        norm_product = np.linalg.norm(vec1) * np.linalg.norm(vec2)

        return dot_product / (norm_product + 1e-10)  # Prevent division by zero
