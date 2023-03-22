#dependencies
import pandas as pd
import sqlite3
from sqlite3 import Error
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.stem.snowball import SnowballStemmer
nltk.download('wordnet')
from nltk.stem.wordnet import WordNetLemmatizer
nltk.download('stopwords')
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
import seaborn as sns
#force output to display the full description
pd.set_option('display.max_colwidth', -1)
dbfile = 'data/portal-just.db'

#create connection to database
conn = sqlite3.connect(dbfile)
c = conn.cursor()
#create the pandas data frame
wine_df = pd.read_sql('Select soluţieSumar from DosarSedinta', conn)
#display the top 3 records from the data frame
wine_df.head(3)
#inline function to produce word count, splitting on spaces
wine_df['word_count'] = wine_df['soluţieSumar'].apply(lambda x: len(str(x).split(" ")))
wine_df.word_count.describe()
#set x for the histogram and set bins based on max
x = wine_df['word_count']
n_bins = 140
#plot histogram
plt.hist(x, bins=n_bins)
plt.show()
stop_words = set(stopwords.words("romanian"))
#show how many words are in the list of stop words
print(len(stop_words))
#179
#loops through descriptions and cleans them
clean_desc = []
for w in range(len(wine_df.soluţieSumar)):
    desc = wine_df['soluţieSumar'][w].lower()
    
    #remove punctuation
    desc = re.sub('[^a-zA-Z]', ' ', desc)
    
    #remove tags
    desc=re.sub("&lt;/?.*?&gt;"," &lt;&gt; ",desc)
    
    #remove digits and special chars
    desc=re.sub("(\\d|\\W)+"," ",desc)
    
    clean_desc.append(desc)
#assign the cleaned descriptions to the data frame
wine_df['clean_desc'] = clean_desc
#calculate the frequency
word_frequency = pd.Series(' '.join(wine_df['clean_desc']).split()).value_counts()[:30]
word_frequency
#add single word to stoplist
#stop_words.add("wine")
#add list of words to stoplist
add_stopwords = ["wine", "drink"]
stop_words = stop_words.union(add_stopwords)
print(len(stop_words))
#181
stem_desc = []
for w in range(len(wine_df['clean_desc'])):
    split_text = wine_df['clean_desc'][w].split()
    
    ##Stemming
#     stm = SnowballStemmer("english")
#     split_text = [stm.stem(word) for word in split_text if not word in stop_words] 
#     split_text = " ".join(split_text)
#     stem_desc.append(split_text)
    
    #Lemmatisation
    lem = WordNetLemmatizer()
    split_text = [lem.lemmatize(word) for word in split_text if not word in stop_words] 
    split_text = " ".join(split_text)
    stem_desc.append(split_text)
stem_desc
#set the word cloud parameters
wordcloud = WordCloud(width = 800, height = 800, background_color = 'black', stopwords = stop_words, max_words = 1000, min_font_size = 20).generate(str(stem_desc))
#plot the word cloud
fig = plt.figure(figsize = (8,8), facecolor = None)
plt.imshow(wordcloud)
plt.axis('off')
plt.show()
#fig.savefig("wordcloud.png")
def get_trigrams(descriptions, n=None):
    
    vec = CountVectorizer(ngram_range = (3,3), max_features = 20000).fit(descriptions)
    bag_of_words = vec.transform(descriptions)
    sum_words = bag_of_words.sum(axis = 0) 
    words_freq = [(word, sum_words[0, i]) for word, i in vec.vocabulary_.items()]
    words_freq =sorted(words_freq, key = lambda x: x[1], reverse = True)
   
    return words_freq[:n]
stops = ['se','va', 'dosar', 'partea', 'cabernet', 'sauvignon', 'black', 'cherry']
stem_desc = []
for w in range(len(wine_df['clean_desc'])):
    split_text = wine_df['clean_desc'][w].split()
       
    #Lemmatisation
    lem = WordNetLemmatizer()
    split_text = [lem.lemmatize(word) for word in split_text if not word in stops] 
    split_text = " ".join(split_text)
    stem_desc.append(split_text)
trigrams = get_trigrams(clean_desc, n=15)
#create a trigram data frame
trigram_df = pd.DataFrame(trigrams)
trigram_df.columns=["Trigram", "Freq"]
#output top 15 rows
trigram_df.head(15)
fig = sns.set(rc = {'figure.figsize':(12,8)})
bp = sns.barplot(x = "Trigram", y = "Freq", data = trigram_df)
bp.set_xticklabels(bp.get_xticklabels(), rotation = 75)
plt.show()