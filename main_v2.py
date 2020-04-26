import pickle
import json
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords

import re
import string
import scholarly

from google.cloud import language
from google.cloud.language import enums, types

# Generally, you can use magnitude values to disambiguate these cases, as truly neutral documents will have a low magnitude value, while mixed documents will have higher magnitude values.

# salience indicates the importance or relevance of this entity to the entire document text. This score can assist information retrieval and summarization by prioritizing salient entities. Scores closer to 0.0 are less important, while scores closer to 1.0 are highly important.


def analyze_text_sentiment(text):
    client = language.LanguageServiceClient()
    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)

    response = client.analyze_entity_sentiment(document=document)

    return response  # .entities
    # results = [
    #     ('text', text),
    #     ('score', sentiment.score),
    #     ('magnitude', sentiment.magnitude),
    # ]
    # for k, v in results:
    #     print('{:10}: {}'.format(k, v))


# text = 'President Trump agreed on Monday to certify again that Iran is complying with an international nuclear agreement that he has strongly criticized, but only after hours of arguing with his top national security advisers, briefly upending a planned announcement.'
# print(analyze_text_sentiment(text))

# SUBJECT_STRING = 'Iran nuclear deal'

# def remove_noise(tweet_tokens, stop_words=()):
#     cleaned_tokens = []
#     for token, tag in pos_tag(tweet_tokens):
#         token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'
#                        '(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', token)
#         token = re.sub("(@[A-Za-z0-9_]+)", "", token)
#         # token = re.sub('[\.]', '', token)
#         if tag.startswith("NN"):
#             pos = 'n'
#         elif tag.startswith('VB'):
#             pos = 'v'
#         else:
#             pos = 'a'
#         lemmatizer = WordNetLemmatizer()
#         token = lemmatizer.lemmatize(token, pos)
#         # Remove ... and digits
#         if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words and not token.isdigit():
#             cleaned_tokens.append(token.lower())
#     return cleaned_tokens


if __name__ == "__main__":
    res = []
    # Parse Json
    with open('iran-nuclear-deal.json') as data_file:
        data = json.load(data_file)
        for entry in data:
            # print(entry)
            try:
                entry = json.loads(entry)
                # Extract the abstract
                abstract = entry['bib']['abstract']
                response = analyze_text_sentiment(abstract)
                curr_map = {}
                for entity in response.entities:
                    # print(entity)
                    score = entity.sentiment.score * 100
                    score = round(score, 4)
                    curr_map[entity.name] = score
                    # curr_map[entity.name] = entity.sentiment.score
                entry['bib']['sentiment_map'] = curr_map
                # print(entry)
                res.append(entry)
                # print(entry)
            except Exception:
                pass
        with open('result_with_status_v2.json', 'w') as outfile:
            json.dump(res, outfile)
            # json.dump(json.dumps(res.__dict__), outfile)
