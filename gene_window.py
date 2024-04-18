import tkinter as tk
import pymysql

window = tk.Tk()
window.title('图书分类结果')
window.geometry('640x640')
v = tk.StringVar()

a=0
b=0
c=0
d=0
nc="数字逻辑概论"
nd="离散数学"
# 打开数据库连接
db = pymysql.connect(host='localhost',
                     user='root',
                     password='yufei5312',
                     database='hello')

# 使用cursor()方法获取操作游标
cursor = db.cursor()

sql = "SELECT `name`,COUNT(*)\
FROM `books`\
GROUP BY `name`;"

try:
    # 执行sql语句
    cursor.execute(sql)
    # 获取所有记录列表
    results = cursor.fetchall()
    a = results[0][1]
    b = results[1][1]
    c = results[2][1]
    d = results[3][1]
except Exception:
    print("Error:unable to fetch data")

print(results)
e = a+b
label = tk.Label(window, textvariable=v,
                 width=300, height=300,  # width为标签的宽，height为高
                 font=30,
                 wraplength=600,  # 设置多少单位后开始换行
                 anchor='w',
                 justify='left')  # 设置文本在标签中显示的位置
v.set("%s：%d；\n"
      "%s：%d；\n"
      "%s：%d；\n"
      "%s：%d；\n"
      "共计：%d" % (na, a, nb, b, nc, c, nd, d, e))
label.pack()
window.mainloop()
# 关闭数据库
cursor.close()
db.close()
