from abc import ABC, abstractmethod

class WordCloudClient(ABC):
    @abstractmethod
    def generate(self, text: str) -> bytes:
        """Generate a word cloud from the given text."""
        ...