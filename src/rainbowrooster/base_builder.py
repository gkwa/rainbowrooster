import string

import rainbowrooster.snake_case


class BaseBuilder:
    """Builds content for Obsidian Bases .base files and companion markdown."""

    def _sorted_pairs(self, stores: list[str]) -> list[tuple[str, str]]:
        """Return (snake_key, display_name) pairs sorted by snake_key."""
        pairs = [(rainbowrooster.snake_case.to_snake_case(s), s) for s in stores]
        return sorted(pairs, key=lambda p: p[0])

    def _column_labels(self, count: int) -> list[str]:
        """Return Excel-style column labels: A, B, ..., Z, AA, AB, ..."""
        labels: list[str] = []
        for first in [""] + list(string.ascii_uppercase):
            for second in string.ascii_uppercase:
                labels.append(first + second)
                if len(labels) >= count:
                    return labels
        return labels

    def _assign_columns(self, stores: list[str]) -> list[tuple[str, str, str]]:
        """Return (label, snake_key, display_name) triples assigned A, B, C, ..., AA, ..."""
        pairs = self._sorted_pairs(stores)
        labels = self._column_labels(len(pairs))
        return [(labels[i], key, name) for i, (key, name) in enumerate(pairs)]

    def _stores_formula(self, stores: list[str]) -> str:
        """Build the cascaded if() chain for the Stores formula."""
        pairs = self._sorted_pairs(stores)
        parts: list[str] = []
        for i, (key, name) in enumerate(pairs):
            preceding = [k for k, _ in pairs[:i]]
            if not preceding:
                parts.append(f'if({key}, "{name}", "")')
            else:
                prev_check = " || ".join(preceding)
                parts.append(
                    f'if({key}, if({prev_check}, ", {name}", "{name}"), "")'
                )
        return " + ".join(parts)

    def _view_filter_block(self, keys: list[str], indent: int) -> str:
        """Build the filters: and: [hasTag, or: [...]] block for a view."""
        p = " " * indent
        lines = [
            f"{p}filters:",
            f"{p}  and:",
            f'{p}    - file.hasTag("product")',
            f"{p}    - or:",
        ]
        lines += [f"{p}        - {k} == true" for k in keys]
        return "\n".join(lines)

    def build_shopping_list_base(self, stores: list[str]) -> str:
        """Return full content of Shopping list.base."""
        cols = self._assign_columns(stores)
        keys = [key for _, key, _ in cols]

        lines: list[str] = [
            "filters:",
            "  and:",
            '    - file.hasTag("product")',
            "formulas:",
        ]
        for letter, key, _ in cols:
            lines.append(f"  {letter}: {key}")
        lines += [
            "views:",
            "  - type: table",
            "    name: Shopping List",
        ]
        lines.append(self._view_filter_block(keys, indent=4))
        lines += ["    order:", "      - file.name"]
        lines += [f"      - formula.{letter}" for letter, _, _ in cols]
        lines += [
            "    sort:",
            "      - property: file.name",
            "        direction: ASC",
        ]
        return "\n".join(lines) + "\n"

    def build_shopping_list_2_base(self, stores: list[str]) -> str:
        """Return full content of Shopping list 2.base."""
        pairs = self._sorted_pairs(stores)
        keys = [k for k, _ in pairs]

        lines: list[str] = [
            "filters:",
            "  and:",
            '    - file.hasTag("product")',
            "formulas:",
            f"  Stores: {self._stores_formula(stores)}",
            "views:",
            "  - type: table",
            "    name: Shopping Summary",
        ]
        lines.append(self._view_filter_block(keys, indent=4))
        lines += [
            "    order:",
            "      - file.name",
            "      - formula.Stores",
            "    sort:",
            "      - property: formula.Stores",
            "        direction: ASC",
            "      - property: file.name",
            "        direction: DESC",
        ]
        for key, name in pairs:
            lines += [
                "  - type: table",
                f"    name: {name}",
                "    filters:",
                "      and:",
                '        - file.hasTag("product")',
                f"        - {key} == true",
                "    order:",
                "      - file.name",
                f"      - {key}",
                "    sort:",
                "      - property: file.name",
                "        direction: ASC",
            ]
        lines += ["  - type: table", "    name: All Items"]
        lines.append(self._view_filter_block(keys, indent=4))
        lines += ["    order:", "      - file.name"]
        lines += [f"      - {k}" for k in keys]
        lines += [
            "    sort:",
            "      - property: file.name",
            "        direction: ASC",
        ]
        return "\n".join(lines) + "\n"

    def build_shopping_list_2_md(self, stores: list[str]) -> str:
        """Return full content of Shopping list 2.md."""
        cols = self._assign_columns(stores)
        name_w = max(len(name) for _, _, name in cols)

        rows = [
            f"| {letter}  | {name.ljust(name_w)} |"
            for letter, _, name in cols
        ]
        lines = [
            "![[Shopping list.base]]",
            "",
            "## Store Reference Chart",
            "",
            f"| Column | {'Store Name'.ljust(name_w)} |",
            f"| ------ | {'-' * name_w} |",
        ] + rows + [""]
        return "\n".join(lines)
