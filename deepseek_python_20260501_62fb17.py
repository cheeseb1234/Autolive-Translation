from rtt.capture.base import CaptureProvider
from rtt.core.datatypes import FramePacket

class MSSX11CaptureProvider(CaptureProvider):
    def start(self):
        raise NotImplementedError("X11 MSS capture is fallback only")

    def stop(self):
        pass

    def get_frame(self) -> FramePacket:
        raise NotImplementedError