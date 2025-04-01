import re
import numpy as np
from pathlib import Path
from typing import Dict, List

# Constants
DEFAULT_OCTAVE = 3
HARMONIC_DECAY_FACTOR = 0.4
HARMONICS_RANGE = range(2, 4)  # 2nd and 3rd harmonics
OUTPUT_FILE = Path("chord_templates.py")

# Note definitions
NOTES_LIST = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
MIDI_BASE_NOTE = 12  # MIDI number for C0
MIDI_NOTES = {note: MIDI_BASE_NOTE + i for i, note in enumerate(NOTES_LIST)}


def note_to_freq(note_str: str) -> float:
    """Convert note string with optional octave to frequency in Hz.

    Args:
        note_str: Note name with optional octave (e.g., 'C4', 'F#3', 'G')

    Returns:
        Calculated frequency in Hz
    """
    match = re.match(r"([A-Z#]+)(\d+)?", note_str)
    if not match:
        raise ValueError(f"Invalid note format: {note_str}")

    note_name, octave_str = match.groups()
    octave = int(octave_str) if octave_str else DEFAULT_OCTAVE

    try:
        midi_number = MIDI_NOTES[note_name] + (octave * 12)
    except KeyError:
        raise ValueError(f"Invalid note name: {note_name}")

    return 440.0 * 2 ** ((midi_number - 69) / 12)


def freq_to_note(freq: float) -> str:
    """Convert frequency to the closest note name.

    Args:
        freq: Frequency in Hz

    Returns:
        Closest note name from NOTES_LIST
    """
    midi_number = 69 + 12 * np.log2(freq / 440)
    midi_number = int(np.round(midi_number))
    note_index = (midi_number - MIDI_BASE_NOTE) % 12
    return NOTES_LIST[note_index]


def build_chord_template(chord_notes: List[str], decay_factor: float = HARMONIC_DECAY_FACTOR) -> Dict[str, float]:
    """Build normalized chord template with harmonic contributions.

    Args:
        chord_notes: List of note names in the chord
        decay_factor: Magnitude decay factor for harmonics

    Returns:
        Normalized template vector as dictionary
    """
    template = {note: 1e-10 for note in NOTES_LIST}
    unique_notes = {re.sub(r'\d+', '', note) for note in chord_notes}
    note_value = 1.0 / len(unique_notes)

    for base_note in unique_notes:
        template[base_note] += note_value

        try:
            freq = note_to_freq(base_note)
        except ValueError:
            continue

        for harmonic in HARMONICS_RANGE:
            harmonic_freq = freq * harmonic
            try:
                harmonic_note = freq_to_note(harmonic_freq)
                template[harmonic_note] += (decay_factor ** (harmonic - 1)) * note_value
            except ValueError:
                continue

    total = sum(template.values())
    return {note: mag / total for note, mag in template.items()} if total > 0 else template


def generate_chord_definitions() -> Dict[str, List[str]]:
    """Generate chord definitions programmatically for all roots."""
    chords = {}
    for root_idx, root in enumerate(NOTES_LIST):
        offsets = {
            '': [0, 4, 7],  # Major
            'm': [0, 3, 7],  # Minor
            '7': [0, 4, 7, 10],  # Dominant 7th
            '7b9': [0, 4, 7, 10, 13],  # Dominant 7th flat ninth
            '7sus4': [0, 5, 7, 10],  # 7th sus 4
            'sus4': [0, 5, 7],  # Suspended 4th
            'sus2': [0, 2, 7],  # Suspended 2nd
            'm7': [0, 3, 7, 10],  # Minor 7th
            'aug': [0, 4, 8],  # Augmented
            'dim': [0, 3, 6],  # Diminished
            'dim7': [0, 3, 6, 9],  # Diminished seventh
            'maj7': [0, 4, 7, 11],  # Major 7th
            'maj7#11': [0, 4, 7, 11, 18],  # Major 7th sharp 11th
            'maj7#5': [0, 4, 8, 11],  # Major 7th sharp 5th
            'm(maj7)': [0, 3, 7, 11],  # Minor Major 7th
            'maj9': [0, 4, 7, 11, 14],  # Major 9th
            'm(add9)': [0, 3, 7, 14],  # Minor add9
            'add9': [0, 4, 7, 14],  # Major add9
            'm9': [0, 3, 7, 10, 14],  # minor 9th
            '13': [0, 4, 10, 14, 21],  # Dominant 13th
            '69': [0, 4, 7, 9, 14],  # Major 6/9
            'm69': [0, 3, 7, 9, 14],  # Minor 6/9
            'm7b5': [0, 3, 6, 10]  # half dim or m7(b5)

        }

        for suffix, intervals in offsets.items():
            chord_notes = []
            for interval in intervals:
                note_idx = (root_idx + interval) % 12
                chord_notes.append(NOTES_LIST[note_idx])

            chord_name = f"{root}{suffix}" if suffix else root
            chords[chord_name] = chord_notes
    return chords


def write_templates_to_file(chords: Dict[str, List[str]]) -> None:
    """Write generated templates to Python file with type hints."""
    chromatic_vectors = {name: build_chord_template(notes) for name, notes in chords.items()}

    with OUTPUT_FILE.open('w', encoding='utf-8') as f:
        f.write("from typing import Dict, List\n\n")
        f.write(f"NOTES: List[str] = {NOTES_LIST}\n\n")
        f.write("chromatic_vectors: Dict[str, Dict[str, float]] = {\n")

        for chord, vector in chromatic_vectors.items():
            f.write(f"    '{chord}': {{\n")
            for note, mag in vector.items():
                f.write(f"        '{note}': {mag:.4f},\n")
            f.write("    },\n")

        f.write("}\n")


if __name__ == "__main__":
    chord_definitions = generate_chord_definitions()
    write_templates_to_file(chord_definitions)
    print(f"Successfully generated chord templates to {OUTPUT_FILE}")
