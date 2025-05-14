class FileNotFoundException(Exception):
    """Exception raised when a file is not found."""
    def __init__(self, message="File not found."):
        self.message = message
        super().__init__(self.message)

class FileAlreadyExistsException(Exception):
    """Exception raised when a file already exists."""
    def __init__(self, message="File already exists."):
        self.message = message
        super().__init__(self.message)

class InvalidFileFormatException(Exception):
    """Exception raised when a file format is invalid."""
    def __init__(self, message="Invalid file format."):
        self.message = message
        super().__init__(self.message)