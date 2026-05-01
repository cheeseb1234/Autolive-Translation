import os
from dataclasses import dataclass

@dataclass
class LinuxEnvInfo:
    session_type: str
    compositor: str
    pipewire_available: bool
    portal_backend: str
    layer_shell_available: bool

def detect_linux_env() -> LinuxEnvInfo:
    session_type = os.environ.get("XDG_SESSION_TYPE", "unknown").lower()
    compositor = os.environ.get("XDG_CURRENT_DESKTOP", "unknown")

    # PipeWire detection (basic)
    pw_available = os.path.exists("/usr/bin/pw-cli") or os.path.exists("/usr/bin/pipewire")

    # Portal backend (try to get from systemd or env)
    portal_backend = os.environ.get("GTK_USE_PORTAL", "0")  # not definitive, placeholder

    # Layer shell: likely if wlroots-based compositor
    wlroots_hints = ["sway", "hyprland", "river", "wayfire"]
    layer_available = any(hint in compositor.lower() for hint in wlroots_hints)

    return LinuxEnvInfo(
        session_type=session_type,
        compositor=compositor,
        pipewire_available=pw_available,
        portal_backend=portal_backend,
        layer_shell_available=layer_available,
    )