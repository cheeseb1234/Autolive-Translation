from rtt.overlay.base import OverlayRenderer
from rtt.core.datatypes import TrackedTextBox

class SubtitleBandOverlayRenderer(OverlayRenderer):
    def show(self):
        raise NotImplementedError("Subtitle band overlay not yet implemented")

    def hide(self):
        pass

    def render(self, tracks: list[TrackedTextBox]):
        raise NotImplementedError