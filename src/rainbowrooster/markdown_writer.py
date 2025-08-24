import logging
import pathlib
import typing

import frontmatter
import yaml


class MarkdownWriter:
    """Handles writing markdown files with frontmatter."""

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)

    def write_file(
        self,
        filename: str,
        frontmatter_data: dict[str, typing.Any],
        *,
        outdir: str = ".",
    ) -> None:
        """Write a markdown file with frontmatter."""
        outdir_path = pathlib.Path(outdir)
        outdir_path.mkdir(parents=True, exist_ok=True)

        file_path = outdir_path / filename

        try:
            existing_data = self._read_existing_frontmatter(file_path)
            merged_data = {**existing_data, **frontmatter_data}

            post = frontmatter.Post("", **merged_data)
            content = frontmatter.dumps(post)

            # Ensure there's a newline after the final frontmatter delimiter
            if not content.endswith("\n"):
                content += "\n"

            with file_path.open("w", encoding="utf-8") as file:
                file.write(content)

            self.logger.info("Generated: %s", file_path)

        except OSError:
            self.logger.exception("Error writing file %s", file_path)

    @staticmethod
    def _read_existing_frontmatter(
        file_path: pathlib.Path,
    ) -> dict[str, typing.Any]:
        """Read existing frontmatter from a file if it exists."""
        logger = logging.getLogger(__name__)

        if not file_path.exists():
            return {}

        try:
            with file_path.open("r", encoding="utf-8") as file:
                post = frontmatter.load(file)
                return post.metadata
        except (OSError, yaml.YAMLError):
            logger.debug("Could not parse existing frontmatter from %s", file_path)
            return {}
