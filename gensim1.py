import sqlite3, os
import gensim
from gensim import corpora, models

# connect to SQLite database and retrieve corpus
conn = sqlite3.connect('data/portal-just-mini.db')
cursor = conn.cursor()
cursor.execute('SELECT soluţieSumar, xnumardosar FROM DosarSedinta')
rows = cursor.fetchall()
corpus = [row[0] for row in rows]
doc_ids = [row[1] for row in rows]

# preprocess the text data
processed_corpus = [gensim.utils.simple_preprocess(doc) for doc in corpus]

# create a dictionary and document-term matrix
dictionary = corpora.Dictionary(processed_corpus)
bow_corpus = [dictionary.doc2bow(doc) for doc in processed_corpus]
tfidf_model = models.TfidfModel(bow_corpus)
tfidf_corpus = tfidf_model[bow_corpus]

# train the model (LDA example shown)
num_topics = 14
lda_model = gensim.models.ldamodel.LdaModel(tfidf_corpus, num_topics=num_topics, id2word=dictionary, passes=10)

# assign categories to documents based on dominant topic(s)
# category_labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', ]
category_assignments = []
for doc in tfidf_corpus:
    topic_scores = lda_model[doc]
    dominant_topic = max(topic_scores, key=lambda x: x[1])[0]
    # category_assignments.append(category_labels[dominant_topic])
    category_assignments.append(dominant_topic)

# update SQLite database with category assignments
for i, category in enumerate(category_assignments):
    cursor.execute('UPDATE DosarSedinta SET category=? WHERE xnumardosar=?', (category, doc_ids[i]))

# commit changes and close database connection
conn.commit()
conn.close()
os.system('say "Done 2"')