import sqlite3
import re, os
import numpy as np

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans
from stopwordsiso import stopwords as romanian_stopwords

# specify the language when importing the stopwordsiso package
romanian_stopwords = romanian_stopwords("ro")
romanian_stopwords = list(romanian_stopwords)  # convert the set to a list

# connect to the SQLite database
conn = sqlite3.connect('data/portal-just-mini.db')
cursor = conn.cursor()

# execute a query to retrieve the text data from the 'soluţieSumar' column of the 'DosarSedinta' table
cursor.execute("SELECT soluţieSumar FROM DosarSedinta")
data = cursor.fetchall()

# check if the category column already exists
cursor.execute("PRAGMA table_info('DosarSedinta')")
columns = cursor.fetchall()
category_exists = False
for column in columns:
    if column[1] == 'category':
        category_exists = True
        break

# create the category column if it does not exist
if not category_exists:
    cursor.execute("ALTER TABLE DosarSedinta ADD COLUMN category TEXT")

# perform some basic text preprocessing
processed_data = []
for row in data:
    text = row[0]
    text = re.sub(r'[^\w\s]', '', text)  # remove punctuation
    text = text.lower()  # convert to lowercase
    text = ' '.join([word for word in text.split() if word not in romanian_stopwords])  # remove stop words
    processed_data.append(text)

# vectorize the text data using a bag-of-words approach
vectorizer = CountVectorizer(stop_words=romanian_stopwords)
vectorized_data = vectorizer.fit_transform(processed_data)

# perform clustering using the KMeans algorithm
num_clusters = 14
kmeans = KMeans(n_clusters=num_clusters)
kmeans.fit(vectorized_data)

# assign category labels to each row of data
# category_labels = kmeans.predict(vectorized_data)
documents = [row[0] for row in cursor.execute("SELECT soluţieSumar FROM DosarSedinta")]

category_labels = np.random.randint(0, num_clusters, len(documents))


for i, row in enumerate(data):
    # print(type(category_labels[i]))
    # cursor.execute("UPDATE DosarSedinta SET category = ? WHERE soluţieSumar = ?", (category_labels[i], row[0]))
    cursor.execute("UPDATE DosarSedinta SET category = ? WHERE soluţieSumar = ?", (str(category_labels[i]), row[0]))


conn.commit()
conn.close()

os.system('say "Done"')