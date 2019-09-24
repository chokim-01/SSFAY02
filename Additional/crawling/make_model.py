from sklearn.linear_model import LogisticRegression
from scipy.sparse import lil_matrix
from konlpy.tag import Okt
import pandas as pd
import numpy as np
import pymysql
import pickle
import time
import nltk
import re

# Train data frame
data_frame = None

# Train docs About label_news & label_local
train_docs = None
word_indices = dict()


def tokenize_data(data_row):
    okt = Okt()
    return ['/'.join(t) for t in okt.pos(data_row, norm=True, stem=True)]


# Get data from Database
def load_data():
    global data_frame, train_docs

    data_frame = pd.read_csv("../Data/data.txt", sep="/~/").dropna()[["context", "label_news", "label_local"]].values
    print("[+] Load")
    # About news
    train_docs = [(tokenize_data(train_data_row[0]), train_data_row[1], train_data_row[2]) for train_data_row in data_frame]

    print("[+] Tokenize")

    return train_docs


# make word_indices
def make_word_indices():
    global train_docs, word_indices

    train_tokens = [token for train_doc in train_docs for token in train_doc[0]]

    train_text = nltk.Text(train_tokens, name='NMSC')

    idx = 0
    for txt in train_text.vocab().items():
        word = txt[0].split("/")[0]
        if not word_indices.get(word):
            word_indices[word] = idx
            idx += 1

    print("[+] Make word")

    return


# one hot embedding
def make_sparse_matrix():
    global train_docs, word_indices

    train_len = len(train_docs)
    word_indices_len = len(word_indices)

    x_train = lil_matrix((train_len, word_indices_len), dtype=np.int64)
    y_train = np.zeros((train_len, 2))

    for idx, data in enumerate(train_docs):
        y_train[idx][0] = data[1]
        y_train[idx][1] = data[2]
        for token in data[0]:
            x_train[idx, word_indices[token.split("/")[0]]] = 1

    print("[+] Make matrix")

    return x_train, y_train


# Make model
def make_model(x_train, y_train):

    y_train_news = [row[0] for row in y_train]
    y_train_local = [row[1] for row in y_train]

    news_model = LogisticRegression().fit(x_train, y_train_news)
    local_model = LogisticRegression().fit(x_train, y_train_local)

    pickle.dump(news_model, open("../Model/news_model.clf", "wb"))
    pickle.dump(local_model, open("../Model/local_model.clf", "wb"))
    pickle.dump(word_indices, open("../Model/word_indices.clf", "wb"))

    print(" [+] Make model")


def main():
    start = time.time()
    load_data()
    make_word_indices()
    x_train, y_train = make_sparse_matrix()
    make_model(x_train, y_train)

    print("End : ", time.time() - start)


if __name__ == '__main__':
    main()
