from rtt.overlay.base import OverlayRenderer
from rtt.core.datatypes import TrackedTextBox

class PySideX11OverlayRenderer(OverlayRenderer):
    def show(self):
        raise NotImplementedError("X11 PySide overlay is fallback only")

    def hide(self):
        pass

    def render(self, tracks: list[TrackedTextBox]):
        raise NotImplementedError