from abc import ABC, abstractmethod
from typing import List
from rtt.core.datatypes import TextBox

class OCRProvider(ABC):
    @abstractmethod
    def recognize(self, image: any, regions: list = None) -> List[TextBox]: ...