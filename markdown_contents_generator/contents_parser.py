__all__ = [
    "ContentsParser",
    "ContentsItem",
]

import re
from dataclasses import dataclass
from typing import Generator

from markdown_contents_generator.utils import FileReader


@dataclass
class ContentsItem:
    level: int
    raw_line: str
    content_line: str


class ContentsParser:

    def __init__(self, target_file: str):
        self._target_file = target_file

    def parse_contents(self) -> Generator[ContentsItem, None, None]:
        for _, line in FileReader(self._target_file):
            match = re.match("^#+", line.strip())
            if not match:
                continue

            head = len(match.group(0))  # Number of sharps
            item = line[head:].strip()

            yield ContentsItem(
                level=head,
                raw_line=item,
                content_line=re.sub(
                    r"[^\w0-9\_]+",
                    "-",
                    item
                ).lower().strip("-")
            )
