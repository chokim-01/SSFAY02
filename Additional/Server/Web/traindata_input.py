import conn.conn as conn
import pickle


# Load data
def load_data():
    # Get news data
    with open('../../crawling/news_data2.clf', 'rb') as news_data:
        news_data = pickle.load(news_data)

    news_len = len(news_data)

    news_d = [[_ for _ in range(4)] for _ in range(news_len)]

    # Count of Deduplication
    input_count = 0
    blank_count = 0

    for news_idx in range(news_len):
        flag = False

        # Skip duplicate news
        for news_before in range(news_idx):
            if news_data[news_idx][0] == news_d[news_before][0]:
                flag = True
                blank_count += 1
                break

        if flag:
            continue

        news_d[input_count] = news_data[news_idx]
        input_count += 1

    news_d = news_d[:input_count]

    # Get comment data
    with open('../../crawling/comment_data2.clf', 'rb') as comments:
        comments_data = pickle.load(comments)
    
    comments_len = len(comments_data)

    # Comment data formmatting
    for cmt_idx in range(comments_len):
        comments_data[cmt_idx].append(int(0))
        comments_data[cmt_idx].append(int(0))
        comments_data[cmt_idx][0] = int(comments_data[cmt_idx][0])

    print(len(news_d))
    print(len(comments_data))
    return news_d, comments_data


# Add News test case to DB
def add_news(news_data):
    db = conn.db()
    cursor = db.cursor()

    sql = "insert into news (news_num, news_title, news_context, news_date) values(%s, %s, %s, %s)"
    cursor.executemany(sql, news_data)
    db.commit()

    return ""


# Add comment case to DB
def add_comment(comments_data):
    db = conn.db()
    cursor = db.cursor()

    sql = "insert into comments(news_num, comment_context, comment_time," \
          " label_news, label_local) values (%s, %s, %s, %s, %s)"

    cursor.executemany(sql, comments_data)
    db.commit()

    return


# check table news duplicate
def check_news_duplicate():
    db = conn.db()
    cursor = db.cursor()

    news_data, comments_data = load_data()

    for news in news_data:
        print(news)
        sql = "select count(*) as count from news where news_num = %s"
        cursor.executemany(sql, news)

        rows = cursor.fetchall()
        print(rows[0]['count'])
        if rows[0]['count'] >= 1:
            del news_data[news]

    return news_data, comments_data


def add_testcase():
    news_data, comments_data = check_news_duplicate()

    add_news(news_data)
    add_comment(comments_data)

    return


def main():
    add_testcase()

    return


if __name__ == '__main__':
    main()
