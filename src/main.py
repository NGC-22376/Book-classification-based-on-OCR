import time

from networkx.classes import add_path

from config import sql_msg, path_msg
import paddleocr
import pymysql
from pymysql import Error

# 创建列表包括书名
book_names = ['微积分', '线性代数', '数字逻辑概论', '离散数学']

# 初始化PaddleOCR
ocr = paddleocr.PaddleOCR()


# 打开数据库连接
db = pymysql.connect(host=sql_msg['my_host'],
                     user=sql_msg['my_root'],
                     password=sql_msg['my_password'],
                     database=sql_msg['book_database'])

# 进行文字识别
result = ocr.ocr(path_msg['photo_path'], cls=True)

# 遍历result列表 判断列表里的书名是否在OCR识别里
n = 'NULL'
for line in result:
    for word in line:
        text = word[1][0]
        for book_name in book_names:
            if book_name in text:
                n = book_name
                break

# 获取当前时间
t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

# 使用cursor()方法获取操作游标
cursor = db.cursor()

# SQL查询id
sql1 = "SELECT `cate_id` FROM `books_category` WHERE `name` = %s" % n
try:
    # 执行sql语句
    cursor.execute(sql1)
    # 获取记录列表
    cate_id = cursor.fetchone()
    if not cate_id:
        print("no found")

except Exception:
    print("Error:unable to insert data")

sql2 = "SELECT `parent_id` FROM `books_category` WHERE `cate_id` = %s" % cate_id
try:
    # 执行sql语句
    cursor.execute(sql2)
    # 获取记录列表
    parent_id = cursor.fetchone()
    if not parent_id:
        print("no found")

except Exception:
    print("Error:unable to insert data")

# SQL 插入语句
sql3 = "INSERT INTO `books_count`\
       VALUES ('%s', '%s', '1','%s','%s')" % \
      (cate_id, t, n,parent_id)

try:
    # 执行sql语句
    cursor.execute(sql3)
    # 提交sql事务
    db.commit()
except Error:
    # 发生错误时回滚
    db.rollback()

#  转换为数字
if n == '微积分':
    n = 0
elif n == '线性代数':
    n = 1
elif n == '数字逻辑概论':
    n = 2
elif n == '离散数学':
    n = 3
else:
    n = 4

# 输出结果文件
with open(path_msg["result_path"], 'w') as f:
    f.write(f"{n}")

# 释放摄像头资源
cap.release()

# 关闭数据库连接
db.close()
