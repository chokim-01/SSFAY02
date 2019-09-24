from scipy.sparse import lil_matrix
from konlpy.tag import Okt
import numpy as np
import pymysql
import pickle

# Load Model using pickle
with open('../Model/news_model.clf', 'rb') as models:
    news_model = pickle.load(models)

with open('../Model/local_model.clf', 'rb') as models:
    local_model = pickle.load(models)

with open('../Model/word_indices.clf', 'rb') as models:
    word_indices = pickle.load(models)


# Get connection
def get_connection():
    return pymysql.connect(host='localhost', user='root', password='toor', db='ssafynews_ai', charset="utf8", cursorclass=pymysql.cursors.DictCursor)


# Get cursor
def get_cursor(db):
    return db.cursor(pymysql.cursors.DictCursor)


# Tokenize mention
def tokenize_mention(data_row):
    """
    :param data_row:
    :return: tokenize data ([word/morpheme, word/morpheme, word/morpheme, ...]
    """
    okt = Okt()

    return ['/'.join(t) for t in okt.pos(data_row, norm=True, stem=True)]


def load_mention(mention):
    """
    :param mention: sentence
    :return: negative 0, positive 1
    """

    # tokenize_mention of mention(sentence)
    mention_token_data = tokenize_mention(mention)

    # sparse matrix of mention(sentence)
    x_mention = lil_matrix((1, len(word_indices)), dtype=np.int64)

    # set sparse matirx of mention
    for token in mention_token_data:
        word = token.split("/")[0]
        if word in word_indices:
            x_mention[0, word_indices[word]] = 1

    return int(news_model.predict(x_mention)[0]), int(local_model.predict(x_mention)[0])


# Get data from
def get_data():
    db = get_connection()
    cursor = get_cursor(db)

    sql = "select comment_context, comment_num from comments"
    cursor.execute(sql)
    result = cursor.fetchall()

    data_len = len(result)

    data_list = [[0 for _ in range(2)] for _ in range(data_len)]

    for idx in range(data_len):
        data_list[idx].append(result[idx]["comment_context"])
        data_list[idx].append(int(result[idx]["comment_num"]))

    print("[+] Load from DB")

    return data_list


def update_label(data):
    cnt = 0
    for d in data:
        label_news, label_local = load_mention(d[2])
        d[0] = label_news
        d[1] = label_local

        cnt += 1
        if cnt % 1000 == 0:
            print("cnt : ", cnt)

    print(" [+] Label change")

    db = get_connection()
    cursor = get_cursor(db)

    sql = "update comments set label_news = %s, label_local = %s, comment_context = %s where comment_num = %s"
    cursor.executemany(sql, data)
    db.commit()

    print("[+] Update to DB")


def main():

    # Get from DB
    data = get_data()
    update_label(data)

    return


if __name__ == '__main__':
    main()
