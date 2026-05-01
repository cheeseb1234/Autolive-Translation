from rtt.capture.base import CaptureProvider
from rtt.core.datatypes import FramePacket

class PipeWirePortalCaptureProvider(CaptureProvider):
    def start(self):
        raise NotImplementedError("PipeWire portal capture not yet implemented")

    def stop(self):
        pass

    def get_frame(self) -> FramePacket:
        raise NotImplementedError