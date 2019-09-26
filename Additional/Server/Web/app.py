import tensorflow as tf
import Preprocessing
import model as ml
from config import DEFINES

from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import conn.conn as conn

# Get file path
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
STATIC_PATH = os.path.join(ROOT_PATH + "\\..\\..\\frontend", 'dist')
print(STATIC_PATH)
app = Flask(__name__, static_folder=STATIC_PATH, static_url_path='')

# Set CORS
cors = CORS(app, resources={
    r"/api/*": {"origin": "*"}
})


# Set directory path for vue
@app.route("/")
def main():
    return app.send_static_file("index.html")


###################################################
#   News section
###################################################
# Get news
@app.route("/api/get/news", methods=["POST"])
def get_news():
    cursor = conn.db().cursor()

    date = int(request.form.get("date"))
    page = int(request.form.get("page"))
    limit = (page - 1) * 5

    sql = "select * from news where news_date = %s order by news_num limit %s, 5"
    cursor.execute(sql, (date, limit))
    result = cursor.fetchall()

    return jsonify(result)


# Get news count
@app.route("/api/get/news_count", methods=["POST"])
def get_news_count():
    cursor = conn.db().cursor()

    date = int(request.form.get("date"))

    sql = "select count(*) from news where news_date = %s"
    cursor.execute(sql, date)
    result = cursor.fetchall()

    return jsonify(result)


# Search news
@app.route("/api/get/search", methods=["POST"])
def get_search_news():
    cursor = conn.db().cursor()

    category = request.form.get("searchCat")
    keyword = request.form.get("searchKey")
    page = int(request.form.get("page"))

    page = (page - 1) * 5

    if category == "제목":
        result = get_news_by_title(keyword, page)
    elif category == "태그":
        result = get_news_by_tags(keyword, page)
    else:
        result = get_news_by_date(keyword, page)

    return jsonify(result)


# Get search_news count
@app.route("/api/get/search_count", methods=["POST"])
def get_search_news_count():
    cursor = conn.db().cursor()

    category = request.form.get("searchCat")
    keyword = request.form.get("searchKey")

    if category == "제목":
        result = get_news_count_by_title(keyword)
    elif category == "태그":
        result = get_news_count_by_tags(keyword)
    else:
        result = get_news_count_by_date(keyword)

    return jsonify(result)


# Get news by tag
def get_news_by_tags(tag, page):
    cursor = conn.db().cursor()

    sql = "select * from news n, tag t where t.tag_name like %s and n.news_num = t.news_num limit %s, 5"

    cursor.execute(sql, (tag, page))
    result = cursor.fetchall()

    return result


# Get news count by tags
def get_news_count_by_tags(tag):
    cursor = conn.db().cursor()

    sql = "select count(*) from news n, tag t where t.tag_name like %s and n.news_num = t.news_num"

    cursor.execute(sql, tag)
    result = cursor.fetchall()

    return result


# Get news by title
def get_news_by_title(title, page):
    cursor = conn.db().cursor()
    title = "%"+title+"%"

    sql = "select * from news where news_title like %s limit %s, 5"
    cursor.execute(sql, (title, page))
    result = cursor.fetchall()

    return result


# Get news count by title
def get_news_count_by_title(title):
    cursor = conn.db().cursor()
    title = "%"+title+"%"

    sql = "select count(*) from news where news_title like %s"
    cursor.execute(sql, title)
    result = cursor.fetchall()

    return result


# Get news by date
def get_news_by_date(date, page):
    cursor = conn.db().cursor()

    sql = "select * from news where news_date = %s limit %s, 5"
    cursor.execute(sql, (date, page))
    result = cursor.fetchall()

    return result


# Get news count by date
def get_news_count_by_date(date):
    cursor = conn.db().cursor()

    sql = "select count(*) from news where news_date = %s"
    cursor.execute(sql, date)
    result = cursor.fetchall()

    return result

# Get news by tags
@app.route("/api/get/tags", methods=["POST"])
def get_tags():
    cursor = conn.db().cursor()

    news_num = int(request.form.get("news_num"))

    sql = "select tag_name from tag where news_num = %s"

    cursor.execute(sql, news_num)
    result = cursor.fetchall()

    return jsonify(result)

# Get news by title
@app.route("/api/get/news_title", methods=["POST"])
def get_news_by_title():
    cursor = conn.db().cursor()

    title = int(request.form.get("title"))

    sql = "select * from news where title like '%%s%"
    cursor.execute(sql, title)
    result = cursor.fetchall()

    return jsonify(result)



###################################################
#   Comments section
###################################################

# Get comment
@app.route("/api/get/comments", methods=["POST"])
def get_comments():
    cursor = conn.db().cursor()

    news_num = int(request.form.get("news_num"))
    page = int(request.form.get("page"))
    limit = (page - 1) * 30
    sql = "select * from comments where news_num = %s order by comment_num limit %s, 30"
    cursor.execute(sql, (news_num, limit))
    result = cursor.fetchall()

    return jsonify(result)

# Get comments Total Count
@app.route("/api/get/page_count", methods=["POST"])
def get_start_page_end_page():
    cursor = conn.db().cursor()

    page = int(request.form.get("page"))
    news_num = int(request.form.get("news_num"))
    sql = "select count(*) as cnt from comments where news_num = %s"
    cursor.execute(sql,news_num)

    cnt_comments = cursor.fetchone()["cnt"]

    final_page = int(cnt_comments / 30)
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



# Get comment_time
@app.route("/api/get/comments_time", methods=["POST"])
def get_comments_time():
    cursor = conn.db().cursor()

    news_num = int(request.form.get("news_num"))

    sql = "select substr(comment_time, 12, 2) as hour, count(*) as hour_cnt " \
          "from comments where news_num = %s group by hour order by hour"

    cursor.execute(sql, news_num)
    result = cursor.fetchall()

    return jsonify(result)


# Get comment_label ( positive, negative)
@app.route("/api/get/comments_label", methods=["POST"])
def get_comments_label():
    cursor = conn.db().cursor()

    news_num = int(request.form.get("news_num"))

    sql = "select sum(label_news) as news_positive, sum(label_local) as local_hit, count(*) as comment_cnt " \
          "from comments where news_num = %s"
    cursor.execute(sql, news_num)
    result = cursor.fetchall()

    return jsonify(result)


###################################################
#   Comments section
###################################################


###################################################
#   Chatbot
###################################################

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


def predict(question):
    tf.logging.set_verbosity(tf.logging.ERROR)
    arg_length = len(question)

    if (arg_length < 2):
        raise Exception("Don't call us. We'll call you")

    # load dictionary
    char2idx, idx2char, vocabulary_length = Preprocessing.load_vocabulary()

    # make test data
    input = str(question)

    # encoding / decoding
    predic_input_enc, predic_input_enc_length = Preprocessing.encode_processing([input], char2idx)
    predic_output_dec, predic_output_dec_length = Preprocessing.decode_processing([""], char2idx)
    predic_target_dec = Preprocessing.decode_target_processing([""], char2idx)

    # Estimator
    classifier = tf.estimator.Estimator(
        model_fn=ml.Model,
        model_dir=DEFINES.check_point_path,
        params={
            'embedding_size': DEFINES.embedding_size,
            'model_hidden_size': DEFINES.model_hidden_size,
            'ffn_hidden_size': DEFINES.ffn_hidden_size,
            'attention_head_size': DEFINES.attention_head_size,
            'learning_rate': DEFINES.learning_rate,
            'vocabulary_length': vocabulary_length,
            'layer_size': DEFINES.layer_size,
            'max_sentence_length': DEFINES.max_sentence_length,
            'xavier_initializer': DEFINES.xavier_initializer
        })

    predictions = classifier.predict(
        input_fn=lambda: Preprocessing.eval_input_fn(predic_input_enc, predic_output_dec, predic_target_dec, 1))

    answer, finished = Preprocessing.predict_next_sentence(predictions, idx2char)

    return answer


@app.route("/api/chat", methods=['POST'])
def chat_test():
    msg = request.form.get("msg")

    answer = predict(msg)

    return jsonify(answer)

#########################################


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
