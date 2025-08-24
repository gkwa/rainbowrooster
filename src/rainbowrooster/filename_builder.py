class FilenameBuilder:
    """Builds filenames for generated markdown files."""

    @staticmethod
    def build_filename(product_name: str, *, annotate_test: bool) -> str:
        """Build filename for a product."""
        filename = product_name.lower()

        if annotate_test:
            filename += " - test"

        return f"{filename}.md"
