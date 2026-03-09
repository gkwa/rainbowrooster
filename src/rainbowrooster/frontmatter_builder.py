import re
import typing


class FrontmatterBuilder:
    """Builds frontmatter data for markdown files."""

    @staticmethod
    def _to_snake_case(text: str) -> str:
        """Convert text to snake_case format.

        Replaces dots, hyphens, apostrophes, and spaces with underscores,
        converts to lowercase, and normalizes multiple underscores to single ones.
        """
        # Replace dots, hyphens, apostrophes, spaces, commas, and ampersands with underscores
        text = re.sub(r"[.\-\'\s,&]+", "_", text)
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
        """Build frontmatter for a product file.

        Creates frontmatter with filetype set to 'product' and adds a boolean
        field for each store (converted to snake_case) set to False by default.
        These values will only be added if they don't already exist in the file.
        """
        frontmatter_data = existing_data.copy()
        frontmatter_data["filetype"] = "product"

        # Add a boolean field for each store, defaulting to False
        # These will be preserved if they already exist in the file
        for store in stores:
            snake_case_store = FrontmatterBuilder._to_snake_case(store)
            frontmatter_data[snake_case_store] = False

        return frontmatter_data
