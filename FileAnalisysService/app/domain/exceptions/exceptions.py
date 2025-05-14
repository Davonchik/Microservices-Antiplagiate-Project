class FileNotFoundException(Exception):
    """Raised when a requested file (or its analysis) is not found."""
    def __init__(self, message: str = "File not found."):
        super().__init__(message)
        self.message = message


class FileAlreadyExistsException(Exception):
    """Raised when trying to upload a file that is already stored."""
    def __init__(self, message: str = "File already exists."):
        super().__init__(message)
        self.message = message


class InvalidFileFormatException(Exception):
    """Raised when an unsupported file format is uploaded."""
    def __init__(self, message: str = "Invalid file format."):
        super().__init__(message)
        self.message = message


class StorageUnavailableException(Exception):
    """Raised when the File Storing Service cannot be reached."""
    def __init__(self, message: str = "Storage service unavailable."):
        super().__init__(message)
        self.message = message