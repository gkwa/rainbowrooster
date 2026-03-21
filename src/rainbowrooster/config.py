import dataclasses


@dataclasses.dataclass
class Config:
    """Configuration for markdown file generation."""

    products_file: str
    outdir: str
    annotate_test: bool
