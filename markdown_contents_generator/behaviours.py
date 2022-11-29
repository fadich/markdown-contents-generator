__all__ = [
    "print_contents",
    "update_file",
]

import os
import re
import shutil
import sys
from datetime import time

from markdown_contents_generator.contents_builder import ContentsBuilder
from markdown_contents_generator.utils import FileReader


def print_contents(contents_builder: ContentsBuilder):
    for line in contents_builder.build_contents():
        sys.stdout.write(f"{line}\n")
        sys.stdout.flush()


def update_file(
    contents_builder: ContentsBuilder,
    target_file: str,
    replace_tags: bool = False
) -> int:
    return FileUpdater(contents_builder, target_file) \
        .insert_contents(replace_tags=replace_tags)


class FileUpdater:
    CONTENT_START = (
        """<br class="contents-start" style="display:none" />"""
    )
    CONTENT_FINISH = (
        """<br class="contents-finish" style="display:none" />"""
    )

    def __init__(self, contents_builder: ContentsBuilder, path: str):
        self._builder = contents_builder
        self._path = path

        self._copy_path = None

    def analyze(self):
        opened_no = 0
        opened = False

        for line_no, line in FileReader(self._path):
            if self.is_opening_tag(line):
                if opened:
                    raise SyntaxError(
                        f"Nested contents tags not allowed in line: {line_no}"
                    )
                else:
                    opened_no = line_no
                    opened = True

            if self.is_closing_tag(line):
                if opened:
                    opened = False
                else:
                    raise SyntaxError(
                        f"Unexpected closing tag in line: {line_no}"
                    )

        if opened:
            raise SyntaxError(
                f"No closing tag found for opened in line: {opened_no}"
            )

    def insert_contents(self, replace_tags: bool = False) -> int:
        self.analyze()

        self._make_copy()

        try:
            inserted = self._update_content(replace_tags=replace_tags)
            self._replace()

            return inserted
        except Exception:
            self._remove_copy()

            raise

    @classmethod
    def is_opening_tag(cls, line: str) -> bool:
        return bool(re.match(r"^.*\<\s*contents-start.*/>.*$", line))

    @classmethod
    def is_closing_tag(cls, line: str) -> bool:
        return bool(re.match(r"^.*\<\s*contents-finish.*/>.*$", line))

    def _update_content(self, replace_tags: bool = False) -> int:
        inserted_count = 0

        with open(self._copy_path, "r+") as file:
            file.truncate(0)

            opened = False
            for _, line in FileReader(self._path):
                if self.is_opening_tag(line):
                    opened = True
                    if not replace_tags:
                        file.write(line)

                    if not replace_tags:
                        file.write(f"\n")

                    for cl in self._builder.build_contents():
                        file.write(f"{cl}\n")

                    if not replace_tags:
                        file.write(f"\n")

                    inserted_count += 1
                elif self.is_closing_tag(line):
                    opened = False
                    if not replace_tags:
                        file.write(line)
                else:
                    if not opened:
                        file.write(line)

            file.flush()

        return inserted_count

    def _make_copy(self):
        self._copy_path = f"{self._path}{hash(time())}"
        shutil.copyfile(self._path, self._copy_path)

    def _remove_copy(self):
        if self._copy_path is None:
            return

        if os.path.exists(self._copy_path):
            os.remove(self._copy_path)

        self._copy_path = None

    def _replace(self):
        if self._copy_path is None:
            return

        os.remove(self._path)
        shutil.move(self._copy_path, self._path)
