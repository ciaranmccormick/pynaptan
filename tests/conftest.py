from pathlib import Path
from unittest.mock import patch

import pytest
from pretend import stub

from pynaptan.naptan import Naptan
from pynaptan.nptg import NPTG, NPTGClient

DATA_DIR = Path(__file__).parent / "data"


@pytest.fixture()
def stops_csv():
    csv_path = DATA_DIR / "stops.csv"
    with csv_path.open("r") as f:
        yield f.read()


@pytest.fixture()
def naptan(stops_csv):
    response = stub(raise_for_status=lambda: True, text=stops_csv)
    with patch.object(Naptan, "get", return_value=response):
        yield Naptan()


@pytest.fixture()
def nptg_zip_bytes() -> bytes:
    zip_path = DATA_DIR / "Nptgcsv.zip"
    with zip_path.open("rb") as zip:
        return zip.read()


@pytest.fixture()
def nptg(nptg_zip_bytes):
    response = stub(raise_for_status=lambda: True, content=nptg_zip_bytes)
    with patch.object(NPTGClient, "get", return_value=response):
        yield NPTG(NPTGClient())
