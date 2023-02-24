# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_load_locality 1'] = '''{
  "creation_date_time": "2022-08-25T10:28:30.233000",
  "revision_number": 0,
  "modification_date_time": "2022-08-25T10:28:30.310000",
  "modification": "new",
  "nptg_locality_code": "N0081215",
  "administrative_area_ref": "085",
  "nptg_district_ref": 68,
  "source_locality_type": "Add",
  "location": {
    "translation": {
      "easting": 549324,
      "northing": 223098,
      "longitude": 0.1682994,
      "latitude": 51.88645
    }
  },
  "descriptor": {
    "locality_name": "St Michael\\u2019s Hurst "
  }
}'''

snapshots['test_load_region 1'] = '''{
  "creation_date_time": "2006-01-25T07:54:31",
  "revision_number": 0,
  "modification_date_time": "2006-01-25T07:54:31",
  "modification": "",
  "region_code": "NE",
  "name": "North East",
  "country": "England",
  "administrative_areas": [
    {
      "creation_date_time": "2006-01-25T07:54:33",
      "revision_number": 0,
      "modification_date_time": "2006-01-25T07:54:33",
      "modification": "",
      "administrative_area_code": "015",
      "atco_area_code": "076",
      "area_name_lang": "",
      "name": "Darlington",
      "short_name": "Darlington",
      "national": 0,
      "districts": []
    },
    {
      "creation_date_time": "2006-01-25T07:54:33",
      "revision_number": 0,
      "modification_date_time": "2006-01-25T07:54:33",
      "modification": "",
      "administrative_area_code": "022",
      "atco_area_code": "075",
      "area_name_lang": "",
      "name": "Hartlepool",
      "short_name": "Hartlepool",
      "national": 0,
      "districts": []
    },
    {
      "creation_date_time": "2006-01-25T07:54:33",
      "revision_number": 0,
      "modification_date_time": "2006-01-25T07:54:33",
      "modification": "",
      "administrative_area_code": "031",
      "atco_area_code": "079",
      "area_name_lang": "",
      "name": "Middlesbrough",
      "short_name": "Middlesbrough",
      "national": 0,
      "districts": []
    },
    {
      "creation_date_time": "2006-01-25T07:54:33",
      "revision_number": 1,
      "modification_date_time": "2006-03-10T12:38:33",
      "modification": "revise",
      "administrative_area_code": "047",
      "atco_area_code": "078",
      "area_name_lang": "",
      "name": "Redcar & Cleveland",
      "short_name": "Cleveland",
      "national": 0,
      "districts": []
    },
    {
      "creation_date_time": "2006-01-25T07:54:33",
      "revision_number": 0,
      "modification_date_time": "2006-01-25T07:54:33",
      "modification": "",
      "administrative_area_code": "054",
      "atco_area_code": "077",
      "area_name_lang": "",
      "name": "Stockton-on-Tees",
      "short_name": "Stockton",
      "national": 0,
      "districts": []
    },
    {
      "creation_date_time": "2006-01-25T07:54:33",
      "revision_number": 0,
      "modification_date_time": "2006-01-25T07:54:33",
      "modification": "",
      "administrative_area_code": "078",
      "atco_area_code": "130",
      "area_name_lang": "",
      "name": "Durham",
      "short_name": "Durham",
      "national": 0,
      "districts": [
        {
          "creation_date_time": "2006-01-25T07:54:36",
          "revision_number": 1,
          "modification_date_time": "2009-04-20T21:45:53.590000",
          "modification": "delete",
          "nptg_district_code": "42",
          "name": "Chester-le-Street"
        },
        {
          "creation_date_time": "2006-01-25T07:54:36",
          "revision_number": 1,
          "modification_date_time": "2009-04-20T21:45:53.590000",
          "modification": "delete",
          "nptg_district_code": "60",
          "name": "Derwentside"
        },
        {
          "creation_date_time": "2006-01-25T07:54:36",
          "revision_number": 1,
          "modification_date_time": "2009-04-20T21:45:53.590000",
          "modification": "delete",
          "nptg_district_code": "62",
          "name": "Durham"
        },
        {
          "creation_date_time": "2006-01-25T07:54:36",
          "revision_number": 1,
          "modification_date_time": "2009-04-20T21:45:53.590000",
          "modification": "delete",
          "nptg_district_code": "63",
          "name": "Easington"
        },
        {
          "creation_date_time": "2006-01-25T07:54:36",
          "revision_number": 1,
          "modification_date_time": "2009-04-20T21:45:53.590000",
          "modification": "delete",
          "nptg_district_code": "166",
          "name": "Sedgefield"
        },
        {
          "creation_date_time": "2006-01-25T07:54:36",
          "revision_number": 1,
          "modification_date_time": "2009-04-20T21:45:53.590000",
          "modification": "delete",
          "nptg_district_code": "201",
          "name": "Teesdale"
        },
        {
          "creation_date_time": "2006-01-25T07:54:36",
          "revision_number": 1,
          "modification_date_time": "2009-04-20T21:45:53.590000",
          "modification": "delete",
          "nptg_district_code": "221",
          "name": "Wear Valley"
        }
      ]
    },
    {
      "creation_date_time": "2006-01-25T07:54:33",
      "revision_number": 0,
      "modification_date_time": "2006-01-25T07:54:33",
      "modification": "",
      "administrative_area_code": "094",
      "atco_area_code": "310",
      "area_name_lang": "",
      "name": "Northumberland",
      "short_name": "Northumberland",
      "national": 0,
      "districts": [
        {
          "creation_date_time": "2006-01-25T07:54:36",
          "revision_number": 1,
          "modification_date_time": "2009-04-20T21:45:53.590000",
          "modification": "delete",
          "nptg_district_code": "3",
          "name": "Alnwick"
        },
        {
          "creation_date_time": "2006-01-25T07:54:36",
          "revision_number": 1,
          "modification_date_time": "2009-04-20T21:45:53.590000",
          "modification": "delete",
          "nptg_district_code": "15",
          "name": "Berwick-upon-Tweed"
        },
        {
          "creation_date_time": "2006-01-25T07:54:36",
          "revision_number": 1,
          "modification_date_time": "2009-04-20T21:45:53.590000",
          "modification": "delete",
          "nptg_district_code": "17",
          "name": "Blyth Valley"
        },
        {
          "creation_date_time": "2006-01-25T07:54:36",
          "revision_number": 1,
          "modification_date_time": "2009-04-20T21:45:53.590000",
          "modification": "delete",
          "nptg_district_code": "35",
          "name": "Castle Morpeth"
        },
        {
          "creation_date_time": "2006-01-25T07:54:36",
          "revision_number": 1,
          "modification_date_time": "2009-04-20T21:45:53.590000",
          "modification": "delete",
          "nptg_district_code": "211",
          "name": "Tynedale"
        },
        {
          "creation_date_time": "2006-01-25T07:54:36",
          "revision_number": 1,
          "modification_date_time": "2009-04-20T21:45:53.590000",
          "modification": "delete",
          "nptg_district_code": "215",
          "name": "Wansbeck"
        }
      ]
    },
    {
      "creation_date_time": "2006-01-25T07:54:33",
      "revision_number": 1,
      "modification_date_time": "2006-03-10T12:38:33",
      "modification": "revise",
      "administrative_area_code": "103",
      "atco_area_code": "410",
      "area_name_lang": "",
      "name": "Tyne & Wear",
      "short_name": "Tyne & Wear",
      "national": 0,
      "districts": [
        {
          "creation_date_time": "2006-01-25T07:54:36",
          "revision_number": 0,
          "modification_date_time": "2006-01-25T07:54:36",
          "modification": "",
          "nptg_district_code": "249",
          "name": "Gateshead"
        },
        {
          "creation_date_time": "2006-01-25T07:54:36",
          "revision_number": 0,
          "modification_date_time": "2006-01-25T07:54:36",
          "modification": "",
          "nptg_district_code": "255",
          "name": "Newcastle upon Tyne"
        },
        {
          "creation_date_time": "2006-01-25T07:54:36",
          "revision_number": 0,
          "modification_date_time": "2006-01-25T07:54:36",
          "modification": "",
          "nptg_district_code": "256",
          "name": "North Tyneside"
        },
        {
          "creation_date_time": "2006-01-25T07:54:36",
          "revision_number": 0,
          "modification_date_time": "2006-01-25T07:54:36",
          "modification": "",
          "nptg_district_code": "265",
          "name": "South Tyneside"
        },
        {
          "creation_date_time": "2006-01-25T07:54:36",
          "revision_number": 0,
          "modification_date_time": "2006-01-25T07:54:36",
          "modification": "",
          "nptg_district_code": "268",
          "name": "Sunderland"
        }
      ]
    }
  ]
}'''
