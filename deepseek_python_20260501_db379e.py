from dataclasses import dataclass, field
from typing import Optional, Tuple
import time

@dataclass
class FramePacket:
    image: any               # numpy ndarray or bytes placeholder
    timestamp: float
    source: str = ""
    dirty_regions: list = field(default_factory=list)

@dataclass
class TextBox:
    bounds: Tuple[int, int, int, int]   # (x, y, w, h)
    text: str
    confidence: float
    language: str = ""

@dataclass
class TranslationUnit:
    source_text: str
    translated_text: str
    source_lang: str
    target_lang: str
    confidence: float = 1.0

@dataclass
class TrackedTextBox:
    track_id: int
    box: TextBox
    stable_text: str = ""
    is_stable: bool = False
    last_translation: Optional[TranslationUnit] = None
    frames_since_last_change: int = 0