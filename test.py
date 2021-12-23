import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
X, y = make_blobs(n_samples=1000,n_features=2,centers=6,cluster_std=0.3,center_box=(-10.0, 10.0)) 
plt.scatter(*zip(*X))