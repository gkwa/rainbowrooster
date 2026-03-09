import re


def to_snake_case(text: str) -> str:
    """Convert text to snake_case format.

    Replaces dots, hyphens, apostrophes, spaces, commas, and ampersands with
    underscores, converts to lowercase, and normalizes multiple underscores.
    """
    text = re.sub(r"[.\-\'\s,&]+", "_", text)
    text = text.lower()
    text = text.strip("_")
    return re.sub(r"_+", "_", text)
