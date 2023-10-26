# We import a method from the  modules to address environment variables and 
# we use that method in a function that will return the variables we need from .env 
# to a dictionary we call sql_config

from dotenv import dotenv_values

def get_sql_config():
    '''
        Function loads credentials from .env file and
        returns a dictionary containing the data needed for sqlalchemy.create_engine()
    '''
    needed_keys = ['host', 'port', 'database','user','password']
    dotenv_dict = dotenv_values(".env")
    sql_config = {key:dotenv_dict[key] for key in needed_keys if key in dotenv_dict}
    return sql_config

import pandas as pd
import sqlalchemy 


def get_data(query):
   ''' Connect to the PostgreSQL database server, run query and return data'''
    # get the connection configuration dictionary using the get_sql_config function
   sql_config = get_sql_config()
    # create a connection engine to the PostgreSQL server
   engine = sqlalchemy.create_engine('postgresql://user:pass@host/database',
                        connect_args=sql_config # use dictionary with config details
                        )
    # open a conn session using 'with', execute the query, and return the results
   with engine.begin() as conn: 
      results = conn.execute(query)
   return results.fetchall()


def get_dataframe(sql_query):
    ''' 
    Connect to the PostgreSQL database server, 
    run query and return data as a pandas dataframe
    '''
     # get the connection configuration dictionary using the get_sql_config function
    sql_config = get_sql_config()
    # create a connection engine to the PostgreSQL server
    engine = sqlalchemy.create_engine('postgresql://user:pass@host/database',
                        connect_args=sql_config # use dictionary with config details
                        )
    # open a conn session using 'with', execute the query, and return the results
    return pd.read_sql_query(sql= sql_query, con=engine)

# function to create sqlalchemy engine for writing data to a database
def get_engine():
    sql_config = get_sql_config()
    engine = sqlalchemy.create_engine('postgresql://user:pass@host/database',
                        connect_args=sql_config
                        )
    return engine





# my modified Function for creating tables:  only the return-Statement was commented out...
def get_data_mod(mod_query):
    ''' Connect to the PostgreSQL database server, run query and return data'''
    # get the connection configuration dictionary using the get_sql_config function
    sql_config = get_sql_config()
    # create a connection engine to the PostgreSQL server
    engine = sqlalchemy.create_engine('postgresql://user:pass@host/database',
                                        connect_args=sql_config # use dictionary with config details
                        )
    # open a conn session using 'with', execute the query, and return the results
    with engine.begin() as conn: 
        conn.execute(mod_query)
   #return results.fetchall()                           # just the return statement is commented out


#-----------------------------------------------------------------------------------------------------

# additional import of the geopandas package
import geopandas as gpd

import numpy as np

# shapely.geometry      Package shapely.geomerty is usefull to for checking, weather a point is inside a polygon and converting string type
from shapely import wkt
from shapely.geometry import Polygon, LineString, Point


# creating a function, witch allows us to convert a dataframe into a geodataframe, by specifying the dataframe name and the geometry column

def to_gdf(dataframe, geometry_column):
    '''Input: DataFrame and the Column that has the geometry stored as a string
        Output: geodataframe, with added column named "new_geometry" '''
    new_dataframe = dataframe
    new_dataframe["new_geometry"] = gpd.GeoSeries.from_wkt(dataframe[str(geometry_column)])
    gdf = gpd.GeoDataFrame(new_dataframe, geometry="new_geometry",crs="WGS 84")
    return gdf

# Same Function, but it doesen't add a crs...
def to_gdf_withoutcrs(dataframe, geometry_column):
    '''Input: DataFrame and the Column that has the geometry stored as a string
        Output: geodataframe, with added column named "new_geometry" '''
    new_dataframe = dataframe
    new_dataframe["new_geometry"] = gpd.GeoSeries.from_wkt(dataframe[str(geometry_column)])
    gdf = gpd.GeoDataFrame(new_dataframe, geometry="new_geometry")
    return gdf


def get_bifi(df_trips):
    '''
    Input:  trips dataframe
    Output: returns a Dataframe with columns "area_number" and "rent_return_index", where rent_return_index is the difference between
            total number of trips with specific district as destination and the total number of trips with specific district as starting point
            A negative number indicates, that there more bikes/trips Leaving the area than comming in.'''
    df_rent_return = pd.DataFrame((df_trips["end_area_number"].value_counts() - df_trips["start_area_number"].value_counts()))
    df_rent_return.reset_index(inplace=True)
    df_rent_return.columns = ["area_number", "bifi_index"]
    # how to deal with NaN Values in the rent_return_index column:
    # adding a helper column with
    df_rent_return["isna"] = df_rent_return["bifi_index"].isna()
    
    # Loop that, deals with NaN values, if there are some and calculates the rent_return_index manualy, by looking at the shape of filtered dataframes...
    for i in df_rent_return.index:
        area_number = df_rent_return["area_number"][i]
        #print("area_number: ",area_number)
        #print("index:", i, "value:", test_df.loc[i,"rent_return_index"])
        if df_rent_return["isna"][i] == True:
                df_rent_return.loc[i,"bifi_index"] = (df_trips[df_trips["end_area_number"] == area_number]).shape[0] - (df_trips[df_trips["start_area_number"] == area_number]).shape[0]
    return df_rent_return