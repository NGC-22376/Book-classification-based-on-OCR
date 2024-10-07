import time
import paddleocr
import pymysql
from config import sql_msg, path_msg, book_names
from pymysql import Error



ocr = paddleocr.PaddleOCR()

db = pymysql.connect(host=sql_msg['my_host'],
                     user=sql_msg['my_root'],
                     password=sql_msg['my_password'],
                     database=sql_msg['book_database'])

result = ocr.ocr(path_msg['photo_path'], cls=True)

m = None
n = 'NULL'
for line in result:
    for word in line:
        text = word[1][0]
        for category in book_names.keys():
            for books in book_names.values():
                for book in books:
                    if book in text:
                        n = book
                        m = category
                    if n:
                        break
        if n:
            break
    if n:
        break


t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

# 使用cursor()方法获取操作游标
cursor = db.cursor()

# SQL查询id
sql1 = "SELECT `cate_id` FROM `books_category` WHERE `name` = '%s'" % n
try:
    # 执行sql语句
    cursor.execute(sql1)
    # 获取记录列表
    cate_id = cursor.fetchone()
    if not cate_id:
        print("no found")

except Exception:
    print("Error:unable to insert data")

# SQL 插入语句
sql2 = "INSERT INTO `books_count`\
       VALUES ('%s', '%s', '1','%s')" % \
       (cate_id, t, n)

try:
    # 执行sql语句
    cursor.execute(sql2)
    # 提交sql事务
    db.commit()
except Error:
    # 发生错误时回滚
    db.rollback()

#  转换为数字
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
    elif n == '中国近代史纲要':
        n = 1
if m == '计算机专业类':
    m = 2
    if n == '计算机组成与系统结构':
        n = 0
    elif n == '离散数学':
        n = 1
if m == '小说文学类':
    n = 3
    if n == '哈利·波特':
        n = 0
    elif n == '朝花夕拾':
        n = 1

# 输出结果文件
with open(path_msg["result_path"], 'w') as f:
    f.write(f"{m}\n{n}")

db.close()
