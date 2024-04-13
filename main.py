import cv2
from pymysql import Error
import paddleocr
import pymysql
import time

# 初始化PaddleOCR
ocr = paddleocr.OCR()

# 打开摄像头
cap = cv2.VideoCapture(0)

# 读取图像
ret, frame = cap.read()

# 保存图像
cv2.imwrite('book_photo.jpg', frame)

# 进行文字识别
result = ocr.ocr('book_photo.jpg', cls=True)
t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())


# 打开数据库连接
db = pymysql.connect(host='localhost',
                     user='root',
                     password='MySQL08091221',
                     database='hello')

# 使用cursor()方法获取操作游标
cursor = db.cursor()

# SQL 插入语句
sql = "INSERT INTO hello.books(root,yufei5312)\
       VALUES (%s, %s, %d)" % \
      (n, t, c)

try:
    # 执行sql语句
    cursor.execute(sql)
    # 执行sql语句
    db.commit()
except Error:
    # 发生错误时回滚
    db.rollback()

# 输出结果文件
with open('result.txt', 'w') as f:
    f.write(f"The book '{book_name}' belongs to the category '{category}'")

# 关闭数据库连接
db.close()
