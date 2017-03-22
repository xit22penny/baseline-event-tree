__author__ = 'Xian Teng'

import time
import csv
import pandas as pd
from datetime import datetime


def extract_dataframe(year, start_month, end_month):
    prefix_csv_name = "~/ny-cab/yellow_tripdata_" + str(year) + "-"
    # prefix_csv_name = "/Users/xianteng/Downloads/yellow_tripdata_" + str(year) + "-"
    df_cab = pd.DataFrame()
    fields = ['tpep_pickup_datetime', 'tpep_dropoff_datetime', 'pickup_longitude', 'pickup_latitude', 'dropoff_longitude', 'dropoff_latitude']
    # fields = [' pickup_datetime', ' dropoff_datetime', ' pickup_longitude', ' pickup_latitude', ' dropoff_longitude', ' dropoff_latitude']
    for i in range(start_month,end_month+1):
        current_csv_name = prefix_csv_name + format(i,'02d') + ".csv"
        print "--- extracting data from ", current_csv_name, " ---"
        df = pd.read_csv(current_csv_name, usecols = fields)
        df_cab = df_cab.append(df, ignore_index = True)

    df_cab.columns = ['pickup_datetime','dropoff_datetime','pickup_longitude','pickup_latitude','dropoff_longitude','dropoff_latitude']
    df_cab['pickup_datetime'] = pd.to_datetime(df_cab['pickup_datetime'])
    df_cab['weekday'] = df_cab['pickup_datetime'].dt.dayofweek
    df_cab['month'] = df_cab['pickup_datetime'].dt.month
    df_cab['day'] = df_cab['pickup_datetime'].dt.day
    
    return df_cab