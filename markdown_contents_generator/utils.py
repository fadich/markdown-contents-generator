from typing import Tuple


class FileReader:

    def __init__(self, path: str):
        self._path = path
        self._file = None
        self.line_no = 0
        self._opened = False

    def __iter__(self):
        return self

    def __next__(self) -> Tuple[int, str]:
        if not self._opened:
            self._open()

        while True:
            self.line_no += 1
            line = self._file.readline()
            if line:
                return self.line_no, line

            self._close()
            raise StopIteration

    def __del__(self):
        self._close()

    def _open(self):
        self._file = open(self._path)
        self._opened = True

    def _close(self):
        self.line_no = 0
        self._opened = False
        if self._file and not self._file.closed:
            self._file.close()
