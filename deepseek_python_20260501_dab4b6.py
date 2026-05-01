from abc import ABC, abstractmethod
from rtt.core.datatypes import TrackedTextBox

class OverlayRenderer(ABC):
    @abstractmethod
    def show(self) -> None: ...

    @abstractmethod
    def hide(self) -> None: ...

    @abstractmethod
    def render(self, tracks: list[TrackedTextBox]) -> None: ...