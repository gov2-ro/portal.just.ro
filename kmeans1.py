import sqlite3
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

nltk.download('stopwords')
nltk.download('punkt')

# Connect to the SQLite database
conn = sqlite3.connect('data/portal-just-sample.db')

# Query the database to select the soluţieSumar column from the DosarSedinta table
cursor = conn.cursor()
cursor.execute("SELECT soluţie || \" \" || soluţie ||  \": \" || soluţieSumar FROM DosarSedinta")
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

# Use K-Means clustering algorithm to group the preprocessed text data into clusters based on their similarity
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(preprocessed_rows)

kmeans = KMeans(n_clusters=15, random_state=42)
kmeans.fit(X)

labels = kmeans.labels_

# Write the clusters and the corresponding text data to a file
with open("cluster_output.txt", "w", encoding="utf-8") as f:
    for i in range(len(set(labels))):
        f.write(f"## Cluster {i}:\n")
        for j in range(len(preprocessed_rows)):
            if labels[j] == i:
                f.write(rows[j][0] + "\n")
        f.write("\n\r>>> -----------xxxx--------------\n\r")

# Close the connection to the SQLite database
conn.close()
