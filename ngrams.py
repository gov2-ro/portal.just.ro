import csv, time, sqlite3, os, argparse
from collections import Counter
from tqdm import tqdm


db_file = 'data/portal-just.db'
sqlq = "SELECT soluţieSumar FROM DosarSedinta"
output_csv = 'data/ngrams.csv'
ignore_list = 'data/ignore_list.csv'
min_words = 10
max_words = 25
no_results = 500
batch_size = 100

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
            # Only add the n-gram if it is the shortest n-gram for this sequence of words
            is_shortest = all(ngram not in shorter for shorter in ngrams)
            if is_shortest:
                ngrams.append(ngram)
    return ngrams

def get_most_common_ngrams(rows, k, ignore=None):
    text = " ".join(row[0] for row in rows)
    ngrams = get_ngrams(text, min_words, max_words, ignore=ignore)
    ngram_counts = Counter(ngrams)
    # Filter out any n-grams that have the same count as a longer n-gram
    for ngram, count in list(ngram_counts.items()):
        if any(ngram in longer for longer in ngram_counts if len(longer) > len(ngram) and ngram_counts[longer] == count):
            del ngram_counts[ngram]
    return ngram_counts.most_common(k)

start_time = time.time()

print('-> Most common [' + str(no_results) + '] ngrams between [' + str(min_words) + '] and [' + str(max_words) + '] words, ignoring [' + ignore_list + ']')
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
num_rows = len(rows)
num_batches = (num_rows + batch_size - 1) // batch_size

# most_common_ngrams = get_most_common_ngrams(rows, k=no_results, ignore=ignore)
most_common_ngrams = Counter()

for i in tqdm(range(num_batches)):
    # Get a batch of rows to process
    start = i * batch_size
    end = min((i+1) * batch_size, num_rows)
    batch_rows = rows[start:end]
    # Get the most common n-grams for this batch
    batch_ngrams = get_most_common_ngrams(batch_rows, k=no_results, ignore=ignore)
    most_common_ngrams += Counter(dict(batch_ngrams))
end_time = time.time()


with open(output_csv, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['ngram', 'count'])
    for ngram, count in most_common_ngrams:
        writer.writerow([ngram, count])

end_time = time.time()

print(">> DONE \n\r" + 'saved to ' + output_csv)
print(f"Execution time: {end_time - start_time:.2f} seconds")
os.system('say -v ioana "în sfârșit, am gătat" -r 250')