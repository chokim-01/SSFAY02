from flask import Flask, jsonify, request
from scipy.sparse import lil_matrix
from flask_cors import CORS
from konlpy.tag import Okt
import numpy as np
import pickle
import os
import conn.conn as conn

# Get file path
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
STATIC_PATH = os.path.join(ROOT_PATH + "\\..\\..\\front_testdatainput",'dist')
print(STATIC_PATH)
app = Flask(__name__, static_folder=STATIC_PATH, static_url_path='')

# Get ai model

with open('../../Model/logistic_regression_model.clf', 'rb') as model:
    logistic_regression_model = pickle.load(model)

with open('../../Model/word_indices.clf', 'rb') as model:
    word_indices = pickle.load(model)

# Set CORS
cors = CORS(app, resources={
    r"/api/*": {"origin": "*"}
})


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


# Set directory path for vue
@app.route("/")
def main():
    return app.send_static_file("index.html")


# Get comments Total Count
@app.route("/api/get/page_count", methods=["POST"])
def get_start_page_end_page():
    cursor = conn.db().cursor()

    page = int(request.form.get("page"))

    sql = "select count(*) as cnt from comments_train"
    cursor.execute(sql)

    cnt_comments = cursor.fetchone()["cnt"]

    final_page = int(cnt_comments / 100)
    start_page = page - 2

    if start_page <= 0:
        start_page = 1

    end_page = page + 3
    if end_page >= final_page:
        end_page = final_page

    page_list = []
    for i in range(start_page, end_page):
        page_list.append(i)

    page_data = {"page_list": page_list, "final_page": final_page}

    return jsonify(page_data)


# Get comment_page
@app.route("/api/get/comments_page", methods=["POST"])
def get_comments_page():
    cursor = conn.db().cursor()

    page = int(request.form.get("page"))
    limit = (page - 1) * 100

    sql = "select * from comments_train order by comment_num limit %s, 100"
    cursor.execute(sql, limit)
    result = cursor.fetchall()

    return jsonify(result)


# Insert comments
@app.route("/api/insert/comments", methods=["POST"])
def comment_push():
    db = conn.db()
    cursor = db.cursor()

    context = request.form.get("context")

    # calc label
    label = load_logistic_mention(context)
    sql = "insert into comments_train(context, label) values(%s, %s)"
    cursor.execute(sql, (context, label))
    db.commit()

    return jsonify(label)


# Edit comment label naive
@app.route("/api/edit/labelnews", methods=["POST"])
def label_news_edit():
    db = conn.db()
    cursor = db.cursor()

    num = request.form.get("num")
    label = request.form.get("label_news")

    label = int(label)
    if label == 1:
        label = 0
    else:
        label = 1

    sql = "update comments_train set label_news =%s where comment_num=%s"
    cursor.execute(sql, (label, num))
    db.commit()
    return ""


@app.route("/api/edit/labellocal", methods=["POST"])
def label_local_edit():
    db = conn.db()
    cursor = db.cursor()

    num = request.form.get("num")
    label = request.form.get("label_local")

    label = int(label)
    if label == 1:
        label = 0
    else:
        label = 1

    sql = "update comments_train set label_local =%s where comment_num=%s"
    cursor.execute(sql, (label, num))
    db.commit()
    return ""


# Del comment
@app.route("/api/del/comments", methods=["POST"])
def comment_del():
    db = conn.db()
    cursor = db.cursor()

    num = request.form.get("num")

    sql = "delete from comments_train where comment_num = %s"
    cursor.execute(sql, num)
    db.commit()

    return ""


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
