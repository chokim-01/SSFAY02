from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql

app = Flask(__name__)
CORS(app)


@app.route("/api/chat", methods=['POST'])
def chat_test():
    msg = request.form.get("msg")
    conn = pymysql.connect(host='localhost', user='root', password='1234', db='testdb', charset='utf8')
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    sql = "select * from chatbot where msg = %s"

    cursor.execute(sql, msg)
    rows = cursor.fetchall()
    conn.close()
    return jsonify(rows)


def main():
    app.run()


if __name__ == '__main__':
    main()
