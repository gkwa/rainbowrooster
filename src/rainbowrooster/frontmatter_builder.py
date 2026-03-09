import typing

import rainbowrooster.snake_case


class FrontmatterBuilder:
    """Builds frontmatter data for markdown files."""

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
        frontmatter_data["tags"] = ["product"]

        # Add a boolean field for each store, defaulting to False
        # These will be preserved if they already exist in the file
        for store in stores:
            snake_case_store = rainbowrooster.snake_case.to_snake_case(store)
            frontmatter_data[snake_case_store] = False

        return frontmatter_data
