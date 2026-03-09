import logging
import pathlib


class BaseWriter:
    """Handles writing plain-text base files with change detection."""

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)

    def write_file(self, filename: str, content: str, *, outdir: str) -> None:
        """Write a plain-text file only if content differs from what exists on disk."""
        outdir_path = pathlib.Path(outdir)
        outdir_path.mkdir(parents=True, exist_ok=True)
        file_path = outdir_path / filename

        if content == self._read_existing(file_path):
            self.logger.debug("No changes detected for: %s", file_path)
            return

        try:
            file_path.write_text(content, encoding="utf-8")
            self.logger.info("Generated: %s", file_path)
        except OSError:
            self.logger.exception("Error writing file %s", file_path)

    @staticmethod
    def _read_existing(file_path: pathlib.Path) -> str:
        if not file_path.exists():
            return ""
        try:
            return file_path.read_text(encoding="utf-8")
        except OSError:
            return ""
