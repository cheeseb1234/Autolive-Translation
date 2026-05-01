from pathlib import Path
from rtt.capture.base import CaptureProvider
from rtt.core.datatypes import FramePacket

class ReplayCaptureProvider(CaptureProvider):
    def __init__(self, directory: str):
        self.dir = Path(directory)
        self.files = sorted(self.dir.glob("*.png"))
        self.index = 0

    def start(self):
        self.index = 0

    def stop(self):
        pass

    def get_frame(self) -> FramePacket:
        # Placeholder: read image from file
        if self.index >= len(self.files):
            raise StopIteration
        # In real implementation: cv2.imread
        frame = FramePacket(image=None, timestamp=0.0, source=str(self.files[self.index]))
        self.index += 1
        return frame