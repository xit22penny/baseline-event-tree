__author__ = 'Xian Teng'

import numpy as np
import sys
import random
import math
import PCST
import time

def get_adjacency_matrix(centroid):
    nCentroids = len(centroid)
    adj_matrix = np.zeros((nCentroids,nCentroids)) # a nCentroids by nCentroids adjacency matrix
    for i in range(0,nCentroids):
        for j in range(i+1,nCentroids):
            adj_matrix[i,j] = np.linalg.norm(centroid[i] - centroid[j]) # calculate distance
            adj_matrix[j,i] = adj_matrix[i,j]

    return adj_matrix


arg1 = sys.argv[1] # number of points
n = int(arg1)
e = np.random.random((n,2)) # randomly create n points

adj_matrix = get_adjacency_matrix(e) # get adjacency matrix
vp = [0]*n

# # ------ insert one spherical event ------ #
# r = 0.3 # radius
# centroid = [0.5,0.5] # event centroid
# for i in range(0,n):
# 	if np.linalg.norm(e[i] - centroid) <= r:
# 		vp[i] = 1
# # insert noises
# p = 0.02
# idx = random.sample(range(0,n), int(math.floor(p*n))) # sample p% indices
# vp = [random.random() if i in idx else vp[i] for i in range(0,len(vp))]
# print " --- starting PCST --- "
# start_time = time.time()
# gamma = 1.0
# T = PCST.FindTree(adj_matrix,vp,gamma)
# end_time = time.time()
# print("--- %s seconds ---" % (end_time - start_time))
# print T['V']['vid']
# print [idx for idx in range(0,len(vp)) if vp[idx] > 0]


# ------ insert two spherical events ------ #
# r = 0.2
# centroid1 = [0.2,0.2]
# centroid2 = [0.8,0.8]
# for i in range(0,n):
# 	if (np.linalg.norm(e[i] - centroid1) <= r) or (np.linalg.norm(e[i] - centroid2) <= r):
# 		vp[i] = 1
# # insert noises
# p = 0.02
# idx = random.sample(range(0,n), int(math.floor(p*n))) # sample p% indices
# vp = [random.random() if i in idx else vp[i] for i in range(0,len(vp))]
# print " --- starting PCST --- "
# start_time = time.time()
# gamma = 1.0
# T = PCST.FindTree(adj_matrix,vp,gamma)
# new_vp = [1 if i in T['V']['vid'] else 0 for i in range(0,n)]
# end_time = time.time()
# print("--- %s seconds ---" % (end_time - start_time))

# ------ insert cross events ------ #
# y = x - 0.2
# y = x + 0.2
# y = -x + 0.8
# y = -x + 1.2
for i in range(0,n):
	if ((e[i][1] >= e[i][0]-0.2) and (e[i][1] <= e[i][0]+0.2)) or ((e[i][1] >= -1*e[i][0]+0.8) and (e[i][1] >= -1*e[i][0]+1.2)):
		vp[i] = 1
# insert noises
p = 0.02
idx = random.sample(range(0,n), int(math.floor(p*n))) # sample p% indices
vp = [random.random() if i in idx else vp[i] for i in range(0,len(vp))]
print " --- starting PCST --- "
start_time = time.time()
gamma = 1.0
T = PCST.FindTree(adj_matrix,vp,gamma)
new_vp = [1 if i in T['V']['vid'] else 0 for i in range(0,n)]
end_time = time.time()
print("--- %s seconds ---" % (end_time - start_time))
np.savetxt("cross-scatter-points.txt",e)
np.savetxt("cross-ground-truth-vp.txt",vp)
np.savetxt("cross-detected-vp.txt",new_vp)