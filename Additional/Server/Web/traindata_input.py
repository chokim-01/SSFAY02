import conn.conn as conn
import pickle


# Load data
def load_data():
    # Get news data
    with open('../../crawling/news_data.clf', 'rb') as news_data:
        news_data = pickle.load(news_data)

    news_len = len(news_data)

    news_d = [[ _ for _ in range(4)] for _ in range(news_len)]

    # Count of Deduplication
    input_count = 0
    blank_count = 0

    for idx in range(news_len):
        flag = False
        for i in range(idx-1):
            if int(news_data[idx][0]) == news_d[i][0]:
                flag = True
                blank_count +=1
                break
        if flag:
            continue

        # news num, title, context, date formating
        news_d[input_count][0] = int(news_data[idx][0])
        news_d[input_count][1] = news_data[idx][1]
        news_d[input_count][2] = news_data[idx][2]
        news_d[input_count][3] = int(news_data[idx][3])

        input_count +=1

    news_d = news_d[:news_len-blank_count]

    # Get comment data
    with open('../../crawling/comment_data.clf', 'rb') as comments:
        comments_data = pickle.load(comments)

    comments_len = len(comments_data)

    # comments news_num, context, date formating
    comments_d = [[ _ for _ in range(2)] for _ in range(comments_len)]
    for idx in range(comments_len):
        comments_d[idx][0] = int(comments_data[idx][0])
        comments_d[idx][1] = comments_data[idx][1]

    return news_d, comments_d


# Add News test case to DB
def add_news(news_data):

    print(" Input News start")
    db = conn.db()
    cursor = db.cursor()

    sql = "insert into News (news_num, news_title, news_context, news_date) values(%s, %s, %s, %s)"
    cursor.executemany(sql, news_data)
    db.commit()

    return ""


# Add comment case to DB
def add_comment(comments_data):

    db = conn.db()
    cursor = db.cursor()

    cnt = 0
    for comment in comments_data:
        comment.append(0)
        comment.append(0)
        cnt +=1

    sql = "insert into comments(news_num, comment_context, label_news, label_local) values (%s, %s, %s, %s)"

    cursor.executemany(sql, comments_data)
    db.commit()

    return


def add_testcase():
    news_data, comments_data = load_data()
    add_news(news_data)
    add_comment(comments_data)

    return


def main():
    add_testcase()

    return


if __name__ == '__main__':
    main()
