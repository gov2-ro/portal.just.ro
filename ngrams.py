import csv, time, sqlite3
from collections import Counter

db_file = 'data/portal-just.db'
output_csv = 'data/ngrams.csv'
ignore_list = 'data/ignore_list.csv'
min_words = 5
max_words = 15
no_results = 50


def get_ngrams(text, min_words, max_words, ignore=None):
    words = text.split()
    ngrams = []
    for n in range(min_words, max_words):
        for i in range(len(words)-n+1):
            ngram = " ".join(words[i:i+n])
            if ignore and ngram in ignore:
                continue
            ngrams.append(ngram)
    return ngrams

def get_most_common_ngrams(rows, k, ignore=None):
    text = " ".join(row[0] for row in rows)
    ngrams = get_ngrams(text, min_words, max_words, ignore=ignore)
    ngram_counts = Counter(ngrams)
    return ngram_counts.most_common(k)

# Read the ignore list from a CSV file
ignore = set()
with open(ignore_list, newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        ignore.add(row[0])

# Connect to the SQLite database
conn = sqlite3.connect(db_file)

# Get a cursor object
cur = conn.cursor()

# Query the database to get the rows to analyze
cur.execute("SELECT soluţieSumar FROM DosarSedinta")
rows = cur.fetchall()

# Get the 25 most common n-grams, excluding any n-grams in the ignore list
start_time = time.time()
most_common_ngrams = get_most_common_ngrams(rows, k=no_results, ignore=ignore)
end_time = time.time()

# Export the results to a CSV file
with open(output_csv, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['ngram', 'count'])
    for ngram, count in most_common_ngrams:
        writer.writerow([ngram, count])

# Display the total execution time of the script
print(f"Execution time: {end_time - start_time:.2f} seconds")
