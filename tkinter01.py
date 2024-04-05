import tkinter as tk

window = tk.Tk()
window.title('Label的使用')
window.geometry('400x400')

label = tk.Label(window, text='test',
                 bg='black', fg='white',  # bg为背景色，fg为前景色
                 width=30, height=3,  # width为标签的宽，height为高
wraplength = 150,  # 设置多少单位后开始换行
anchor = 'w')  # 设置文本在标签中显示的位置
label.pack()
window.mainloop()
