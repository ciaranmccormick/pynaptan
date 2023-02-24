import os
from datetime import datetime
from functools import cached_property
from logging import getLogger
from typing import Final, List

from httpx import Client, HTTPStatusError
from lxml import etree
from pydantic import BaseModel, Field

from pynaptan.exceptions import PyNaptanError

logger = getLogger(__name__)

_DEFAULT_URL: Final = "https://naptan.api.dft.gov.uk/v1/nptg"
_NAMESPACE = {None: "http://www.naptan.org.uk/"}
_ADMIN_AREA: Final = "AdministrativeAreas/AdministrativeArea"
_DISTRICTS: Final = "NptgDistricts/NptgDistrict"
NPTG_URL = os.environ.get("NPTG_URL", _DEFAULT_URL)


def clean_tag(tag: str) -> str:
    end = tag.find("}") + 1
    return tag[end:]


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
        xml = etree.fromstring(district)
        district_data = dict(xml.items())
        district_data.update({clean_tag(x.tag): x.text for x in xml.getchildren()})
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
        xml = etree.fromstring(admin_area)
        admin_area_data = dict(xml.items())
        admin_area_data.update({clean_tag(x.tag): x.text for x in xml.getchildren()})
        districts = [
            District.from_string(etree.tounicode(x))
            for x in xml.findall(_DISTRICTS, namespaces=_NAMESPACE)
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
        xml = etree.fromstring(region)
        region_data = dict(xml.items())
        region_data.update({clean_tag(x.tag): x.text for x in xml.getchildren()})
        admin_areas = [
            AdministrativeArea.from_string(etree.tounicode(x))
            for x in xml.findall(_ADMIN_AREA, namespaces=_NAMESPACE)
        ]
        region_data["administrative_areas"] = admin_areas
        return cls.parse_obj(region_data)


class Descriptor(BaseModel):
    """Models for a Locality Descriptor."""

    locality_name: str = Field(..., alias="LocalityName")

    @classmethod
    def from_string(cls, descriptor: str) -> "Descriptor":
        xml = etree.fromstring(descriptor)
        descriptor_data = {}
        descriptor_data.update({clean_tag(x.tag): x.text for x in xml.getchildren()})
        return cls.parse_obj(descriptor_data)


class Translation(BaseModel):
    """Model for a NPTG Translation."""

    easting: int = Field(..., alias="Easting")
    northing: int = Field(..., alias="Northing")
    longitude: float = Field(..., alias="Longitude")
    latitude: float = Field(..., alias="Latitude")

    @classmethod
    def from_string(cls, translation: str) -> "Translation":
        xml = etree.fromstring(translation)
        translation_data = dict(xml.items())
        translation_data.update({clean_tag(x.tag): x.text for x in xml.getchildren()})
        return cls.parse_obj(translation_data)


class Location(BaseModel):
    """Model for NPTG Location."""

    translation: Translation = Field(..., alias="Translation")

    @classmethod
    def from_string(cls, location: str) -> "Location":
        xml = etree.fromstring(location)
        location_data = dict(xml.items())
        translation = etree.tounicode(xml.find("Translation", namespaces=_NAMESPACE))
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
        xml = etree.fromstring(locality)
        locality_data = dict(xml.items())
        locality_data.update({clean_tag(x.tag): x.text for x in xml.getchildren()})
        locality_data["Location"] = Location.from_string(
            etree.tounicode(xml.find("Location", namespaces=_NAMESPACE))
        )
        locality_data["Descriptor"] = Descriptor.from_string(
            etree.tounicode(xml.find("Descriptor", namespaces=_NAMESPACE))
        )
        return cls.parse_obj(locality_data)


class NPTGClient(Client):
    """A client for requesting NPTG data."""

    def __init__(self, url: str = NPTG_URL):
        super().__init__()
        self.url = url

    @cached_property
    def xml(self):
        response = self.get(self.url)
        try:
            response.raise_for_status()
        except HTTPStatusError:
            raise PyNaptanError("Unable to fetch NPTG data.")
        return etree.fromstring(response.text)

    def get_regions(self) -> List[Region]:
        regions = self.xml.find("Regions", namespaces=_NAMESPACE)
        return [Region.from_string(etree.tounicode(r)) for r in regions]

    def get_localities(self) -> List[Locality]:
        localities = self.xml.find("NptgLocalities", namespaces=_NAMESPACE)
        return [Locality.from_string(etree.tounicode(x)) for x in localities]
