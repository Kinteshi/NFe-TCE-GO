# %%
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

# Constants
seed = 15
# %%
# Funções


def descricao_preprocessing(input_text):
    out_text = str(input_text).lower()
    out_text = unidecode(out_text)
    out_text = ' '.join([w for w in word_tokenize(
        out_text) if w not in stopwords.words('portuguese')])
    out_text = re.sub(r'[0-9]{5,}', '', out_text)
    return out_text

# %%
# Main


if __name__ == "__main__":
    print('Carregando dados')
    unlabeled_data = pd.read_csv('nfedataNoEAN.csv', low_memory=False)
    unlabeled_data['codigo_ean'] = np.array(['outro'] * len(unlabeled_data))
    unlabeled_X = unlabeled_data.loc[:, 'produto_descricao']
    unlabeled_X = unlabeled_X.apply(descricao_preprocessing)

    data = pd.read_csv('nfedataEAN.csv',
                       low_memory=False, encoding='utf-8')
    X = data.loc[:, 'produto_descricao']
    X = X.apply(descricao_preprocessing)
    cod = data.loc[:, 'produto_codigo_ean'].value_counts().index.tolist()
    
    print('Iniciando loop')
    # For loop to get each next 100 elements of the list
    for i in range(1, len(cod), 100):
        # Get the next 100 elements
        offset = -1 if i + 100 > len(cod) else (i + 100)
        cod_sub = cod[i:offset]
        cod_sub = list(map(str, cod_sub[1:100]))
        y = data.loc[:, 'produto_codigo_ean'].apply(
            lambda x: str(x) if str(x) in cod_sub else 'outro')
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=seed)
        vectorizer = CountVectorizer(analyzer='word', ngram_range=(1, 3))
        X_train_vectorized = vectorizer.fit_transform(X_train)
        X_test_vectorized = vectorizer.transform(X_test)
        clf = RandomForestClassifier(
            n_estimators=1000, random_state=seed, n_jobs=-1)
        clf.fit(X_train_vectorized, y_train)
        y_pred = clf.predict(X_test_vectorized)
        print(classification_report(y_test, y_pred))
        print()
        mask = unlabeled_data.loc[:, 'codigo_ean'] == 'outro'
        unlabeled_data.loc[mask, 'codigo_ean'] = clf.predict(
            vectorizer.transform(unlabeled_X.loc[mask]))

        unlabeled_data.to_csv('nfedataEAN_with_codigo_ean.csv', index=False)
