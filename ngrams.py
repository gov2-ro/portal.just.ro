import csv, time, sqlite3, os
from collections import Counter
import argparse

db_file = 'data/portal-just-mini.db'
sqlq = "SELECT soluţieSumar FROM DosarSedinta"
output_csv = 'data/processed/ngrams/ngrams.csv'
ignore_list = 'data/ignore_list.csv'
min_words = 10
max_words = 25
no_results = 500

parser = argparse.ArgumentParser(description='does the ngram thing from db')
parser.add_argument('-min', '--min_words', help='min words')
parser.add_argument('-max', '--max_words', help='max words')
parser.add_argument('-r', '--no_results', help='number of results')
parser.add_argument('-i', '--ignore_list', help='ignore list')
parser.add_argument('-o', '--output_csv', help='output csv')
parser.add_argument('-db', '--database', help='input sqlite db file')
parser.add_argument('-q', '--sql', help='query')

args = parser.parse_args()

if args.min_words:
    min_words = int(args.min_words)
if args.max_words:
    max_words = int(args.max_words)
if args.no_results:
    no_results = int(args.no_results)
if args.ignore_list:
    ignore_list = args.ignore_list
if args.output_csv:
    output_csv = args.output_csv
if args.database:
    db_file = args.database
if args.sql:
    sqlq = args.sql

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
    print('1')
    ngrams = get_ngrams(text, min_words, max_words, ignore=ignore)
    print('2')
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
print('0')
most_common_ngrams = get_most_common_ngrams(rows, k=no_results, ignore=ignore)
print('3')
end_time = time.time()

with open(output_csv, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['ngram', 'count'])
    for ngram, count in most_common_ngrams:
        writer.writerow([ngram, count])

print(">> DONE \n\r" + 'saved to ' + output_csv)
print(f"Execution time: {end_time - start_time:.2f} seconds")

os.system('say -v ioana "în sfârșit, am gătat" -r 250')