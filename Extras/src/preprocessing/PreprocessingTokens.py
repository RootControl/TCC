import csv
import nltk
import pandas
import re
from nltk.corpus import stopwords
from nltk import stem
import string


emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""

regex_str = [
    emoticons_str,
    r'<[^>]+>',  # HTML tags
    r'(?:@[\w_]+)',  # @-mentions
    r'(?:\#+[\w_]+[\w\'_\-]*[\w_]+)',  # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+',  # URLs

    r'(?:(?:\d+,?)+(?:\.?\d+)?)',  # numbers
    r'(?:[a-z][a-z\-_]+[a-z])',  # words with - and '
    r'(?:[\w_]+)',  # other words
    r'(?:\S)'  # anything else
]

tokens_re = re.compile(r'(' + '|'.join(regex_str) + ')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^' + emoticons_str + '$', re.VERBOSE | re.IGNORECASE)



punctuation = list(string.punctuation)
stop = stopwords.words('english')  # + punctuation  # + regex_str



def tokenize(s):
    return tokens_re.findall(s)


def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens if token not in stop]
    return tokens


def removeStopwords(text):
    result = re.sub(r"http\S+", " ", text)
    result = re.sub(r"#\S+", " ", result)
    result = re.sub(r"@\S+", " ", result)
    tmp = result.split(' ')
    phrase = []
    for word in tmp:
        if word not in stop:
            phrase.append(word)
    return phrase


def removeStemmer(list):
    ENstopwords = stopwords.words('english') + punctuation + regex_str
    stemmer = stem.PorterStemmer()

    phrase = []
    for row in list:
        low_text = row.lower()
        tmp = re.sub(r'[^\w]', ' ', low_text)
        result = [str(stemmer.stem(element)) for element in tmp.split() if element not in ENstopwords]
        phrase.append((result, ''))

    return phrase


def generate_csv_file_removing_stemmer(game):
    pd = pandas.read_csv(f'files/finalFiles/{game}.csv', error_bad_lines=False)
    result = removeStemmer(pd['text'])

    with open(f'files/texts/{game}_ll.csv', 'w+', encoding='utf-8') as csvfile:
        fieldnames = ['text', 'emotion']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for item in result:
            text, emotion = item

            writer.writerow({'text': f'{text}', 'emotion': f'{emotion}'})
        print('ok')


def database(file):
    allData = []
    with open(file, encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                allData.append((row[0], row[1]))
                line_count += 1
    return allData


def all_words_in_file(file):
    pd = pandas.read_csv(file, error_bad_lines=False, low_memory=False)
    allWords = []
    phraseList = pd['text']
    for text in phraseList:
        tmp = re.sub(r'[^\w]', ' ', text)
        tmp = tmp.split()
        allWords.extend(tmp)

    frequentWords = nltk.FreqDist(allWords)  # show all words and his frequency
    freq = frequentWords.keys()
    return freq


def extract_words(list):
    features = {}
    unique_words = all_words_in_file('../files/oneFile/treinamento.csv')
    for words in unique_words:
        features[f'{words}'] = (words in list)
    return features


def verifyPhrase(list, classified):
    template = []
    for (phrase, emotion) in list:
        result = extract_words(phrase)
        template.append((phrase, classified.classify(result)))

    with open(f'../files/oneFile/classify_ll.csv', 'w+', encoding='utf-8') as csvfile:
        fieldnames = ['text', 'emotion']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for item in template:
            text, emotion = item
            writer.writerow({'text': f'{text}', 'emotion': f'{emotion}'})
        print('ok')
