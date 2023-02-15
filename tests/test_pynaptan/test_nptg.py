from unittest.mock import Mock, patch

import pytest
from httpx import HTTPStatusError, Request, Response
from pretend import raiser, stub

from pynaptan.exceptions import PyNaptanError
from pynaptan.nptg import NPTGClient


def test_load_regions(nptg, snapshot):
    """Test regions can be loaded correctly."""
    regions = nptg.get_regions()
    snapshot.assert_match(regions)


def test_load_admin_areas(nptg, snapshot):
    """Test admin areas can be loaded correctly."""
    admin_areas = nptg.get_admin_areas()
    assert admin_areas
    snapshot.assert_match(admin_areas)


def test_load_localities(nptg, snapshot):
    """Test localities can be loaded correctly."""
    localities = nptg.get_localities()
    assert localities
    snapshot.assert_match(localities)


def test_load_districts(nptg, snapshot):
    """Test districts can be loaded correctly."""
    districts = nptg.get_districts()
    assert districts
    snapshot.assert_match(districts)


def test_get_zipdata_exception():
    """Test that nptg can handle exceptions."""
    response = Mock(spec=Response)
    request = Mock(spec=Request)
    error = HTTPStatusError(message="Message", request=request, response=response)
    response = stub(raise_for_status=raiser(error))
    with patch.object(NPTGClient, "get", return_value=response):
        with pytest.raises(PyNaptanError) as exc:
            NPTGClient().get_zipdata()
            assert str(exc.value) == "Unable to fetch NPTG data."
