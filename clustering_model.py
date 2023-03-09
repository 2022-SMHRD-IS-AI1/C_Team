import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

# Define the file paths
data_dir = '/path/to/data/directory'

# Load the data
files = []
for file in os.listdir(data_dir):
    with open(os.path.join(data_dir, file), 'r') as f:
        files.append(f.read())

# Extract features from the data using TF-IDF
vectorizer = TfidfVectorizer()
features = vectorizer.fit_transform(files)

# Cluster the data using K-Means
num_clusters = 3
km = KMeans(n_clusters=num_clusters)
km.fit(features)

# Print the top terms for each cluster
order_centroids = km.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names()
for i in range(num_clusters):
    print('Cluster {}:'.format(i))
    for j in order_centroids[i, :10]:
        print('  {}'.format(terms[j]))
    print()