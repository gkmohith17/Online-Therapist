import pickle
import nltk
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger_eng')
import re
import sys  # To receive input from command line
from collections import Counter
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer

# Load the trained model and count vectorizer
with open('./Models/emotiondetector.pkl', 'rb') as file:
    model_text = pickle.load(file)

with open('./Supporting Files/count_vect.pkl', 'rb') as file:
    count_vect = pickle.load(file)

def word_prob(word): return dictionary[word] / total
def words(text): return re.findall('[a-z]+', text.lower())
dictionary = Counter(words(open('./Supporting Files/merged.txt').read()))
max_word_length = max(map(len, dictionary))
total = float(sum(dictionary.values()))

def viterbi_segment(text):
    probs, lasts = [1.0], [0]
    for i in range(1, len(text) + 1):
        prob_k, k = max((probs[j] * word_prob(text[j:i]), j)
                        for j in range(max(0, i - max_word_length), i))
        probs.append(prob_k)
        lasts.append(k)
    words = []
    i = len(text)
    while 0 < i:
        words.append(text[lasts[i]:i])
        i = lasts[i]
    words.reverse()
    return words, probs[-1]

def fix_hashtag(text):
    text = text.group().split(":")[0]
    text = text[1:]  # remove '#'
    try:
        test = int(text[0])
        text = text[1:]
    except:
        pass
    output = ' '.join(viterbi_segment(text)[0])
    return output

def prep(tweet):
    tweet = str(tweet)
    tweet = tweet.lower()
    tweet = re.sub("(#[A-Za-z0-9]+)", fix_hashtag, tweet)
    tweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
    tweet = re.sub('\d+', '', str(tweet))
    
    def get_wordnet_pos(word):
        tag = nltk.pos_tag([word])[0][1][0].upper()
        tag_dict = {"J": wordnet.ADJ, "N": wordnet.NOUN, "V": wordnet.VERB, "R": wordnet.ADV}
        return tag_dict.get(tag, wordnet.NOUN)

    ps = PorterStemmer()
    words = tweet.split()
    lemmatizer = WordNetLemmatizer()
    lemma_words = [lemmatizer.lemmatize(word, get_wordnet_pos(word)) for word in words]
    tweet = " ".join(lemma_words)

    stopwords_list = stopwords.words('english')
    whitelist = ["n't", "not", "no"]
    words = tweet.split()
    clean_words = [word for word in words if (word not in stopwords_list or word in whitelist) and len(word) > 1]
    tweet = " ".join(clean_words)

    tweet = tweet.strip()
    return tweet

# Process input from GUI.py
if __name__ == "__main__":
    input_text = sys.argv[1]  # Text passed from the GUI.py

    # Preprocess the input text
    input_text = prep(input_text)

    # Vectorize the text and predict
    tweet_count = count_vect.transform([input_text])
    tweet_pred = model_text.predict(tweet_count)

    # Map predictions to emotions
    if tweet_pred[0] == 0:
        emotion = "Neutral"
    elif tweet_pred[0] == 1:
        emotion = "Happy"
    elif tweet_pred[0] == 2:
        emotion = "Sad"
    elif tweet_pred[0] == 3:
        emotion = "Love"
    else:
        emotion = "Anger"

    print(emotion)  # Output the emotion back to the GUI.py
