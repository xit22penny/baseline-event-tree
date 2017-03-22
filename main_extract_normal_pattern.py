__author__ = 'Xian Teng'

import time
import pandas as pd
import numpy as np
import load_csv
import region_kmeans
import PCST
from datetime import datetime
from scipy.cluster.vq import vq, kmeans2, whiten
import sys

arg1 = sys.argv[1] # year
arg2 = sys.argv[2] # start_month
arg3 = sys.argv[3] # end_month
arg4 = sys.argv[4] # nclusters

year = int(arg1)
start_month = int(arg2)
end_month = int(arg3)
nclusters = int(arg4)

start_time = time.time()
print "--- loading data ----"
df_cab = load_csv.extract_dataframe(year, start_month, end_month)
end_time = time.time()
print("--- %s seconds ---" % (end_time - start_time))

for wkd in range(0,7):
	region_kmeans.find_normal_pattern(df_cab,year,start_month,end_month,wkd,nclusters)




# --- get raletive activity level for a specific day --- #
# for i in range(0,nclusters):
# 	clusters[i] = {'centroid':result[0][i], 'activity_level':len(result[1][i])}

# G = np.array([(-1, 1, 10, -1, -1, -1, -1, -1, -1, -1),
#   (1, -1, -1, -1, -1, 10, -1, -1, -1, -1),
#   (10, -1, -1, 10, 1, -1, -1, -1, -1, -1),
#   (-1, -1, 1, -1, -1, -1, -1, -1, 10, -1),
#   (-1, -1, 1, -1, -1, 1, 10, 10, 1, -1),
#   (-1, 10, -1, -1, 1, -1, 10, -1, -1, -1),
#   (-1, -1, -1, -1, 10, 10, -1, -1, -1, -1),
#   (-1, -1, -1, -1, 10, -1, -1, -1, -1, 100),
#   (-1, -1, -1, 10, 1, -1, -1, -1, -1, 100),
#   (-1, -1, -1, -1, -1, -1, -1, 100, 100, -1)])
# vp = [10, 1, 1, 150, 200, 1, 100, 1, 1, 20]
# T = PCST.FindTree(G,vp)
# print T
# T = PCST.PCSTr(G,vp,0)

