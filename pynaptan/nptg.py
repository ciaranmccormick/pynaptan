import os
from datetime import datetime
from functools import cached_property
from logging import getLogger
from typing import Final, List

from defusedxml.ElementTree import fromstring, tostring
from httpx import Client, HTTPStatusError
from pydantic import BaseModel, Field

from pynaptan.exceptions import PyNaptanError

logger = getLogger(__name__)

NSKEY = "ns0"
_DEFAULT_URL: Final = "https://naptan.api.dft.gov.uk/v1/nptg"
_ADMIN_AREA: Final = f"{NSKEY}:AdministrativeAreas/{NSKEY}:AdministrativeArea"
_DISTRICTS: Final = f"{NSKEY}:NptgDistricts/{NSKEY}:NptgDistrict"
NPTG_URL = os.environ.get("NPTG_URL", _DEFAULT_URL)
TRANSLATION = f"{NSKEY}:Translation"
namespace = {NSKEY: "http://www.naptan.org.uk/"}


def _clean_tag(tag: str) -> str:
    """Remove namespace from tag name."""
    end = tag.find("}") + 1
    return tag[end:]


def _to_unicode(xml) -> str:
    """Return an Element as a unicode string."""
    return tostring(xml, encoding="unicode")


class NPTGBaseModel(BaseModel):
    """BaseModel for all NPTG models."""

    creation_date_time: datetime = Field(..., alias="CreationDateTime")
    revision_number: int = Field(..., alias="RevisionNumber")
    modification_date_time: datetime = Field(..., alias="ModificationDateTime")
    modification: str = Field("", alias="Modification")


class District(NPTGBaseModel):
    """Model for Districts."""

    nptg_district_code: str = Field(..., alias="NptgDistrictCode")
    name: str = Field(..., alias="Name")

    @classmethod
    def from_string(cls, district: str) -> "District":
        """Return District from xml string."""
        xml = fromstring(district)
        district_data = dict(xml.items())
        district_data.update({_clean_tag(child.tag): child.text for child in xml})
        return cls.parse_obj(district_data)


class AdministrativeArea(NPTGBaseModel):
    """Model for Admin Areas."""

    administrative_area_code: str = Field(..., alias="AdministrativeAreaCode")
    atco_area_code: str = Field(..., alias="AtcoAreaCode")
    area_name_lang: str = Field("", alias="AreaNameLang")
    name: str = Field(..., alias="Name")
    short_name: str = Field(..., alias="ShortName")
    national: int = Field(..., alias="National")
    districts: List[District]

    @classmethod
    def from_string(cls, admin_area: str) -> "AdministrativeArea":
        """Return AdministrativeArea from xml string."""
        xml = fromstring(admin_area)
        admin_area_data = dict(xml.items())
        admin_area_data.update({_clean_tag(child.tag): child.text for child in xml})
        districts = [
            District.from_string(_to_unicode(district))
            for district in xml.findall(_DISTRICTS, namespaces=namespace)
        ]
        admin_area_data["districts"] = districts
        return cls.parse_obj(admin_area_data)


class Region(NPTGBaseModel):
    """Model for Region."""

    region_code: str = Field(..., alias="RegionCode")
    name: str = Field(..., alias="Name")
    country: str = Field(..., alias="Country")
    administrative_areas: List[AdministrativeArea]

    @classmethod
    def from_string(cls, region: str) -> "Region":
        """Return Region from xml string."""
        xml = fromstring(region)
        region_data = dict(xml.items())
        region_data.update({_clean_tag(child.tag): child.text for child in xml})
        admin_areas = [
            AdministrativeArea.from_string(_to_unicode(element))
            for element in xml.findall(_ADMIN_AREA, namespaces=namespace)
        ]
        region_data["administrative_areas"] = admin_areas
        return cls.parse_obj(region_data)


class Descriptor(BaseModel):
    """Models for a Locality Descriptor."""

    locality_name: str = Field(..., alias="LocalityName")

    @classmethod
    def from_string(cls, descriptor: str) -> "Descriptor":
        """Return Descriptor from xml string."""
        xml = fromstring(descriptor)
        descriptor_data = {}
        descriptor_data.update({_clean_tag(child.tag): child.text for child in xml})
        return cls.parse_obj(descriptor_data)


class Translation(BaseModel):
    """Model for a NPTG Translation."""

    easting: int = Field(..., alias="Easting")
    northing: int = Field(..., alias="Northing")
    longitude: float = Field(..., alias="Longitude")
    latitude: float = Field(..., alias="Latitude")

    @classmethod
    def from_string(cls, translation: str) -> "Translation":
        """Return Translation from xml string."""
        xml = fromstring(translation)
        translation_data = dict(xml.items())
        translation_data.update({_clean_tag(child.tag): child.text for child in xml})
        return cls.parse_obj(translation_data)


class Location(BaseModel):
    """Model for NPTG Location."""

    translation: Translation = Field(..., alias="Translation")

    @classmethod
    def from_string(cls, location: str) -> "Location":
        """Return Location from xml string."""
        xml = fromstring(location)
        location_data = dict(xml.items())
        translation = _to_unicode(xml.find(TRANSLATION, namespaces=namespace))
        location_data["Translation"] = Translation.from_string(translation)
        return cls.parse_obj(location_data)


class Locality(NPTGBaseModel):
    """Model for Localities."""

    nptg_locality_code: str = Field(..., alias="NptgLocalityCode")
    administrative_area_ref: str = Field(..., alias="AdministrativeAreaRef")
    nptg_district_ref: int = Field(..., alias="NptgDistrictRef")
    source_locality_type: str = Field(..., alias="SourceLocalityType")
    location: Location = Field(..., alias="Location")
    descriptor: Descriptor = Field(..., alias="Descriptor")

    @classmethod
    def from_string(cls, locality: str) -> "Locality":
        """Return Locality from xml string."""
        xml = fromstring(locality)
        locality_data = dict(xml.items())
        locality_data.update({_clean_tag(child.tag): child.text for child in xml})
        locality_data["Location"] = Location.from_string(
            _to_unicode(xml.find(f"{NSKEY}:Location", namespaces=namespace))
        )
        locality_data["Descriptor"] = Descriptor.from_string(
            _to_unicode(xml.find(f"{NSKEY}:Descriptor", namespaces=namespace))
        )
        return cls.parse_obj(locality_data)


class NPTGClient(Client):
    """A client for requesting NPTG data."""

    def __init__(self, url: str = NPTG_URL):
        """A HTTP client for retrieving NPTG data."""
        super().__init__()
        self.url = url

    @cached_property
    def xml(self):
        """Return NPTG data as an xml Element."""
        response = self.get(self.url)
        try:
            response.raise_for_status()
        except HTTPStatusError:
            raise PyNaptanError("Unable to fetch NPTG data.")
        return fromstring(response.text)

    def get_regions(self) -> List[Region]:
        """Return a list of Regions."""
        regions = self.xml.find(f"{NSKEY}:Regions", namespaces=namespace)
        return [Region.from_string(_to_unicode(region)) for region in regions]

    def get_localities(self) -> List[Locality]:
        """Return a list of Localities."""
        localities = self.xml.find(f"{NSKEY}:NptgLocalities", namespaces=namespace)
        return [Locality.from_string(_to_unicode(locality)) for locality in localities]
