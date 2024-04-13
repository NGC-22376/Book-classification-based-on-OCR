import cv2
import mysql.connector
from pymysql import Error
import paddleocr
import pymysql

# 打开数据库连接
db = pymysql.connect(host='localhost',
                     user='root',
                     password='MySQL08091221',
                     database='hello')

# 使用cursor()方法获取操作游标
cursor = db.cursor()
# SQL 插入语句
sql = "INSERT INTO EMPLOYEE(`书名`, `当前时间`, `已分类书籍总数`) \
       VALUES (%s, %s, %d)" % \
      (a, b, c)

try:
    # 执行sql语句
    cursor.execute(sql)
    # 执行sql语句
    db.commit()
except Error:
    # 发生错误时回滚
    db.rollback()

# 关闭数据库连接
db.close()

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

# 连接MySQL数据库
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='MySQL08091221',
    database='hello'
)
cursor = conn.cursor()

# 遍历识别结果，找到书名
category = "Unknown"
book_name = "Unknown"
for line in result:
    book_name = line[0]
    cursor.execute("SELECT category FROM books WHERE name = %s", (book_name,))
    category = cursor.fetchone()
    if category:
        break

if category:
    category = category[0]
else:
    category = "Unknown"

# 输出结果文件
with open('result.txt', 'w') as f:
    f.write(f"The book '{book_name}' belongs to the category '{category}'")

# 关闭连接
cursor.close()
conn.close()