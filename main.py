import cv2
from pymysql import Error
import paddleocr
import pymysql
import time

# 创建列表包括书名
book_names = ['微积分','线性代数','数字逻辑与电路','离散数学']

# 初始化PaddleOCR
ocr = paddleocr.OCR()

# 打开摄像头
cap = cv2.VideoCapture(0)

# 设置无限循环
while Ture:
    # 读取图像
    ret, frame = cap.read()

    # 保存图像
    cv2.imwrite('book_photo.jpg', frame)

    # 进行文字识别
    result = ocr.ocr('book_photo.jpg', cls=True)

    # 遍历result列表 判断列表里的书名是否在OCR识别里
    for line in result:
        for word in line:
            text = word[1][0]
            for book_name in book_names:
                if book_name in text:
                    n = book_name
                    break

    # 获取当前时间
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

    # 关闭数据库连接
    db.close()

    #  转换为数字
    if n == '微积分':
        n = 0
    elif n == '线性代数':
        n = 1
    elif n == '数字逻辑与电路':
        n = 2
    else:
        n = 3

    # 输出结果文件
    with open('result.txt', 'w') as f:
        f.write(f"The book '{n}' belongs to the category '{category}'")

    # 按'q'键退出程序
    if cv2.waitKey(1) == ord('q'):
        break

# 释放摄像头资源
cap.release()
