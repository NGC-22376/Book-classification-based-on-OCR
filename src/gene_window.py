import threading
import tkinter as tk
import cv2
import numpy
from PIL import Image, ImageTk
import subprocess

from config import path_msg, book_names, book_classes
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


# 显示图像
def show_img(frame, widget):
    if isinstance(frame, numpy.ndarray):
        # 将OpenCV的BGR帧转换为RGB格式
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cv2image)
    else:
        img = Image.open(frame)
    # 转换为Tkinter的PhotoImage对象
    imgtk = ImageTk.PhotoImage(image=img)
    widget.config(image=imgtk)
    widget.image = imgtk  # 防止图片被垃圾回收


# 显示分类结果
def show_result(window):
    result_file = open(path_msg["result_path"], "r")
    top_class, _, sub_class = result_file.read()
    top_class = book_classes[ord(top_class) - ord('0')]
    sub_class = book_names[top_class][ord(sub_class) - ord('0')]
    result_frame = tk.Label(window, text=f"一级类别：{top_class}\n二级类别：{sub_class}", font={'黑体', 20, 'bold'})
    result_frame.place(x=800, y=500, width=int(window_width / 2), height=300)
    result_file.close()


# 存图、识别并显示结果
def main_process_in_thread(window, frame, widget):
    def process():
        cv2.imwrite(path_msg['photo_path'], frame)
        show_img(path_msg["photo_path"], widget)
        subprocess.run(["python", r".\classify.py"])
        subprocess.run(["python", r".\mcu_top_class.py"])
        subprocess.run(["python", r".\mcu_sub_class.py"])
        show_result(window)

    threading.Thread(target=process).start()


# 每5秒调用main_process
def periodic_call(window, cap, widget, running_flag):
    if not running_flag["run"]:
        return  # 如果标志为False，停止调用
    ret, frame = cap.read()
    if ret:
        main_process_in_thread(window, frame, widget)
    window.after(5000, periodic_call, window, cap, widget, running_flag)


# 单本入库
def camera():
    # 隐藏菜单窗口
    init_window.withdraw()
    # 创建新窗口
    top = tk.Toplevel()
    top.title("摄像头-逐本入库")
    top.geometry(f'{screen_width}x{screen_height}+{0}+{0}')

    # 获取摄像头
    cap = cv2.VideoCapture(0)
    time_frame = tk.Label(top)
    time_frame.place(x=0, y=0)
    result_label = tk.Label(top)
    result_label.place(x=800, y=0)

    # 运行状态的标志，用于控制定时任务
    running_flag = {"run": True}

    # 更新图像显示
    def update_pic():
        ret, frame = cap.read()
        if ret:
            show_img(frame, time_frame)
        time_frame.after(10, update_pic)

    # 启动画面更新
    update_pic()

    # 定时任务：每隔5秒调用
    periodic_call(top, cap, result_label, running_flag)

    # 关闭窗口时，释放摄像头资源并停止定时任务
    def on_closing():
        running_flag["run"] = False  # 设置标志为False以停止任务
        cap.release()
        top.destroy()
        init_window.deiconify()

    top.protocol("WM_DELETE_WINDOW", on_closing)


def folder():
    pass


def database():
    bases = tk.Toplevel()
    bases.title("仓库")
    bases.geometry("800x600+400+300")
    books = get_data.get_data()
    listbox = tk.Listbox(bases, font=("宋体", 20))
    listbox.pack(pady=10)

    for item in books:
        listbox.insert(tk.END, item)

    bases.mainloop()


# 创建按钮
buttons = tk.Frame(init_window)
buttons.place(x=0, y=int(window_height * 0.8))
button1 = tk.Button(buttons, text="单本入库", font=("黑体", 30), command=camera)
button2 = tk.Button(buttons, text="批量入库", font=("黑体", 30), command=folder)
button3 = tk.Button(buttons, text="查看仓库", font=("黑体", 30), command=database)
button1.pack(side=tk.LEFT, padx=window_width // 20, pady=int(window_height * 0.04))
button2.pack(side=tk.LEFT, padx=window_width // 20, pady=int(window_height * 0.04))
button3.pack(side=tk.LEFT, padx=window_width // 20, pady=int(window_height * 0.04))

init_window.mainloop()
