import argparse
import importlib.metadata
import logging
import sys

import rainbowrooster.config
import rainbowrooster.generator


def setup_logging(verbose_count: int) -> None:
    """Configure logging based on verbosity level."""
    log_levels = [logging.WARNING, logging.INFO, logging.DEBUG]
    level = log_levels[min(verbose_count, len(log_levels) - 1)]

    logging.basicConfig(
        level=level, format="%(levelname)s: %(message)s", stream=sys.stderr
    )


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        description="Generate test markdown files for products and stores"
    )

    parser.add_argument(
        "--products",
        type=str,
        default="products.txt",
        help="Path to products file (default: products.txt)",
    )

    parser.add_argument(
        "--stores",
        type=str,
        default="stores.txt",
        help="Path to stores file (default: stores.txt)",
    )

    parser.add_argument(
        "--outdir",
        type=str,
        default=".",
        help="Output directory for generated markdown files (default: .)",
    )

    parser.add_argument(
        "--annotate-test",
        action="store_true",
        help="Add '- test' suffix to generated filenames",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Increase verbosity (can be used multiple times)",
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {importlib.metadata.version('rainbowrooster')}",
    )

    return parser


def main() -> None:
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()

    setup_logging(args.verbose)

    config = rainbowrooster.config.Config(
        products_file=args.products,
        stores_file=args.stores,
        outdir=args.outdir,
        annotate_test=args.annotate_test,
    )

    generator_service = rainbowrooster.generator.MarkdownGenerator()
    generator_service.generate_files(config)
