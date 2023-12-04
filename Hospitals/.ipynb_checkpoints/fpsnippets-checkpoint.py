import geopandas
import pandas
from shapely.geometry import Point

# Load neighborhoods
NEIGHBORHOODS = geopandas.read_file("https://data.wprdc.org/dataset/e672f13d-71c4-4a66-8f38-710e75ed80a4/resource/c5a93a8e-03d7-4eb3-91a8-c6b7db0fa261/download/pittsburghpaneighborhoods-.zip")
# Load zip codes
ZIPS = geopandas.read_file("https://data.wprdc.org/dataset/1a5135de-cabe-4e23-b5e4-b2b8dd733817/resource/ec228c0e-6b1e-4f44-a335-df05546d52ea/download/alcogisallegheny-county-zip-code-boundaries.zip")

def geo_to_neighborhood(latitude, longitude):
    """Converts a geolocation (latitude and longitude) to a Pittsburgh neighborhood name.

    Args:
        latitude (float): The latitude of the point.
        longitude (float): The longitude of the point.

    Returns:
        Union[str, None]: Name of the Pittsburgh neighborhood the point falls within or None if it does not fall within a neighborhood.
    """
    # Create a shapely point for the latitude and longitude
    pt = Point(longitude, latitude)
    # Loop through the neighborhoods
    for _idx, neighborhood in NEIGHBORHOODS.iterrows():
        # Check if this neighborhood contains the point
        if neighborhood["geometry"].contains(pt):
            # Return the name of the neighborhood
            return neighborhood["hood"]
    # Wasn't contained in the neighborhood
    return None

def zip_to_neighborhoods(zip_code):
    """Converts a ZIP code to a list of Pittsburgh neighborhood names.

    Args:
        zip_code (int): The ZIP code of interest.

    Returns:
        list[str]: A list of neighborhood names within that ZIP code.
    """
    # Get this specific zip
    zips_filtered = ZIPS[ZIPS["ZIP"] == str(zip_code)]
    if len(zips_filtered) < 1:
        return None
    zp = zips_filtered.iloc[0]
    # List of neighborhoods for this zip
    zp_neighborhoods = []
    # Loop through the neighborhoods
    for _idx, neighborhood in NEIGHBORHOODS.iterrows():
        # Check if this zip intersects the neighborhood
        if neighborhood["geometry"].intersects(zp["geometry"]):
            # Add this neighborhood to the list
            zp_neighborhoods.append(neighborhood["hood"])
    return zp_neighborhoods

def census_to_neighborhoods(census_tract):
    """Converts a census tract number to a list of Pittsburgh neighborhoods.

    Args:
        census_tract (int): The Census tract of interest. 

    Returns:
        list[str]: A list of Pittsburgh neighborhood names that 
    """
    # Census to ZIP data
    census_data = pandas.read_csv("./ZIP_TRACT_032020.csv")
    tract_filtered = census_data[census_data["TRACT"] == census_tract]
    if len(tract_filtered) < 1:
        return []
    tract = tract_filtered.iloc[0]
    return zip_to_neighborhoods(int(tract["ZIP"]))