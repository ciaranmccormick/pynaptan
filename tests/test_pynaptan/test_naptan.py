from unittest.mock import MagicMock, patch

import pytest
from httpx import HTTPStatusError, Request, Response
from pretend import raiser, stub

from pynaptan.exceptions import PyNaptanError
from pynaptan.naptan import Naptan


def test_load_stops(naptan: Naptan, snapshot):
    """Test that stops are loaded."""
    stops = list(naptan.iget_all_stops())
    assert stops
    snapshot.assert_match(stops)


def test_iload_stops_exception():
    """Test when loading stops throws exceptions."""
    mrequest = MagicMock(spec=Request)
    mresponse = MagicMock(spec=Response)
    error = HTTPStatusError(message="Message", request=mrequest, response=mresponse)
    response = stub(raise_for_status=raiser(error))
    with patch.object(Naptan, "get", return_value=response):
        with pytest.raises(PyNaptanError) as exc:
            Naptan().iget_all_stops()
            assert str(exc.value) == "Unable to load stops."
