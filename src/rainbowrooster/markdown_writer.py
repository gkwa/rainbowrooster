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
        """Write a markdown file with frontmatter.

        Preserves existing frontmatter values and file content, only adding new
        key-value pairs. If a key already exists in the file, its value will not
        be overwritten. New keys from frontmatter_data will be merged in if they
        don't exist. The existing content body of the file is preserved.

        Only writes to disk if there are actual changes to avoid unnecessary
        file system operations.
        """
        outdir_path = pathlib.Path(outdir)
        outdir_path.mkdir(parents=True, exist_ok=True)

        file_path = outdir_path / filename

        try:
            # Read any existing frontmatter and content from the file
            existing_post = self._read_existing_file(file_path)

            # Merge frontmatter data: existing values take precedence, new keys
            # are added. Order is critical: frontmatter_data first, then
            # existing_data overwrites. This preserves existing values and only
            # adds missing keys
            merged_metadata = {**frontmatter_data, **existing_post.metadata}

            # Sort the frontmatter keys for consistent ordering
            sorted_metadata = dict(sorted(merged_metadata.items()))

            # Create new post with merged metadata and preserved content
            new_post = frontmatter.Post(existing_post.content, **sorted_metadata)

            # Check if there are any changes before writing
            if self._has_changes(existing_post, new_post):
                content = frontmatter.dumps(new_post)

                # Ensure there's a newline after the final frontmatter delimiter
                if not content.endswith("\n"):
                    content += "\n"

                with file_path.open("w", encoding="utf-8") as file:
                    file.write(content)

                self.logger.info("Generated: %s", file_path)
            else:
                self.logger.debug("No changes detected for: %s", file_path)

        except OSError:
            self.logger.exception("Error writing file %s", file_path)

    @staticmethod
    def _has_changes(
        existing_post: frontmatter.Post, new_post: frontmatter.Post
    ) -> bool:
        """Check if there are any changes between existing and new post data.

        Compares both content and metadata to determine if a file write is needed.
        """
        # Compare content
        if existing_post.content != new_post.content:
            return True

        # Compare metadata (both keys and values)
        return existing_post.metadata != new_post.metadata

    @staticmethod
    def _read_existing_file(file_path: pathlib.Path) -> frontmatter.Post:
        """Read existing frontmatter and content from a file if it exists.

        Returns a Post object with empty content and metadata if the file
        doesn't exist or if frontmatter cannot be parsed. This ensures we can
        always safely merge with new data.
        """
        logger = logging.getLogger(__name__)

        if not file_path.exists():
            return frontmatter.Post("")

        try:
            with file_path.open("r", encoding="utf-8") as file:
                return frontmatter.load(file)
        except (OSError, yaml.YAMLError):
            logger.debug("Could not parse existing file %s", file_path)
            return frontmatter.Post("")

    @staticmethod
    def _read_existing_frontmatter(
        file_path: pathlib.Path,
    ) -> dict[str, typing.Any]:
        """Read existing frontmatter from a file if it exists.

        Returns an empty dictionary if the file doesn't exist or if frontmatter
        cannot be parsed. This ensures we can always safely merge with new data.

        Note: This method is now deprecated in favor of _read_existing_file
        which preserves both frontmatter and content.
        """
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
