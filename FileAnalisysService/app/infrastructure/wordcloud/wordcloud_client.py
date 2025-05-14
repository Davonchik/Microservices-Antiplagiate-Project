from app.domain.services.wordcloud_client import WordCloudClient
import requests

class WordCloudClientImpl(WordCloudClient):
    def __init__(self, url: str = "https://quickchart.io/wordcloud"):
        self.url = url

    def generate(self, text: str) -> bytes:
        """
        Generate a word cloud image from the given text.
        :param text: The text to generate the word cloud from.
        :return: The generated word cloud image as bytes.
        """
        response = requests.get(
            self.url,
            params={"text": text},
        )
        if response.status_code != 200:
            raise Exception("Failed to generate word cloud")
        return response.content
        