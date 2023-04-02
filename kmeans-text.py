import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from string import punctuation
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

input_file = 'data/processed/ngrams/ngrams.csv'
num_clusters = 5
# TODO run on a series of clusters and add columns for each cluster

output_file = 'data/processed/ngrams/ngrams-clusters-' + str(num_clusters) + '.csv'
# Load Romanian stopwords
stop_words = set(stopwords.words('romanian') + list(punctuation))

# Load sentences from file
with open(input_file, 'r', encoding='utf-8') as f:
    sentences = f.readlines()

# Preprocess sentences
preprocessed_sentences = []
for sentence in sentences:
    tokens = word_tokenize(sentence.lower())
    words = [word for word in tokens if word not in stop_words]
    preprocessed_sentences.append(' '.join(words))

# Convert preprocessed sentences to vectors using TF-IDF
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(preprocessed_sentences)

# Apply k-means clustering

km = KMeans(n_clusters=num_clusters)
km.fit(tfidf_matrix)

# Print out clusters and sentences
clusters = {}
for i, label in enumerate(km.labels_):
    if label not in clusters:
        clusters[label] = []
    clusters[label].append(sentences[i])

# Save clusters to file
with open(output_file, 'w', encoding='utf-8') as f:
    for label, sentences in clusters.items():
        # f.write(f"Cluster {label+1}:\n")
        sentence_label = f"{label+1}, "
        for sentence in sentences:
            f.write(f"\t{sentence_label}{sentence}")
        # f.write('\n')

# # Print out clusters and sentences
# for label, sentences in clusters.items():
#     print(f"Cluster {label+1}:")
#     for sentence in sentences:
#         print(f"\t{sentence}")
