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
import datetime
import math


arg1 = sys.argv[1] # year
arg2 = sys.argv[2] # month
# arg3 = sys.argv[3] # days

year = int(arg1)
month = int(arg2)
# days = arg3.split(",")

# --- prepare data --- #
print "--- loading data ----"
start_time = time.time()
df_cab = load_csv.extract_dataframe(year, month, month)
print min(df_cab['day']), min(df_cab['month'])
end_time = time.time()
print("--- %s seconds ---" % (end_time - start_time))

print "--- extracting adj_matrix & vp data ----"
start_time = time.time()
# for i in range(0,len(days)):
# 	day = int(days[i])
for day in range(1,30):
	print "day",day
	adj_matrix, vp = region_kmeans.find_G_vp(df_cab,year,month,day)
	midstr = format(year,'04d')+"-"+format(month,'02d')+"-"+format(day,'02d')
	np.savetxt("vp-"+midstr+".txt",vp)
	# print min(vp),np.mean(vp),max(vp)

end_time = time.time()
print("--- %s seconds ---" % (end_time - start_time))
# ------------------------------------------------------ #

# year = int(arg1)
# month = int(arg2)
# gamma = 1.0
# file = open("detection-results.dat","ab")
# print "--- starting to detect anomalies --- "
# for day in range(1,30):
# 	start_time = time.time()
# 	wkd = datetime.datetime(year,month,day).weekday()
# 	print "day: ",day," weekday: ",wkd
# 	midstr = format(year,'04d')+"-"+format(month,'02d')+"-"+format(month+2,'02d')+"-"+format(wkd,"01d")
# 	G = np.loadtxt("normal_data/adj_matrix-"+midstr+".txt")
# 	vp = np.loadtxt("vp-"+format(year,'04d')+"-"+format(month,'02d')+"-"+format(day,'02d')+".txt")
# 	T = PCST.FindTree(G,vp,gamma)
# 	score = T['score']
# 	file.write("day: "+str(day)+", weekday: "+str(wkd)+", score: "+str(score)+"\n")
# 	file.write("detected coordinates\n")
# 	vid = T['V']['vid']
# 	vcoordinate = G[vid,:]
# 	np.savetxt(file,vcoordinate)
# 	file.write("\n")
# 	end_time = time.time()
# 	print("--- %s seconds ---" % (end_time - start_time))

# file.close()