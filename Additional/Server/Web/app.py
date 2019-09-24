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
    cursor.execute(sql, date, limit)
    result = cursor.fetchall()

    return jsonify(result)


# Get news by tag

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
#   News section
###################################################


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
    cursor.execute(sql, news_num, limit)
    result = cursor.fetchall()

    return jsonify(result)


# Get comment_time
@app.route("/api/get/comments_time", methods=["POST"])
def get_comments_time():
    cursor = conn.db().cursor()

    news_num = int(request.form.get("news_num"))

    sql = "select substr(comment_time, 12, 2) as hour, count(*) as hour_cnt " \
          "from comments where news_num = %s group by hour"
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


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
