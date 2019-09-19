from flask import Flask, request, jsonify
import pymysql

app = Flask(__name__)


@app.route("/api/chatbottest", method=["POST"])
def chatbot_test():
    msg = request.form.get("msg")
    conn = pymysql.connect(host='localhost', user='root', password='1234', db='testdb', charset='utf8')
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    sql = "select * from chatbot where msg = %s"
    cursor.execute(sql, msg)

    rows = cursor.fetchall()
    return jsonify(rows)

    conn.close()
