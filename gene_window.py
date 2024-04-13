import tkinter as tk
import pymysql

window = tk.Tk()
window.title('图书分类结果')
window.geometry('640x640')

# 打开数据库连接
db = pymysql.connect(host='localhost',
                     user='root',
                     password='MySQL08091221',
                     database='hello')

# 使用cursor()方法获取操作游标
cursor = db.cursor()

sql = "SELECT *\
FROM books\
GROUP BY name;"

cursor.execute(sql)

a = 1
b = 2
c = 3
d = 4
v = tk.StringVar()
label = tk.Label(window, textvariable=v,
                 width=300, height=300,  # width为标签的宽，height为高
                 font=30,
                 wraplength=600,  # 设置多少单位后开始换行
                 anchor='w',
                 justify='left')  # 设置文本在标签中显示的位置
v.set("微积分：%d；\n"
      "线性代数：%d；\n"
      "数字逻辑与电路：%d；\n"
      "离散数学：%d" % (a, b, c, d))
label.pack()
window.mainloop()
cursor.close()
db.close()
