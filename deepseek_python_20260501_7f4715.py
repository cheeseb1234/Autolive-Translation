from abc import ABC, abstractmethod
from rtt.core.datatypes import TranslationUnit

class TranslationProvider(ABC):
    @abstractmethod
    def translate(self, text: str, source_lang: str, target_lang: str) -> TranslationUnit: ...