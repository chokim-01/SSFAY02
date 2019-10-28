from sklearn.linear_model import LogisticRegression
from scipy.sparse import lil_matrix
from konlpy.tag import Okt
import conn.conn as conn
import numpy as np
import time
import datetime
import pymysql
import pickle
import nltk

train_docs = None
word_indices = dict()


# Tokenize text
def tokenize_data(data_row):
    okt = Okt()
    return ['/'.join(t) for t in okt.pos(data_row, norm=True, stem=True)]


# Get data from Database
def load_data():
    global train_docs
    db = conn.db()
    cursor = db.cursor()

    sql = "select comment_context, label_news, label_local from comments"
    cursor.execute(sql)
    result = cursor.fetchall()

    print("[+] Load from DB")
    train_docs = [(tokenize_data(data_row["comment_context"]), data_row["label_news"], data_row["label_local"]) for data_row in result]
    print("[+] Tokenize")


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

    print("[+] Make word_indices")


# one hot embedding
def make_sparse_matrix():
    global train_docs, word_indices

    train_len = len(train_docs)
    word_indices_len = len(word_indices) + 1

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
    local_model = LogisticRegression().fit(x_train,y_train_local)

    pickle.dump(news_model, open("../Model/news_model_server.clf", "wb"))
    pickle.dump(local_model, open("../Model/local_model_server.clf","wb"))
    pickle.dump(word_indices, open("../Model/word_indices_server.clf", "wb"))
    
    print("[+] Make model")


def main():
    start_time = str(datetime.datetime.now())

    load_data()
    make_word_indices()
    x_train, y_train = make_sparse_matrix()
    make_model(x_train, y_train)
    end_time = str(datetime.datetime.now())

    file_time = open("time.log","w")
    file_time.write(start_time+"\n")
    file_time.write(end_time)
    file_time.close()

if __name__ == '__main__':
    main()
