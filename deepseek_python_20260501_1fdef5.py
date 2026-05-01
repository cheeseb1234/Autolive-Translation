from abc import ABC, abstractmethod
from rtt.core.datatypes import FramePacket

class CaptureProvider(ABC):
    @abstractmethod
    def start(self) -> None: ...

    @abstractmethod
    def stop(self) -> None: ...

    @abstractmethod
    def get_frame(self) -> FramePacket: ...