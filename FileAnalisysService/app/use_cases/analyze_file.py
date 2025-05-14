import re
import os
import hashlib
from uuid import UUID
from app.domain.repositories.analysis_repository import FileAnalysisRepository
from app.domain.repositories.storage_client import FileStorageClient
from app.domain.entities.models import FileAnalysisModel
from app.domain.services.wordcloud_client import WordCloudClient
from app.domain.services.file_storage_client import FileStorageClient


class AnalyzeFileUseCase:
    def __init__(
        self,
        analysis_repo: FileAnalysisRepository,
        storage_client: FileStorageClient,
        wordcloud_client: WordCloudClient,
        file_storage_client: FileStorageClient,
    ):
        """
        Initialize the AnalyzeFileUseCase with the required dependencies.
        :param analysis_repo: Repository for file analysis results.
        :param storage_client: Client for file storage operations.
        :param
        wordcloud_client: Client for generating word clouds.
        """
        self.analysis_repo = analysis_repo
        self.storage = storage_client
        self.wordcloud = wordcloud_client
        self.file_storage_client = file_storage_client

    def generate_svg(self, text: str, file_id: UUID) -> None:
        image_bytes = self.wordcloud.generate(text)

        image_path = f"wordclouds/{file_id}.svg"
        with open(image_path, "wb") as img:
            img.write(image_bytes)

    def execute(self, file_id: UUID) -> FileAnalysisModel:
        """
        Execute the file analysis use case.
        :param file_id: The ID of the file to analyze.
        :return: The file analysis result.
        """
        existing_analysis = self.analysis_repo.get_by_id(file_id)
        if existing_analysis:
            return existing_analysis
        
        content_bytes = self.file_storage_client.get_file(file_id)

        text = content_bytes.decode("utf-8", errors="ignore")

        paragraphs = len([p for p in re.split(r"\n\s*\n", text) if p.strip()])
        words = len(text.split())
        symbols = len(text)

        content_hash = hashlib.sha256(content_bytes).hexdigest()

        existing = self.analysis_repo.find_by_hash(content_hash)
        if existing:
            return existing

        self.generate_svg(text, file_id)

        analysis = FileAnalysisModel(
            file_id=file_id,
            paragraphs_count=paragraphs,
            words_count=words,
            symbols_count=symbols,
            content_hash=content_hash,
            wordcloud_location=f"{file_id}.svg",
        )
        self.analysis_repo.save(analysis)

        return analysis