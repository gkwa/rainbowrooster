import logging

import rainbowrooster.config
import rainbowrooster.file_reader
import rainbowrooster.filename_builder
import rainbowrooster.frontmatter_builder
import rainbowrooster.markdown_writer


class MarkdownGenerator:
    """Main service for generating markdown files."""

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.file_reader = rainbowrooster.file_reader.FileReader()
        self.filename_builder = rainbowrooster.filename_builder.FilenameBuilder()
        self.frontmatter_builder = (
            rainbowrooster.frontmatter_builder.FrontmatterBuilder()
        )
        self.markdown_writer = rainbowrooster.markdown_writer.MarkdownWriter()

    def generate_files(self, config: rainbowrooster.config.Config) -> None:
        """Generate markdown files based on configuration."""
        products = self.file_reader.read_lines(config.products_file)
        stores = self.file_reader.read_lines(config.stores_file)

        if not products:
            self.logger.warning("No products found to process")
            return

        if not stores:
            self.logger.warning("No stores found to process")
            return

        for product in products:
            self._generate_product_file(
                product,
                stores,
                outdir=config.outdir,
                annotate_test=config.annotate_test,
            )

    def _generate_product_file(
        self,
        product: str,
        stores: list[str],
        *,
        outdir: str,
        annotate_test: bool,
    ) -> None:
        """Generate a single product markdown file."""
        filename = self.filename_builder.build_filename(
            product, annotate_test=annotate_test
        )
        frontmatter_data = self.frontmatter_builder.build_product_frontmatter(
            stores, {}
        )
        self.markdown_writer.write_file(filename, frontmatter_data, outdir=outdir)
