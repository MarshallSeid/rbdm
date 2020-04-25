import pickle
import json
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords

import re
import string
import scholarly

SUBJECT_STRING = 'Iran nuclear deal'


def remove_noise(tweet_tokens, stop_words=()):
    cleaned_tokens = []
    for token, tag in pos_tag(tweet_tokens):
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', token)
        token = re.sub("(@[A-Za-z0-9_]+)", "", token)
        # token = re.sub('[\.]', '', token)
        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'
        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)
        # Remove ... and digits
        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words and not token.isdigit():
            cleaned_tokens.append(token.lower())
    return cleaned_tokens


if __name__ == "__main__":
    # Open classifier.
    f = open('my_classifier.pickle', 'rb')
    classifier = pickle.load(f)

    # Add Stop words.
    stop_words = stopwords.words('english')
    stop_words += ['…']

    # TODO change this to all be in the same file when we're no longer rate limited.
    # data_list = []
    # data_generator = scholarly.search_pubs_query('China')
    # print(next(data_generator))
    # for data in data_generator:
    #     print(data)

    res = []
    # Parse Json
    with open('iran-nuclear-deal.json') as data_file:
        data = json.load(data_file)
        for entry in data:
            try:
                entry = json.loads(entry)
                # Extract the abstract
                abstract = entry['bib']['abstract']
                custom_tokens = remove_noise(
                    word_tokenize(abstract), stop_words
                )
                predicted_status = classifier.classify(
                    dict([token, True] for token in custom_tokens))
                # print(custom_tokens)
                entry['bib']['predicted_status'] = predicted_status
                print(entry)
                res.append(entry)
                # print(abstract)
            except Exception:
                pass
        with open('result_with_status.json', 'w') as outfile:
            json.dump(res, outfile)
    f.close()
