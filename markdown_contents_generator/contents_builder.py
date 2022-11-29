__all__ = [
    "ContentsBuilder",
]

from typing import Generator

from markdown_contents_generator.contents_parser import ContentsItem, \
    ContentsParser


class ContentsBuilder:

    def __init__(
        self,
        contents_parser: ContentsParser,
        margin: str,
        prefix: str,
        higher: int,
        lower: int,
        save_margin: bool
    ):
        self._parser = contents_parser
        self._margin = margin
        self._prefix = prefix
        self._higher = higher
        self._lower = lower
        self._save_margin = save_margin

    def build_contents(self) -> Generator[str, None, None]:
        for item in self._parser.parse_contents():
            if self._higher <= item.level <= self._lower:
                yield self._format_item(item)

    def _format_item(self, item: ContentsItem) -> str:
        margin_times = item.level - (0 if self._save_margin else self._higher)

        return "{}{}[{}](#{})".format(
            self._margin * margin_times,
            self._prefix,
            item.raw_line,
            item.content_line
        )
