## ==================== k-means clustering ========================= ###
# cluster points
def cluster_points(sample_set, centroids):
    clusters  = {}
    for x in sample_set:
    	## lambda is an anonymous function: lambda arguments: expression
    	## t[1] tells min() to compare values at position 1 (2nd)
        best_centroid_key = min([(i[0], np.linalg.norm(x - centroids[i[0]])) for i in enumerate(centroids)], key = lambda t:t[1])[0]
        try:
            clusters[best_centroid_key].append(x)
        except KeyError:
            clusters[best_centroid_key] = [x]
    return clusters

# recompute centroids
def re_evaluate_centers(clusters):
    new_centroids = []
    keys = sorted(clusters.keys())
    for k in keys:
        new_centroids.append(np.mean(clusters[k], axis = 0))
    return new_centroids

# test whether it is converged
def has_converged(centroids, old_centroids):
	return(set([tuple(a) for a in centroids]) == set([tuple(a) for a in old_centroids]))

# sample_set has 'longitude', 'latitude' information
def find_centers(sample_set, nclusters):
    old_centroids = random.sample(sample_set, nclusters) # Initialize to K random centers
    centroids = random.sample(sample_set, nclusters)
    while not has_converged(centroids, old_centroids):
        old_centroids = centroids
        clusters = cluster_points(sample_set, centroids) # operation one: assign all points to clusters
        centroids = re_evaluate_centers(clusters) # operation two: reevaluate centers
    return {'centroid':centroids, 'cluster':clusters} # returned result is tuple type

def sampling(whole_set):
    sample_set = whole_set.sample(frac = 0.01, replace = True)
    return sample_set
