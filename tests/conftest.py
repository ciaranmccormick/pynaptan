from pathlib import Path
from unittest.mock import patch

import pytest
from pretend import stub

from pynaptan.naptan import Naptan
from pynaptan.nptg import NPTGClient

DATA_DIR = Path(__file__).parent / "data"
SESSION = "session"


@pytest.fixture(scope=SESSION)
def stops_csv():
    """Return contents of the stops.csv."""
    csv_path = DATA_DIR / "stops.csv"
    with csv_path.open("r") as csv_file:
        yield csv_file.read()


@pytest.fixture(scope=SESSION)
def naptan(stops_csv):
    """Return a patch Naptan object."""
    response = stub(raise_for_status=lambda: True, text=stops_csv)
    with patch.object(Naptan, "get", return_value=response):
        yield Naptan()


@pytest.fixture(scope=SESSION)
def localities_xml() -> str:
    """Return the nptg zip as bytes."""
    xml_path = DATA_DIR / "localities.xml"
    with xml_path.open("r") as xml_file:
        return xml_file.read()


@pytest.fixture(scope=SESSION)
def region_string() -> str:
    """Return the nptg zip as bytes."""
    xml_path = DATA_DIR / "region.xml"
    with xml_path.open("r") as xml_file:
        return xml_file.read()


@pytest.fixture(scope=SESSION)
def nptg(nptg_xml):
    """Return a patched NPTGClient."""
    response = stub(raise_for_status=lambda: True, text=nptg_xml)
    with patch.object(NPTGClient, "get", return_value=response):
        yield NPTGClient()
