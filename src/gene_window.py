import threading
import time
import tkinter as tk
import cv2
from PIL import Image, ImageTk
import subprocess
from config import path_msg
import get_data

# 创建窗口并使其居中显示
init_window = tk.Tk()
init_window.title('图书分类管理系统')

screen_width = init_window.winfo_screenwidth()
screen_height = init_window.winfo_screenheight()
window_width = 900
window_height = 700
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2 - 20  # 考虑到任务栏，额外-20后能使窗口位于视觉正中心

init_window.geometry(f'{window_width}x{window_height}+{x}+{y}')

# 创建带背景的标题
background_img = ImageTk.PhotoImage(file=path_msg["background_path"])
title_label = tk.Label(init_window, text='图书分类管理系统', font=('黑体', 50, 'bold'), fg='white',
                       image=background_img, compound='center')
title_label.place(x=0, y=0, width=window_width, height=int(window_height * 0.8))

# 创建用户选项：单本入库、批量入库、后台管理
# 定义对应的按钮行为

# 图片的窗口显示
def show_img(frame, widge):
    # 转换显示方向，转换BGR->RGB
    frame = cv2.flip(frame, 1)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # 显示到窗口
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    widge.image = imgtk
    widge.configure(image=imgtk)


# 存图-识别-显示结果（放在后台线程执行）
def main_process_in_thread(window, frame, result_label):
    # 在后台线程执行耗时任务
    def process():
        # 存图
        cv2.imwrite(path_msg['photo_path'], frame)
        # 调用分类脚本和写入 MCU 脚本
        subprocess.run(["python", "./classify.py"])
        subprocess.run(["python", "./write_into_mcu.py"])
        # 分类结果更新，需要在主线程中更新 GUI
        window.after(0, show_img, frame, result_label)  # 主线程更新右侧图片

    # 启动后台线程
    threading.Thread(target=process).start()


# 定时调用 main_process 的函数，确保每次使用最新的帧
def periodic_call(window, cap, result_label):
    ret, frame = cap.read()  # 读取最新的摄像头帧
    if ret:
        main_process_in_thread(window, frame, result_label)  # 在后台线程中调用 main_process
    # 每隔 5 秒再次调用该函数
    window.after(5000, periodic_call, window, cap, result_label)


# 单本入库
def camera():
    global timer
    # 隐藏菜单窗口
    init_window.withdraw()

    # 创建新窗口
    top = tk.Toplevel()
    top.title("摄像头-逐本入库")
    top.geometry(f'{screen_width}x{screen_height}+{0}+{0}')

    # 获取摄像头，并设置其分辨率为适应窗口的尺寸
    cap = cv2.VideoCapture(0)

    # 创建组件，包括摄像头画面
    time_frame = tk.Label(top)
    time_frame.place(x=0, y=0)

    # 右侧用于显示分类结果的 Label
    result_label = tk.Label(top)
    result_label.place(x=800, y=0)

    # 定义获取摄像头画面的局部函数
    def update_pic():
        # 获取每帧
        ret, frame = cap.read()
        if ret:
            show_img(frame, time_frame)  # 左侧显示实时图像
        # 每隔十毫秒执行一次：获取图像并显示，模拟实时显示
        time_frame.after(10, update_pic)

    # 启动画面更新
    update_pic()

    # 定时任务：每隔 5 秒调用一次 main_process，确保使用最新的帧
    periodic_call(top, cap, result_label)

    # 窗口关闭时停止定时任务
    def on_close():
        global timer
        if timer is not None:
            top.after_cancel(timer)  # 取消定时任务
        cap.release()
        top.destroy()
        init_window.deiconify()

    # 绑定窗口关闭事件
    top.protocol("top", on_close)


def folder():
    pass


def database():
    bases = tk.Toplevel()
    bases.title("仓库")
    bases.geometry("800x600+400+300")
    books = get_data.get_data()
    # books=(1,"ewqewq","二九五情况呢")
    listbox = tk.Listbox(bases, font=("宋体", 20))
    listbox.pack(pady=10)

    for item in books:
        listbox.insert(tk.END, item)

    bases.mainloop()


# 创建Frame存放选择的按钮
buttons = tk.Frame(init_window)
buttons.place(x=0, y=int(window_height * 0.8))
# 创建按钮，规定为从左到右排列
button1 = tk.Button(buttons, text="单本入库", font=("黑体", 30), command=camera)
button2 = tk.Button(buttons, text="批量入库", font=("黑体", 30), command=folder)
button3 = tk.Button(buttons, text="查看仓库", font=("黑体", 30), command=database)
button1.pack(side=tk.LEFT, padx=window_width // 20, pady=int(window_height * 0.04))
button2.pack(side=tk.LEFT, padx=window_width // 20, pady=int(window_height * 0.04))
button3.pack(side=tk.LEFT, padx=window_width // 20, pady=int(window_height * 0.04))

# 启动循环
init_window.mainloop()
