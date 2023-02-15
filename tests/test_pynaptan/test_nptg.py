from unittest.mock import Mock, patch

import pytest
from httpx import HTTPStatusError, Request, Response
from pretend import raiser, stub

from pynaptan.exceptions import PyNaptanError
from pynaptan.nptg import NPTGClient


def test_load_regions(nptg, snapshot):
    regions = nptg.get_regions()
    snapshot.assert_match(regions)


def test_load_admin_areas(nptg, snapshot):
    admin_areas = nptg.get_admin_areas()
    assert len(admin_areas) > 0
    snapshot.assert_match(admin_areas)


def test_load_localities(nptg, snapshot):
    localities = nptg.get_localities()
    assert len(localities) > 0
    snapshot.assert_match(localities)


def test_load_districts(nptg, snapshot):
    districts = nptg.get_districts()
    assert len(districts) > 0
    snapshot.assert_match(districts)


def test_get_zipdata_exception():
    response = Mock(spec=Response)
    request = Mock(spec=Request)
    error = HTTPStatusError(message="Message", request=request, response=response)
    response = stub(raise_for_status=raiser(error))
    with patch.object(NPTGClient, "get", return_value=response):
        with pytest.raises(PyNaptanError) as exc:
            NPTGClient().get_zipdata()
        assert str(exc.value) == "Unable to fetch NPTG data."
