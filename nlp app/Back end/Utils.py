import pandas as pd
from bs4 import BeautifulSoup
import unidecode
from nltk import word_tokenize
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
from contraction import CONTRACTION_MAP
def remove_html_tag(text):
    text = BeautifulSoup(text, 'lxml')
    return text.get_text()

def removing_new_line(text):
    text = re.sub('\s+', ' ', text)
    return text

def remove_accent_char(text):
    res = unidecode.unidecode(text)
    return res

def remove_email(text):
    text = re.sub('\S+@\S+', ' ', text)
    return text

def remove_stopwords(sent):
    stop_words = set(stopwords.words('english'))
    filtered_sentence = ' '.join([w for w in sent.split() if not w.lower() in stop_words])
    return filtered_sentence

def remove_stopwords_sentiment(text):
    new_stopwords = set(stopwords.words('english')) - {'not', 'such', 'up', 'down', 'too', 'against', 'only'}
    text = [word for word in text if word not in new_stopwords]
    return text

def remove_special_characters(text):
    pattern = r'[^a-zA-Z\s]'
    text = re.sub(pattern, ' ', text)
    return text

def remove_spacing(text):
    res = " ".join(text.split())
    return res

def expand_contractions(s, contractions_dict=CONTRACTION_MAP):
    c_re = re.compile('(%s)' % '|'.join(CONTRACTION_MAP.keys()))
    def replace(match):
        return contractions_dict[match.group(0)]
    return c_re.sub(replace, s)

def lemmatizer_acc(sent):
    lemmatizer = WordNetLemmatizer()
    lemma_sent = []
    for word, tag in pos_tag(word_tokenize(sent)):
        wntag = tag[0].lower()
        wntag = wntag if wntag in ['a', 'r', 'n', 'v'] else None
        if not wntag:
            lemma = word
        else:
            lemma = lemmatizer.lemmatize(word, wntag)
        lemma_sent.append(lemma)
    lemma_sent = " ".join(lemma_sent)
    return lemma_sent

def tokenizer_and_lemmatizer(sents):
    lemmatizer = WordNetLemmatizer()
    new_sents = []
    for ind, sent in enumerate(sents):
        print(ind)
        lemma_sent = lemmatizer_acc(sent)
        new_sents.append(lemma_sent)
    return new_sents

def tokenizer(text):
    text = word_tokenize(text)
    return text