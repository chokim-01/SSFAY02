from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from scipy.sparse import lil_matrix
from konlpy.tag import Okt
import pandas as pd
import numpy as np
import pymysql
import pickle
import nltk
import re
import decode

# Train data frame
data_frame = None

# Train docs About label_news & label_local
train_docs_news, train_docs_local = None
word_indices = dict()


def tokenize_data(data_row):
    okt = Okt()
    return ['/'.join(t) for t in okt.pos(data_row, norm=True, stem=True)]


# Get data from Database
def load_data():
    global data_frame, train_docs_news, train_docs_local

    data_frame = pd.read_csv("../Data/data.txt", sep="/~/").dropna()[["context", "label_news", "label_local"]].values

    # About news
    train_docs_news = [(tokenize_data(train_data_row[0]), train_data_row[1]) for train_data_row in train_data_frame]

    train_docs_local = train_docs_news

    data_len = len(train_docs_local)
    for idx in range(data_len):
        train_docs_local[idx][1] = train_data_frame[idx][2]

    return train_docs.tolist()


# make word_indices
def make_word_indices():
    global train_docs, word_indices
    train_tokens = [token for train_doc in train_docs for token in train_doc[0]]

    train_text = nltk.Text(train_tokens, name='NMSC')

    idx = 0
    for txt in train_text.vocab().items():
        print(txt)
        word = txt[0].split("/")[0]
        if not word_indices.get(word):
            word_indices[word] = idx
            idx += 1


# one hot embedding
def make_sparse_matrix():
    global train_docs, word_indices

    train_len = len(train_docs)
    word_indices_len = len(word_indices) + 1

    x_train = lil_matrix((train_len, word_indices_len), dtype=np.int64)
    y_train = np.zeros((train_len,2))

    for idx, data in enumerate(train_docs):
        y_train[idx][0] = data[1]
        y_train[idx][1] = data[2]
        for token in data[0]:
            x_train[idx, word_indices[token.split("/")[0]]] = 1

    return x_train, y_train


# Make model
def make_model(x_train, y_train):

    y_train_naive = [row[0] for row in y_train]
    y_train_logistic = [row[1] for row in y_train]

    multinomial_nb_model = MultinomialNB().fit(x_train, y_train_naive)
    logistic_regression_model = LogisticRegression().fit(x_train, y_train_logistic)

    pickle.dump(multinomial_nb_model, open("/home/ubuntu/front/ai-sub2/Model/multinomial_nb_model.clf", "wb"))
    pickle.dump(logistic_regression_model, open("/home/ubuntu/front/ai-sub2/Model/logistic_regression_model.clf", "wb"))
    pickle.dump(word_indices, open("/home/ubuntu/front/ai-sub2/Model/word_indices.clf", "wb"))


def main():
    load_data()
    make_word_indices()
    # x_train, y_train = make_sparse_matrix()
    # make_model(x_train, y_train)


if __name__ == '__main__':
    main()
