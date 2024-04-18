import time

import cv2
import paddleocr
import pymysql
from pymysql import Error

# 创建列表包括书名
book_names = ['微积分', '线性代数', '数字逻辑概论', '离散数学']

# 初始化PaddleOCR
ocr = paddleocr.PaddleOCR()

# 打开摄像头
cap = cv2.VideoCapture(0)

while cap.isOpened():
    retval, image = cap.read()
    cv2.imshow("Video", image)
    cv2.imwrite('book_photo.jpg', image)
    key = cv2.waitKey(1)
    if key == 32:
        break

# 打开数据库连接
db = pymysql.connect(host='localhost',
                     user='root',
                     password='yufei5312',
                     database='hello')

# 进行文字识别
result = ocr.ocr('book_photo.jpg', cls=True)

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

# SQL 插入语句
sql = "INSERT INTO `books`\
       VALUES (%s, %s, %d)" % \
      (n, t, 1)

try:
    # 执行sql语句
    cursor.execute(sql)
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
with open('result.txt', 'w') as f:
    f.write(f"{n}")

# 释放摄像头资源
cap.release()

# 关闭数据库连接
db.close()
