import io
import os
import zipfile
from pathlib import Path

import openpyxl
import requests
import pandas

from vaalianalyysi.data import checksum


_DATA_ROOT = Path(".vaalianalyysi-data")


class Download:
    """Downloadable data file"""

    def __init__(self, path, url, chk=None):
        """New downloadable file"""
        self.path = _DATA_ROOT / Path(path)
        self.url = url
        if chk is None:
            self.checksum = None
        elif chk.startswith("http"):
            self.checksum = Download(path + ".chk", chk)
        else:
            self.checksum = chk
        self._ready = False

    def require(self) -> None:
        """Require this file to exist"""
        if not self._ready:
            if not self.verify():
                self.fetch()
                assert self.verify()
        self._ready = True

    def line(self, encoding="utf-8") -> str:
        """Read the file as a line of text"""
        self.require()
        with open(self.path, "r", encoding=encoding) as f:
            return f.read().rstrip()

    def workbook(self) -> openpyxl.Workbook:
        """Read the file as a xlsx workbook"""
        assert self.path.suffix == ".xlsx"
        self.require()
        return openpyxl.reader.excel.load_workbook(self.path)

    def csv(self, *args, **kwargs) -> pandas.DataFrame:
        """Read the file as csv"""
        assert self.path.suffix == ".csv"
        self.require()
        return pandas.read_csv(self.path, *args, **kwargs)

    def fetch(self) -> None:
        """Fetch the file"""
        if self.url.endswith(".zip"):
            zip_bytes = Download.download(self.url)
            with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zip_file:
                file = zip_file.read(self.path.name)
        else:
            file = Download.download(self.url)
        os.makedirs(self.path.parent, exist_ok=True)
        with open(self.path, "wb") as f:
            f.write(file)

    def verify(self) -> bool:
        """Verify existence and integrity of the file"""
        if self.checksum:
            if isinstance(self.checksum, Download):
                chk = self.checksum.line()
            else:
                chk = self.checksum
            return checksum.sha256(chk, self.path) or checksum.md5(chk, self.path)
        return self.path.exists()

    @staticmethod
    def download(url: str) -> bytes:
        """Download file from an URL"""
        r = requests.get(url, allow_redirects=True, timeout=60)
        assert r.status_code == 200
        return r.content
