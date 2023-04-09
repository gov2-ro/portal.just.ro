import os
import sqlite3
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import DBSCAN

# Define input and output file paths
db_file = 'data/portal-just-mini.db'
output_dir = 'data/processed/dbscan'

# Create output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Connect to database and execute query
conn = sqlite3.connect(db_file)
c = conn.cursor()
c.execute("SELECT soluţieSumar FROM DosarSedinta")
rows = c.fetchall()
# breakpoint()
print(str(len(rows)) + " rows in " + db_file)
# Create list of documents from query results
documents = [row[0] for row in rows]

# Define vectorizer and transform documents into feature vectors
vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(documents)

# Cluster documents using DBSCAN
dbscan = DBSCAN(eps=0.7, min_samples=5)
dbscan.fit(X)

# Get list of unique cluster labels
unique_labels = set(dbscan.labels_)

# Iterate over clusters and write to file
for i, label in enumerate(unique_labels):
    # Get indices of documents in current cluster
    cluster_indices = [j for j in range(len(documents)) if dbscan.labels_[j] == label]

    # Define output file path for current cluster
    cluster_file = os.path.join(output_dir, f"cluster_{i}.txt")

    # Write cluster label and number of documents to output file
    with open(cluster_file, 'w') as f:
        f.write(f"Cluster {i} (n={len(cluster_indices)})\n")
        print("c "+ str(i))
        # Write each document to output file
        for idx in cluster_indices:
            f.write(documents[idx] + '\n')
        print("-c "+ str(i))
        # Add spacer line between clusters
        f.write('--------\n')
