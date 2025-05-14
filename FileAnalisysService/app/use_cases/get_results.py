from app.domain.exceptions.exceptions import FileNotFoundException

class GetAnalysisResultsUseCase:
    def execute(self, location: str) -> bytes:
        """
        Retrieve the file content from the given location.
        """
        try:
            with open(f"wordclouds/{location}", "rb") as img:
                content = img.read()
        except Exception:
            raise FileNotFoundException
        return content
