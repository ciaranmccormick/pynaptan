from pynaptan.nptg import Locality, Region


def test_load_region(snapshot, region_string):
    """Test regions can be loaded correctly."""
    region = Region.from_string(region_string)
    snapshot.assert_match(region.json(indent=2))


def test_load_locality(snapshot):
    """Test localities can be loaded correctly."""
    xml = """
      <NptgLocality
        xmlns="http://www.naptan.org.uk/"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        CreationDateTime="2022-08-25T10:28:30.233"
        ModificationDateTime="2022-08-25T10:28:30.310"
        RevisionNumber="0"
        Modification="new">
          <NptgLocalityCode>N0081215</NptgLocalityCode>
          <Descriptor>
              <LocalityName xml:lang="EN">St Michael’s Hurst </LocalityName>
          </Descriptor>
          <AdministrativeAreaRef>085</AdministrativeAreaRef>
          <NptgDistrictRef>68</NptgDistrictRef>
          <SourceLocalityType>Add</SourceLocalityType>
          <Location>
              <Translation>
                  <Easting>549324</Easting>
                  <Northing>223098</Northing>
                  <Longitude>0.1682994</Longitude>
                  <Latitude>51.88645</Latitude>
              </Translation>
          </Location>
      </NptgLocality>
    """
    locality = Locality.from_string(xml)
    snapshot.assert_match(locality.json(indent=2))
