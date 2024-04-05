import tkinter as tk

window = tk.Tk()
window.title('图书分类结果')
window.geometry('640x640')

v = tk.StringVar()
label = tk.Label(window, textvariable=v,
                 width=30, height=3,  # width为标签的宽，height为高
                 font=24,
                 wraplength=150,  # 设置多少单位后开始换行
                 anchor='w')  # 设置文本在标签中显示的位置
v.set("微积分：%d；线性代数：%d；数字逻辑与电路：%d；大学英语：%d；离散数学：%d" % (a, b, c, d, e))
label.pack()
window.mainloop()
