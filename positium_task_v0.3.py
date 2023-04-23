# import geopandas module
import geopandas as gpd
# Import function 'make_valid' from shapely module
from shapely.validation import make_valid
# Import CRS function
from fiona.crs import from_epsg
# Import these function to download and extract data from URL
import requests
import zipfile
from io import BytesIO

# Data has been downloaded form naturalearthdata and kept in github
# Site URL - https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/50m/cultural/ne_50m_admin_0_countries.zip

download_countries = 'https://github.com/soniadas123/Geometries/blob/main/ne_50m_admin_0_countries.zip?raw=true'
# Get the Exact file name by splitting the URL last part
zipname = download_countries.split('/')[-1]
r = requests.get(download_countries)

# Extracting the zip file contents
# Create a directory where you want to save final shapefile
zipfile = zipfile.ZipFile(BytesIO(r.content))
zipfile.extractall('C:\\python\\ne_50m_admin_0_countries\\')

# Locate an open-source geospatial database which geometries of countries could be downloaded from. Preferably a single location for all countries.
# Geometries should not be too large, the range of the total size of downloadable geometries: 1MB ... 100MB.

shape_countries = "C:\\python\\ne_50m_admin_0_countries\\ne_50m_admin_0_countries.shp"
# Read the data from the shape files
data_countries = gpd.read_file(shape_countries)

# Selecting the required column
data_countries1 = data_countries[['SOVEREIGNT', 'ISO_A2', 'geometry']]
# Setting the correct geometry for the column 'gepmetry'
# Checks for the validity of the geometries, corrects them if necessary
# If some geometries are not valid, remove these from the list.
for index, row in data_countries1.iterrows():
    if row['geometry'].is_valid == True:
        data_countries1.loc[index, 'geometry'] = row['geometry']
    elif row['geometry'].is_valid == False:
        make_valid(data_countries1.loc[index, 'geometry'])
    else:
        data_countries1.drop(data_countries1.index[row])

# For each (or at least for as many as possible) country codes in the provided ISO_A2 list, there should be a geometry (multipolygon) in WGS84 (srs=4326), which is valid.
data_countries1['geometry'].crs = from_epsg(4326)

# Download the shapefiles for the QGIS usage
data_countries1.to_file('C:\\python\\ne_50m_admin_0_countries\\final.shp')

# # Download also in csv to use in R Programming
# data_countries1.to_csv(
#     'C:\\tools\\ne_50m_admin_0_countries\\final.csv', index=False)