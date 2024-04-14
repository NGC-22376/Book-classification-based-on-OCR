import tkinter as tk
import pymysql

window = tk.Tk()
window.title('图书分类结果')
window.geometry('640x640')
v = tk.StringVar()

# 打开数据库连接
db = pymysql.connect(host='localhost',
                     user='root',
                     password='yufei5312',
                     database='hello')

# 使用cursor()方法获取操作游标
cursor = db.cursor()

sql = "SELECT name,COUNT(*)\
FROM books\
GROUP BY name;"

try:
    # 执行sql语句
    cursor.execute(sql)
    # 获取所有记录列表
    results = cursor.fetchall()
    for row in results:
        a = row[0][0]
        b = row[0][1]
        c = row[0][2]
        d = row[0][3]
except Exception:
    v.set("Error:unable to fetch data")

e = a+b+c+d
label = tk.Label(window, textvariable=v,
                 width=300, height=300,  # width为标签的宽，height为高
                 font=30,
                 wraplength=600,  # 设置多少单位后开始换行
                 anchor='w',
                 justify='left')  # 设置文本在标签中显示的位置
v.set("微积分：%d；\n"
      "线性代数：%d；\n"
      "数字逻辑与电路：%d；\n"
      "离散数学：%d；\n"
      "共计：%d" % (a, b, c, d, e))
label.pack()
window.mainloop()
# 关闭数据库
cursor.close()
db.close()
