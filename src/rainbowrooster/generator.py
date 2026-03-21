import logging

import rainbowrooster.base_builder
import rainbowrooster.base_writer
import rainbowrooster.config
import rainbowrooster.file_reader
import rainbowrooster.filename_builder
import rainbowrooster.frontmatter_builder
import rainbowrooster.markdown_writer
import rainbowrooster.stores_loader


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
        self.base_builder = rainbowrooster.base_builder.BaseBuilder()
        self.base_writer = rainbowrooster.base_writer.BaseWriter()

    def generate_files(self, config: rainbowrooster.config.Config) -> None:
        """Generate markdown files based on configuration."""
        products = self.file_reader.read_lines(config.products_file)
        stores = rainbowrooster.stores_loader.load_stores()

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

        self._generate_base_files(stores, outdir=config.outdir)

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

    def _generate_base_files(self, stores: list[str], *, outdir: str) -> None:
        """Generate the Obsidian Bases support files."""
        self.base_writer.write_file(
            "Shopping list.base",
            self.base_builder.build_shopping_list_base(stores),
            outdir=outdir,
        )
        self.base_writer.write_file(
            "Shopping list 2.base",
            self.base_builder.build_shopping_list_2_base(stores),
            outdir=outdir,
        )
        self.base_writer.write_file(
            "Shopping list 2.md",
            self.base_builder.build_shopping_list_2_md(stores),
            outdir=outdir,
        )
