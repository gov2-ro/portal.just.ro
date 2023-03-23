import sqlite3
import nltk
from nltk.collocations import BigramAssocMeasures, BigramCollocationFinder
dbfile = "data/portal-just.db"
# Connect to the SQLite database and get a cursor
conn = sqlite3.connect(dbfile)
cursor = conn.cursor()

# Select the text column from the table
cursor.execute('SELECT soluţieSumar FROM DosarSedinta')

# Fetch all rows as a list of tuples
rows = cursor.fetchall()
print('- 1')
# Concatenate all text into a single string
corpus = ' '.join([row[0] for row in rows])
print('- 2')
# Tokenize the corpus
tokens = nltk.word_tokenize(corpus)
print('- 3')
# Set up the bigram finder and scorer
finder = BigramCollocationFinder.from_words(tokens)
scorer = BigramAssocMeasures()
print('- 4')
# Get the 10 most frequent bigrams
top_n_bigrams = finder.nbest(scorer.raw_freq, 10)
print('- 5')
# Print the results
for bigram in top_n_bigrams:
    print(bigram)
