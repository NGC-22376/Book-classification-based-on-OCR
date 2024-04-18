import tkinter as tk
import pymysql

window = tk.Tk()
window.title('图书分类结果')
window.geometry('800x640')
v = tk.StringVar()

a=0
b=0
c=0
d=0
# 打开数据库连接
db = pymysql.connect(host='localhost',
                     user='root',
                     password='yufei5312',
                     database='hello')

# 使用cursor()方法获取操作游标
cursor = db.cursor()


sql1 = "SELECT * FROM `books` WHERE `name` = '微积分'"
sql2 = "SELECT * FROM `books` WHERE `name` = '线性代数'"
sql3 = "SELECT * FROM `books` WHERE `name` = '数字逻辑概论'"
sql4 = "SELECT * FROM `books` WHERE `name` = '离散数学'"
sql5 = "SELECT `name`,SUM(`count`)\
FROM `books`\
GROUP BY `name`;"
try:
    # 执行sql语句
    cursor.execute(sql1)
    # 获取记录列表
    result1 = cursor.fetchone()
    if not result1:
        insert_sql1 = "INSERT INTO `books` VALUES ('%s','0','0')" % "微积分"
        cursor.execute(insert_sql1)
        cursor.commit()

except Exception:
    print("Error:unable to insert data")

try:
    # 执行sql语句
    cursor.execute(sql2)
    # 获取记录列表
    result2 = cursor.fetchone()
    if not result2:
        insert_sql2 = "INSERT INTO `books` VALUES ('%s','0','0')" % "线性代数"
        cursor.execute(insert_sql2)
        cursor.commit()

except Exception:
    print("Error:unable to insert data")

try:
    # 执行sql语句
    cursor.execute(sql3)
    # 获取记录列表
    result3 = cursor.fetchone()
    if not result3:
        insert_sql3 = "INSERT INTO `books` VALUES ('%s','0','0')" % "数字逻辑概论"
        cursor.execute(insert_sql3)
        cursor.commit()

except Exception:
    print("Error:unable to insert data")

try:
    # 执行sql语句
    cursor.execute(sql4)
    # 获取记录列表
    result4 = cursor.fetchone()
    if not result4:
        insert_sql4 = "INSERT INTO `books` VALUES ('%s','0','0')" % "离散数学"
        cursor.execute(insert_sql4)
        cursor.commit()

except Exception:
    print("Error:unable to insert data")

try:
    # 执行sql语句
    cursor.execute(sql5)
    # 获取所有记录列表
    results = cursor.fetchall()
    na = results[0][0]
    nb = results[1][0]
    nc = results[2][0]
    nd = results[3][0]
    a = results[0][1]
    b = results[1][1]
    c = results[2][1]
    d = results[3][1]
except Exception:
    print("Error:unable to fetch data")

e = a+b+c+d
label = tk.Label(window, textvariable=v,
                 width=1000, height=1000,  # width为标签的宽，height为高
                 font=("黑体", 50),
                 wraplength=600,
                 justify="left")
v.set("%s：%d\n"
      "%s：%d\n"
      "%s：%d\n"
      "%s：%d\n"
      "共计：%d" % (na, a, nb, b, nc, c, nd, d, e))
label.pack()
window.mainloop()
# 关闭数据库
cursor.close()
db.close()
