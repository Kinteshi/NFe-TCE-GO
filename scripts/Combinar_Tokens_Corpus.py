# Imports
import re

import nltk
import numpy as np
import pandas as pd
from joblib import dump
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from unidecode import unidecode

nltk.download('stopwords')
nltk.download('punkt')


def descricao_preprocessing(input_text):
    out_text = str(input_text).lower()
    out_text = unidecode(out_text)
    out_text = ' '.join([w for w in word_tokenize(
        out_text) if w not in stopwords.words('portuguese')])
    out_text = re.sub(r'[0-9]{5,}', '', out_text)
    return out_text


# function to combine similar tokens from corpus
def combine_tokens(corpus):
    tokenized_corpus = [word_tokenize(sentence) for sentence in corpus]
    # flatten the list
    flattened_corpus = [
        item for sublist in tokenized_corpus for item in sublist]
    token_set = set(flattened_corpus)
    token_set = [
        token for token in token_set if token not in stopwords.words('portuguese')]
    # check for tokens that are substring of other bigger tokens
    token_set = [
        token for token in token_set if not any(token in substring for substring in token_set if len(substring) > len(token))]
    # for each sentence in the corpus, replace the tokens with the new supertokens
    for i, sentence in enumerate(tokenized_corpus):
        for j, token in enumerate(sentence):
            for supertoken in token_set:
                if token in supertoken:
                    tokenized_corpus[i][j] = supertoken
    # Join the tokens back to sentences
    tokenized_corpus = [
        ' '.join(sentence) for sentence in tokenized_corpus]
    return tokenized_corpus


# function to calculate cosine similarity between all sentences in the corpus and sum them up
def calculate_similarity(corpus):
    vectorizer = CountVectorizer(analyzer='word', ngram_range=(1, 1))
    vectorized = vectorizer.fit_transform(corpus)
    similarity_matrix = vectorized * vectorized.T
    similarity_matrix = similarity_matrix.toarray()
    similarity_matrix = np.sum(similarity_matrix, axis=1)
    return similarity_matrix


# function that calculates the confidence interval of 95% for the similarity and removes the sentences with a similarity outside the confidence interval
def calculate_confidence_interval(similarity_matrix):
    confidence_interval = np.percentile(similarity_matrix, 95)
    confidence_interval = np.mean(similarity_matrix) + confidence_interval
    return confidence_interval
