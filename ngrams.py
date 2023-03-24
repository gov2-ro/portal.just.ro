db_file = 'data/portal-just.db'
sqlq = "SELECT soluţieSumar FROM DosarSedinta"
output_csv = 'data/ngrams.csv'
ignore_list = 'data/ignore_list.csv'
min_words = 5
max_words = 15
no_results = 50

import csv, time, sqlite3
from collections import Counter

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

start_time = time.time()
print('-> Looking for most frequent [' + str(no_results) + '] ngrams between [' + str(min_words) + '] and [' + str(max_words) + '] words, ignoring the sets found in [' + ignore_list + ']')
print('-> db: [' + db_file + ']')
print('-> SQL: [' + sqlq + ']')

ignore = set()
with open(ignore_list, newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        ignore.add(row[0])

conn = sqlite3.connect(db_file)
cur = conn.cursor()
cur.execute(sqlq)
rows = cur.fetchall()

most_common_ngrams = get_most_common_ngrams(rows, k=no_results, ignore=ignore)
end_time = time.time()

with open(output_csv, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['ngram', 'count'])
    for ngram, count in most_common_ngrams:
        writer.writerow([ngram, count])

print(">> DONE \n\r" + 'saved to ' + output_csv)
print(f"Execution time: {end_time - start_time:.2f} seconds")