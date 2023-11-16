# Divvy_Bikeshare_Chicago

This project focusses on the analysis of data from a bike sharing company called Divvy located in Chicago. 

In the following, i will give a short introduction for every Notebook in this repository.

#### Notebook: 01_get_trip_data
    * 1. Unzip monthly tripdata 
    * 2. Creating a DataFrame with every trip in 2022
    * 3. Cleaning Data/ changing datatypes
    * 4. Push to sql database/store as csv on local machine

#### Notebook: 01_get_stations_data
    * 1. Creating json object from divvy stations feed
    * 2. Convert json object to a DataFrame
    * 3. Clean Dataframe
    * 4. Convert to a GeoDataframe (by converting latitude and longitude to a geometrical point via shapely package)
    * 5. Upload to SQL database

#### Notebook: 01_get_geodata_districts_chicago
Creating a GeoPandas GeoDataFrame for all districts of Chicago. These shapely Polygon will be the basis for any interactive maps of Chicago i will be creating in this Project.

    * 1. Loading data into DataFrame
    * 2. Cleaning Data
    * 3. Adding the geometry of the City of Evanston (north end of Chicago) to the DataFrame, since Divvy operates also in this area
    * 4. Converting dataframe to geodataframe
    * 5. Visualizing District areas on interactive map
    * 6. Upload to SQL Database

#### Notebook: 01_get_socioeconomic_data
    * 1. Downloading Census data of the city of chicago from 2016 to 2020
    * 2. Cleaning Data
    * 3. Upload to SQL Database and save as csv on localy

#### Notebook: 02_merge_areas_trips_data
Goal: For every Trip in 2022, i want to identify the community area the trip started in and where it ended. Then, i want to add this information to the trips table for every trip.

    * 1. For every trip, take "start_lat" and "start_lon", and create a Geometrical Point
    * 2. Do the same thing with end_lat and end_lon.
    * 3. Use community districts Polygon data (see notebook 01_get_geodata_districts_chicago.ipynb)
    * 4. Perform a spatial join, to match points (start/end)  and polygons (districts).
    * 5. Upload to Sql DataBase

#### Notebook: 03_linear_distance
Goal: Calculate linear distance from start to end point for every trip in 2022

    Since Divvy does not provide data about the distance traveled in each trip, I will calculate the linear distance of the starting and ending location. 

    * 1. Load SQL Trips Table into Dataframe and transform to GeoDataFrame
    * 2. Create a shapelly Linestring that connects the start and endpoint
    * 3. Calculate the length of each Linestring
    * 4. Basic visualization (Distribution of linear distances of all Trips)

#### Notebook: 04_bikeflow_index
Goal: I want to find general tendencies of the fleet movement over time through the City of Chicago. For that, i will create and calculate the Bikeflow-Index for every District of Chicago:

The Bikeflow-Index is a positive or negative number, depending on whether a district "loses" or "gains" Bikes over a specific time period. The Bikeflow-Index for a specific District is calculated by adding up all trips that end in this district and substracting the number of trips starting in this district. That way, trips that start and end in the same district, don't have any effect on the Bikeflow-Index.

A District with a strong negative Bikeflow Index needs to be resupplied with bikes from districts with positive Bikeflow indexes.


    * 1. Loading community_areas table and 2022_trips data into DataFrames
    * 2. creating function, that calculates the Bikeflow-Index (BiFi) for every District of Chicago
    * 3. Create Heatmap of Bikeflow-Index
    * 4. Identifying patterns of customer behavior by looking at the Bikeflow-Index for specific time periods(Mornings vs. Afternoons)



To be able to see all the Visualizations in the Notebooks, use this Link:
[Notebook Viewer](https://nbviewer.org/github/Brettmett/Divvy_Bikeshare_Chicago/tree/main/)

## Data Sources
- Divvy Tripdata: [Divvy Trip Data](https://divvy-tripdata.s3.amazonaws.com/index.html)
- Bikeways Chicago: [Chicago Bikeways](https://data.cityofchicago.org/Transportation/Bike-Routes/3w5d-sru8)
- Geodata City of Chicago: [Community Areas Boundraries Chicago](https://data.cityofchicago.org/Facilities-Geographic-Boundaries/Boundaries-Community-Areas-current-/cauq-8yn6)
- Geodata Evanston: [Gespatial Data Evanston](https://data.cityofevanston.org/Information-Technology-includes-maps-geospatial-da/The-City-of-Evanston/4qkz-evsc)

