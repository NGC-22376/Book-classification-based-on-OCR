import tkinter as tk
import subprocess
def prepare():
    selection = var.get()
    if selection == 1:
        camera()
    elif selection == 2:
        takeall()
def camera():
    label.config(text="123")
    subprocess.run(["python", ".\main.py"])
    subprocess.run(["python", ".\write_into_mcu.py"])
def takeall():
    label.config(text="321")

window = tk.Tk()
window.title('图书分类管理系统')
window.geometry('1000x800')

# 标题标签
var_title = tk.StringVar()
title_label = tk.Label(window, text='图书分类管理系统', bg='lightblue', font=('Arial', 35), width=65, height=6)
title_label.pack()

# 创建一个 Frame 用来放置单选按钮
left_frame = tk.Frame(window)
left_frame.pack(side=tk.LEFT, padx=50,pady=0)
# 创建一个变量来存储单选按钮的状态
var = tk.IntVar()
# 创建单选按钮
rb1 = tk.Radiobutton(left_frame, text="摄像头检测", variable=var, value=1,font=('宋体', 30))
rb2 = tk.Radiobutton(left_frame, text="文件夹批量检测", variable=var, value=2,font=('宋体', 30))

# 将单选按钮放置到左侧的 Frame 中
rb1.pack(anchor=tk.W)
rb2.pack(anchor=tk.W)

confirm_button = tk.Button(window, text="确定", command=prepare, font=('Arial', 20),
                           bg='lightgreen', fg='black', width=10, height=2)
confirm_button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

label = tk.Label(window)
label.pack()

window.mainloop()