from abc import ABC, abstractmethod
from typing import List
from rtt.core.datatypes import TrackedTextBox, TextBox

class TrackingProvider(ABC):
    @abstractmethod
    def update(self, new_boxes: List[TextBox]) -> List[TrackedTextBox]: ...

    @abstractmethod
    def get_stable_tracks(self) -> List[TrackedTextBox]: ...