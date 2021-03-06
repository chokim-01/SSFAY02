from flask import Flask, jsonify, request
from collections import Counter
from flask_cors import CORS
from config import DEFINES
from konlpy.tag import Okt
import conn.conn as conn
import tensorflow as tf
import Preprocessing
import model as ml
import os

# Get file path
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
STATIC_PATH = os.path.join(ROOT_PATH + "/../../frontend", 'dist')
app = Flask(__name__, static_folder=STATIC_PATH, static_url_path='')
LOAD_PAGE_COUNT = 3

# Set CORS
cors = CORS(app, resources={
    r"/api/*": {"origin": "*"}
})

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


# Set directory path for vue
@app.route("/")
def main():
    return app.send_static_file("index.html")


###################################################
#   News section
###################################################
# Get news from header
@app.route("/api/get/head_news", methods=["POST"])
def get_head_news():
    cursor = conn.db().cursor()

    page = int(request.form.get("page"))

    sql = "select * from news where news_date = (select news_date from news  group by news_date order by news_date desc limit 1) order by news_num desc limit %s"
    cursor.execute(sql, page)
    result = cursor.fetchall()

    return jsonify(result)


# Get One news
@app.route("/api/get/one_news", methods=["POST"])
def get_one_news():
    cursor = conn.db().cursor()

    news_num = int(request.form.get("news_num"))

    sql = "select * from news where news_num = %s"
    cursor.execute(sql, news_num)
    result = cursor.fetchall()

    return jsonify(result)


# Get news
@app.route("/api/get/news", methods=["POST"])
def get_news():
    cursor = conn.db().cursor()

    page = int(request.form.get("page"))
    limit = (page - 1) * LOAD_PAGE_COUNT

    sql = "select * from news where news_date = (select news_date from news  group by news_date order by news_date desc limit 1) order by news_num desc limit %s,%s"
    cursor.execute(sql, (limit, LOAD_PAGE_COUNT))
    result = cursor.fetchall()

    return jsonify(result)


# Get news count
@app.route("/api/get/news_count", methods=["POST"])
def get_news_count():
    cursor = conn.db().cursor()

    sql = "select count(*) from news where news_date = (select news_date from news  group by news_date order by news_date desc limit 1) order by news_num desc"
    cursor.execute(sql)
    result = cursor.fetchall()

    return jsonify(result)


# Search news
@app.route("/api/get/search", methods=["POST"])
def get_search_news():

    category = request.form.get("searchCategory")
    keyword = request.form.get("searchKey")
    page = int(request.form.get("page"))

    page = (page - 1) * LOAD_PAGE_COUNT

    if category == "title":
        result = get_news_by_title(keyword, page)
    elif category == "tag":
        result = get_news_by_tags(keyword, page)
    else:
        result = get_news_by_date(keyword, page)

    return jsonify(result)


# Get search_news count
@app.route("/api/get/search_count", methods=["POST"])
def get_search_news_count():
    category = request.form.get("searchCategory")
    keyword = request.form.get("searchKey")

    if category == "title":
        result = get_news_count_by_title(keyword)
    elif category == "tag":
        result = get_news_count_by_tags(keyword)
    else:
        result = get_news_count_by_date(keyword)

    return jsonify(result)


# Get news by tag
def get_news_by_tags(tag, page):
    cursor = conn.db().cursor()

    sql = "select * from news n, newstag t where t.newstag_name like %s and n.news_num = t.news_num limit %s, %s"

    cursor.execute(sql, (tag, page, LOAD_PAGE_COUNT))
    result = cursor.fetchall()

    return result


# Get news count by tags
def get_news_count_by_tags(tag):
    cursor = conn.db().cursor()

    sql = "select count(*) from news n, newstag t where t.newstag_name like %s and n.news_num = t.news_num"

    cursor.execute(sql, tag)
    result = cursor.fetchall()

    return result


# Get news by title
def get_news_by_title(title, page):
    cursor = conn.db().cursor()
    title = "%"+title+"%"

    sql = "select * from news where news_title like %s limit %s, %s"
    cursor.execute(sql, (title, page, LOAD_PAGE_COUNT))
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

    sql = "select * from news where news_date = %s limit %s, %s"
    cursor.execute(sql, (date, page, LOAD_PAGE_COUNT))
    result = cursor.fetchall()

    return result


# Get news count by date
def get_news_count_by_date(date):
    cursor = conn.db().cursor()

    sql = "select count(*) from news where news_date = %s"
    cursor.execute(sql, date)
    result = cursor.fetchall()

    return result

###################################################
#   Cloud section
###################################################


# Get news by newstags
@app.route("/api/get/newstags", methods=["POST"])
def get_newstags():
    cursor = conn.db().cursor()

    news_num = int(request.form.get("news_num"))

    sql = "select newstag_name from newstag where news_num = %s limit 0,10"

    cursor.execute(sql, news_num)
    result = cursor.fetchall()

    return jsonify(result)


# Get news_tag for news cloud
@app.route("/api/get/news_cloud", methods=["POST"])
def get_news_cloud():
    cursor = conn.db().cursor()

    news_num = int(request.form.get("news_num"))

    sql = "select newstag_name as newstagname, newstag_count as newstagcount from newstag where news_num = %s"
    cursor.execute(sql, news_num)
    result = cursor.fetchall()

    return jsonify(result)


# Get comments for news cloud
@app.route("/api/get/comments_cloud", methods=["POST"])
def get_comments_cloud():
    cursor = conn.db().cursor()

    news_num = int(request.form.get("news_num"))

    sql = "select commentstag_name as commentstagname, commentstag_count as commentstagcount" \
          " from commentstag where news_num = %s"
    cursor.execute(sql, news_num)
    result = cursor.fetchall()

    return jsonify(result)


###################################################
#   Cloud section
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
    cursor.execute(sql, news_num)

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


# Edit comment label news
@app.route("/api/edit/label_news", methods=["POST"])
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

    sql = "update comments set label_news =%s where comment_num=%s"
    cursor.execute(sql, (label, num))
    db.commit()
    return ""


# Edit comment label local
@app.route("/api/edit/label_local", methods=["POST"])
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

    sql = "update comments set label_local =%s where comment_num=%s"
    cursor.execute(sql, (label, num))
    db.commit()
    return ""


###################################################
#   Comments section
###################################################


###################################################
#   Chat bot
###################################################


# Search chat
@app.route("/api/get/chat", methods=['POST'])
def chat_search():
    okt = Okt()
    msg = request.form.get("msg")
    msg = okt.nouns(msg)

    # If nouns not in msg False
    if len(msg) == 0:
        return "False"

    msg_most_nouns = Counter(msg).most_common()[0][0]

    cursor = conn.db().cursor()

    sql = "select news_num from newstag where newstag_name like %s order by newstag_count desc limit 0,5"

    cursor.execute(sql, msg_most_nouns)
    result_news = cursor.fetchall()
    
    # If tag not in table False
    if len(result_news) < 1:
        return "False"

    else:
        # Get tags from table
        news_list = [str(item['news_num']) for item in result_news]
        result = [] 
        
        sql = "select n.news_num, news_title, newstag_name from news n inner join newstag nt on n.news_num = nt.news_num and n.news_num = %s limit 5"
        for newsnum in news_list:
            cursor.execute(sql, newsnum)
            result.append(cursor.fetchall())
        
        print(result)
        return jsonify(result)


def main():
    app.run(debug=True, host="0.0.0.0")


if __name__ == '__main__':
    main()
