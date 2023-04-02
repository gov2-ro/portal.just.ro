import sqlite3
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

# ------------
clusters = 25
random_state=42
# ------------

print(str(clusters) + " clusters; random state = " + str(random_state))

nltk.download('stopwords')
nltk.download('punkt')

# Connect to the SQLite database
conn = sqlite3.connect('data/portal-just-sample.db')

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

# Use K-Means clustering algorithm to group the preprocessed text data into clusters based on their similarity
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(preprocessed_rows)

kmeans = KMeans(n_clusters=clusters, random_state = random_state)
kmeans.fit(X)

labels = kmeans.labels_

# Write the clusters and the corresponding text data to separate files
for i in range(len(set(labels))):
    cluster_file = f"data/processed/cluster_{i}.txt"
    print ("-cluster: " + str(i))
    count_total = 0
    with open(cluster_file, "w", encoding="utf-8") as f:
        for j in range(len(preprocessed_rows)):
            if labels[j] == i:
                count_total += 1
                count = sum([1 for l in labels if l == i])
                f.write(rows[j][0] + f"\n-----> zzz \n")
        f.write(f"\n\r----- >>  Number of occurrenceszzz: {count_total}\n")
        print ("-- cstr: " + i)
conn.close()
