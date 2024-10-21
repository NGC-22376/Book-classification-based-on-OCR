import time
import paddleocr
import pymysql
from config import sql_msg, book_names,path_msg
from pymysql import Error

ocr = paddleocr.PaddleOCR()


def classify(image_path):
    result = ocr.ocr(image_path, cls=True)
    m = None
    n = None
    book_to_category = {book: category for category, books in book_names.items() for book in books}
    for line in result:
        for word in line:
            text = word[1][0]
            for book, category in book_to_category.items():
                if book in text:
                    n = book
                    m = category
                    break
            if n:
                break
        if n:
            break
    db = pymysql.connect(host=sql_msg['my_host'],
                         user=sql_msg['my_root'],
                         password=sql_msg['my_password'],
                         database=sql_msg['book_database'])

    t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL查询id
    sql1 = "SELECT `cate_id`,`parent_id` FROM `books_category` WHERE `name` = '%s'" % n
    try:
        # 执行sql语句
        cursor.execute(sql1)
        # 获取记录列表
        cate_id1 = cursor.fetchone()
        cate_id2 = cate_id1[0]
        cate_id3 = cate_id1[1]
        if not cate_id2:
            print("no found")

    except Exception as e:
        print("Error:unable to insert data", e)

    # SQL 插入语句
    sql2 = "INSERT INTO `books_count`\
               VALUES ('%d', '%s', 1,'%s','%d')" % \
           (cate_id2, t, n, cate_id3)

    try:
        # 执行sql语句
        cursor.execute(sql2)
        # 提交sql事务
        db.commit()
    except Error as e:
        # 发生错误时回滚
        print(e)
        db.rollback()
    db.close()

    if m == '数理基础类':
        m = 0
        if n == '微积分':
            n = 0
        elif n == '线性代数':
            n = 1
    if m == '历史哲学类类':
        m = 1
        if n == '论语':
            n = 0
        elif n == '中国近现代史纲要':
            n = 1
    if m == '计算机专业类':
        m = 2
        if n == '计算机组成与系统结构':
            n = 0
        elif n == '离散数学':
            n = 1
    if m == '小说文学类':
        m = 3
        if n == '哈利·波特':
            n = 0
        elif n == '朝花夕拾':
            n = 1

    # 分类结果写入result.txt
    with open(path_msg["result_path"], 'w') as f:
        f.write(f"{m}\n{n}")