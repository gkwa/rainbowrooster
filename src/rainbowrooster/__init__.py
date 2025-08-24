import importlib.metadata

import rainbowrooster.cli

__version__ = importlib.metadata.version("rainbowrooster")


def main() -> None:
    """Entry point for the rainbowrooster application."""
    rainbowrooster.cli.main()
