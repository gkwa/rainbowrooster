import logging
import pathlib


class FileReader:
    """Handles reading input files."""

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)

    def read_lines(self, file_path: str) -> list[str]:
        """Read and return non-empty lines from a file."""
        path = pathlib.Path(file_path)

        if not path.exists():
            self.logger.error("File not found: %s", file_path)
            return []

        try:
            with path.open("r", encoding="utf-8") as file:
                lines = [line.strip() for line in file.readlines()]
                return [line for line in lines if line]
        except OSError:
            self.logger.exception("Error reading file %s", file_path)
            return []
