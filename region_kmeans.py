__author__ = 'Xian Teng'

import pandas as pd
import datetime
import networkx as nx
import numpy as np
import random
import time
from scipy.cluster.vq import vq, kmeans2, whiten

# get adjacency matrix storing distance between two centroids
def get_adjacency_matrix(centroid):
    nCentroids = len(centroid)
    adj_matrix = np.zeros((nCentroids,nCentroids)) # a nCentroids by nCentroids adjacency matrix
    for i in range(0,nCentroids):
        for j in range(i+1,nCentroids):
            adj_matrix[i,j] = np.linalg.norm(centroid[i] - centroid[j]) # calculate distance
            adj_matrix[j,i] = adj_matrix[i,j]

    return adj_matrix

# find normal centroids and check-in levels
def find_normal_pattern(df_cab,year,start_month,end_month,wkd,nclusters):
    poi = df_cab[df_cab['weekday'] == wkd]
    ndays = len(poi.groupby(['day','month']).count())
    poi_pick = poi[['pickup_longitude','pickup_latitude']] # pickup locations
    poi_drop = poi[['dropoff_longitude','dropoff_latitude']] # dropoff locations
    poi_pick.columns = ['longitude','latitude']
    poi_drop.columns = ['longitude','latitude']
    # poi_pick['tag'] = ['pick']*len(poi_pick) # add tags
    # poi_drop['tag'] = ['drop']*len(poi_drop)
    poi = pd.concat([poi_pick,poi_drop]) # concatenate two dataframes
    
    poi = poi[(poi['longitude'] > -74.4) & (poi['longitude'] < -73.6) & (poi['latitude'] > 40.4) & (poi['latitude'] < 41.0)]
    print("--- start performing k-means clustering for %s ---" % wkd)
    start_time = time.time()
    centroids, labels = kmeans2(np.array(poi[['longitude','latitude']]), nclusters) # k-means
    
    pick_counts = pd.value_counts(pd.DataFrame(labels[0:(len(poi_pick)-1)])[0].values, sort = False) # get normal check-ins counts
    pick_counts = pick_counts/ndays
    pick_counts = pick_counts.sort_index()
    
    drop_counts = pd.value_counts(pd.DataFrame(labels[len(poi_pick):len(poi)])[0].values, sort = False)
    drop_counts = drop_counts/ndays
    drop_counts = drop_counts.sort_index()

    adj_matrix = get_adjacency_matrix(centroids) # --- get adjacency matrix --- #
    end_time = time.time()
    print("--- k-means costs %s seconds ---" % (end_time - start_time))
    
    print "--- outputing data --- "
    midstr = format(year,'04d')+"-"+format(start_month,'02d')+"-"+format(end_month,'02d')+"-"+format(wkd,'01d')
    np.savetxt("normal_data/centroids-"+midstr+".txt",centroids)
    np.savetxt("normal_data/adj_matrix-"+midstr+".txt",adj_matrix)
    np.savetxt("normal_data/pickcounts-"+midstr+".txt",np.array(pick_counts)) # save dropoff counts
    np.savetxt("normal_data/dropcounts-"+midstr+".txt",np.array(drop_counts)) # save pickup counts

def find_G_vp(df_cab,year,month,day):
    poi = df_cab[df_cab['day'] == day]
    poi = poi.reset_index()
    wkd = poi.loc[0,['weekday']]
    wkd = int(wkd)
    print "weekday",wkd
    poi_pick = poi[['pickup_longitude','pickup_latitude']]
    poi_drop = poi[['dropoff_longitude','dropoff_latitude']]
    poi_pick = poi_pick[(poi_pick['pickup_longitude'] > -74.4) & (poi_pick['pickup_longitude'] < -73.6) & (poi_pick['pickup_latitude'] > 40.4) & (poi_pick['pickup_latitude'] < 41.0)]
    poi_drop = poi_drop[(poi_drop['dropoff_longitude'] > -74.4) & (poi_drop['dropoff_longitude'] < -73.6) & (poi_drop['dropoff_latitude'] > 40.4) & (poi_drop['dropoff_latitude'] < 41.0)]


    # --- load normal data --- #
    if (month >=1) and (month <= 3):
        start_month = 1
        end_month = 3
    elif (month >= 4) and (month <= 6):
        start_month = 4
        end_month = 6
    elif (month >= 7) and (month <= 9):
        start_month = 7
        end_month = 9
    else:
        start_month = 10
        end_month = 12
    midstr = format(year,'04d')+"-"+format(start_month,'02d')+"-"+format(end_month,'02d')+"-"+format(wkd,'01d')
    centroids = np.loadtxt("normal_data/centroids-"+midstr+".txt")
    nclusters = len(centroids)
    normal_pickcounts = np.loadtxt("normal_data/pickcounts-"+midstr+".txt")
    normal_dropcounts = np.loadtxt("normal_data/dropcounts-"+midstr+".txt")
    
    pick_labels, dist = vq(poi_pick,centroids) # assign samples to centroids
    new_pickcounts = pd.value_counts(pd.DataFrame(pick_labels)[0].values, sort = False)
    new_pickcounts = new_pickcounts.sort_index()

    drop_labels, dist = vq(poi_drop,centroids)
    new_dropcounts = pd.value_counts(pd.DataFrame(drop_labels)[0].values, sort = False)
    new_dropcounts = new_dropcounts.sort_index()

    new_idx = range(0,nclusters)
    new_pickcounts = new_pickcounts.reindex(new_idx,fill_value = 0) # fill values
    new_dropcounts = new_dropcounts.reindex(new_idx,fill_value = 0)
    # vp combines two cases: pickup and dropoff
    # vp = 0.5*(abs(np.array(new_pickcounts)-normal_pickcounts)/normal_pickcounts+abs(np.array(new_dropcounts)-normal_dropcounts)/normal_dropcounts)
    # vp = abs(np.array(new_pickcounts)-normal_pickcounts)/normal_pickcounts
    vp = abs(np.array(new_dropcounts)-normal_dropcounts)/normal_dropcounts
    adj_matrix = np.loadtxt("normal_data/adj_matrix-"+midstr+".txt")
    
    return(adj_matrix,vp)


# def create_manhattan_polygon(file):
#     grid = pd.read_csv(file)
#     grid = grid.as_matrix()
#     polygon_list = []
#     for i in range(0,len(grid)):
#         x = grid[i:i+1]
#         coord_list = []
#         coord_list.append((x[0,0], x[0,2]))
#         coord_list.append((x[0,0], x[0,3]))
#         coord_list.append((x[0,1], x[0,3]))
#         coord_list.append((x[0,1], x[0,2]))
#
#         tp = Polygon(coord_list)
#         polygon_list.append(tp)
#
#     crs = '+init=epsg:3395'
#     grid_series = GeoSeries(polygon_list)
#     grid_df = GeoDataFrame(geometry = grid_series, crs = crs)
#     return grid_df

# def filter_points(grid_spdf, df_cab, which):
#     if which == 'pick':
#         geometry = [Point(xy) for xy in zip(df_cab['pickup_longitude'], df_cab['pickup_latitude'])]
#     elif which == 'drop':
#         geometry = [Point(xy) for xy in zip(df_cab['dropoff_longitude'], df_cab['dropoff_latitude'])]
#
#     crs = '+init=epsg:3395'
#     point_spdf = GeoDataFrame(df_cab, crs = crs, geometry = geometry)
#     point_spdf['geometry'] = point_spdf.buffer(0.0001)
#     inside_point_spdf = overlay(point_spdf, grid_spdf, how = 'intersection')
#     return inside_point_spdf