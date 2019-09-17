from scipy.sparse import lil_matrix
from konlpy.tag import Okt
import numpy as np
import pickle
import conn.conn as conn

with open('../../Model/logistic_regression_model.clf', 'rb') as model:
    logistic_regression_model = pickle.load(model)

with open('../../Model/word_indices.clf', 'rb') as model:
    word_indices = pickle.load(model)


# Tokenize data
def tokenize_data(data_row):
    """
    :param data_row:
    :return: tokenize data ([word/morpheme, word/morpheme, word/morpheme, ...]
    """
    okt = Okt()

    return ['/'.join(t) for t in okt.pos(data_row, norm=True, stem=True)]


# Logistic Regression Model
def load_logistic_mention(mention):
    global logistic_regression_model, word_indices
    mention_token_data = tokenize_data(mention)

    x_mention = lil_matrix((1, len(word_indices) + 1), dtype=np.int64)

    for token in mention_token_data:
        word = token.split("/")[0]
        if word in word_indices:
            x_mention[0, word_indices[word]] = 1

    return int(logistic_regression_model.predict(x_mention)[0])


# Load data
def load_data():
    # Get data
    with open('../../Data/train_news_data.clf', 'rb') as news_data:
        news_data = pickle.load(news_data)

    with open('../../Data/train_comments_data.clf', 'rb') as comment_data:
        comments_data = pickle.load(comment_data)

    return news_data, comments_data


# Add News test case to DB
def add_news():
    db = conn.db()
    cursor = db.cursor()

    news_data, comments_data = load_data()

    sql = "insert into News (news_title, news_context, news_date) values()"
    cursor.executemany(sql, news_data)
    db.commit()

    add_comment()

    return ""


# Add comment case to DB
def add_comment(comments_data):
    db = conn.db()
    cursor = db.cursor()

    for comment in comments_data:
        comment.append(load_logistic_mention(comment[1]))

    sql = "insert into comments(news_num, context, label_news, label_local) values ()"

    cursor.executemany(sql, comments_data)
    db.commit()


def add_testcase():
    news_data, comments_data = load_data()
    add_news(news_data)
    add_comment(comments_data)


def main():
    add_testcase()


if __name__ == '__main__':
    main()
