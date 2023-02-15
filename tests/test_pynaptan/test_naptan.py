from unittest.mock import MagicMock, patch
from httpx import HTTPStatusError, Request, Response
from pretend import raiser, stub
import pytest
from pynaptan.exceptions import PyNaptanError
from pynaptan.naptan import Naptan


def test_load_stops(naptan: Naptan, snapshot):
    """Test that stops are loaded."""
    stops = [stop for stop in naptan.iload_from_api()]
    assert len(stops) > 0
    snapshot.assert_match(stops)


def test_iload_stops_exception():
    mrequest = MagicMock(spec=Request)
    mresponse = MagicMock(spec=Response)
    error = HTTPStatusError(message="Message", request=mrequest, response=mresponse)
    response = stub(raise_for_status=raiser(error))
    with patch.object(Naptan, "get", return_value=response):
        with pytest.raises(PyNaptanError) as exc:
            Naptan().iload_from_api()
        assert str(exc.value) == "Unable to load stops."
