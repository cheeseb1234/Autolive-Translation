import toml
from pathlib import Path
from dataclasses import dataclass, field

@dataclass
class AppConfig:
    source_lang: str = "en"
    target_lang: str = "es"
    capture_backend: str = "pipewire"      # pipewire, replay, x11
    overlay_backend: str = "subtitle_band"  # subtitle_band, layer_shell, x11
    ocr_engine: str = "paddleocr"
    translation_engine: str = "argos"
    db_path: str = "~/.cache/rtt/cache.db"

def load_config(path: str = "~/.config/rtt/config.toml") -> AppConfig:
    p = Path(path).expanduser()
    if p.exists():
        data = toml.load(p)
        return AppConfig(**data.get("rtt", {}))
    return AppConfig()