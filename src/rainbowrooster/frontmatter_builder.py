import re
import typing


class FrontmatterBuilder:
    """Builds frontmatter data for markdown files."""

    @staticmethod
    def _to_snake_case(text: str) -> str:
        """Convert text to snake_case format."""
        # Replace dots, hyphens, apostrophes, and spaces with underscores
        text = re.sub(r"[.\-\'\s]+", "_", text)
        # Convert to lowercase
        text = text.lower()
        # Remove leading/trailing underscores
        text = text.strip("_")
        # Replace multiple consecutive underscores with single underscore
        return re.sub(r"_+", "_", text)

    @staticmethod
    def build_product_frontmatter(
        stores: list[str], existing_data: dict[str, typing.Any]
    ) -> dict[str, typing.Any]:
        """Build frontmatter for a product file."""
        frontmatter_data = existing_data.copy()
        frontmatter_data["filetype"] = "product"

        for store in stores:
            snake_case_store = FrontmatterBuilder._to_snake_case(store)
            frontmatter_data[snake_case_store] = False

        return frontmatter_data
