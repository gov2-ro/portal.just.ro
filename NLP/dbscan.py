import os
import sqlite3
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import DBSCAN
from sklearn.metrics.pairwise import cosine_similarity

db_file = 'data/portal-just-mini.db'
output_dir = 'data/processed'

nltk.download('stopwords')
nltk.download('punkt')

# Connect to the SQLite database
conn = sqlite3.connect(db_file)

# Query the database to select the soluţieSumar column from the DosarSedinta table
cursor = conn.cursor()
cursor.execute("SELECT soluţie || \": \" || soluţieSumar as meme FROM DosarSedinta")
rows = cursor.fetchall()

# Clean and preprocess the text data
stop_words = set(stopwords.words('romanian'))
punctuations = string.punctuation + "’" + "„" + "“"

def preprocess_text(text):
    text = text.lower()
    tokens = word_tokenize(text)
    tokens = [token for token in tokens if token not in stop_words and token not in punctuations]
    return " ".join(tokens)

preprocessed_rows = [preprocess_text(row[0]) for row in rows]

# Use DBSCAN clustering algorithm to group the preprocessed text data into clusters based on their similarity
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(preprocessed_rows)

cosine_sim = cosine_similarity(X)

dbscan = DBSCAN(eps=0.5, min_samples=3, metric='precomputed')
dbscan.fit(cosine_sim)

labels = dbscan.labels_

# Create the 'data/processed' folder if it doesn't exist
if not os.path.exists('data/processed'):
    os.makedirs('data/processed')

# Write the clusters and the corresponding text data to separate files inside the 'data/processed' folder
for i in range(len(set(labels))):
    # cluster_file = f"data/processed/cluster_{i}.txt"
    cluster_file = os.path.join(output_dir, f"cluster_{i}.txt")
    print ("-cluster: " + str(i))
    with open(cluster_file, "w", encoding="utf-8") as f:
        for j in range(len(preprocessed_rows)):
            if labels[j] == i:
                count = sum([1 for l in labels if l == i])
                # f.write(f"Cluster {i} (Number of occurrences: {count})\n")
                f.write(rows[j][0] + "\n")
                f.write("--------\n")
    print (" --c: " + str(i))
# Close the connection to the SQLite database
conn.close()
