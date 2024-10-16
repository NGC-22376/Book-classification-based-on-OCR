import concurrent.futures
import threading
import time
import tkinter as tk
import cv2
from PIL import Image, ImageTk
import subprocess

from config import path_msg, book_names, book_classes, interval
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


# 计时器: 使用Tkinter的after方法来避免阻塞
def clock(window, clock_label, remaining_time):
    if remaining_time > 0:
        clock_label.config(text=f"下一次拍照:{remaining_time}秒后")
        # 每1000ms更新一次倒计时（1秒）
        window.after(1000, clock, window, clock_label, remaining_time - 1)
    else:
        clock_label.config(text="拍照")


# 显示图像
def show_img(frame, widget, opt_code):
    # 实时帧显示
    if opt_code == 0:
        # 将OpenCV的BGR帧转换为RGB格式
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cv2image)
    # 被分类的图片保存与显示
    else:
        cv2.imwrite(path_msg['photo_path'], frame)
        img = Image.open(path_msg['photo_path'])
    # 转换为Tkinter的PhotoImage对象
    imgtk = ImageTk.PhotoImage(image=img)
    widget.config(image=imgtk)
    widget.image = imgtk  # 防止图片被垃圾回收


# 实时画面显示（左上角窗口）
global img_to_classify


def update_pic(cap, widget):
    global img_to_classify
    ret, img_to_classify = cap.read()
    if ret:
        show_img(img_to_classify, widget, 0)
    # 每10ms运行一次，模拟实时显示
    widget.after(10, update_pic, cap, widget)


# 显示分类结果（右下角窗口）
def show_result(window):
    print("结果显示函数")
    result_file = open(path_msg["result_path"], "r")
    top_class, _, sub_class = result_file.read()
    top_class = book_classes[ord(top_class) - ord('0')]
    sub_class = book_names[top_class][ord(sub_class) - ord('0')]
    result_frame = tk.Label(window, text=f"一级类别：{top_class}\n二级类别：{sub_class}", font={'黑体', 20, 'bold'})
    result_frame.place(x=800, y=500, width=int(window_width / 2), height=300)
    result_file.close()


# 识别并显示结果
def main_process(window):
    print("主线函数")
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        # 进行分类识别，并将分类结果写入对应文件
        executor.submit(subprocess.run, ["python", r".\classify.py"])
        executor.submit(subprocess.run, ["python", r".\mcu_top_class.py"])

        # 等待写入完成再执行操作(一级分类)
        time.sleep(2)
        print("单片机启动-即将进行一级分类")
        keil_command = [
            path_msg["keil_path"],  # Keil 编译器路径
            "-b", path_msg["mcu_proj_path"],  # 项目文件路径
            "-o", path_msg["output_log_path"]  # 输出日志文件路径
        ]
        # 调用 Keil 编译器
        try:
            result = subprocess.run(keil_command, check=True, capture_output=True, text=True, shell=True)
            print("编译成功")
            print("输出日志:")
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"编译失败，错误码: {e.returncode}")
            print("错误输出:")
            print(e.stderr)
        # 一级分类完成-等待烧录完成后继续执行
        time.sleep(5)

        # 二级分类开始
        executor.submit(subprocess.run, ["python", r".\mcu_sub_class.py"])
        # 等待二级分类写入完成再执行操作
        time.sleep(2)
        print("单片机启动-即将进行二级分类")
        # 调用 Keil 编译器
        try:
            result = subprocess.run(keil_command, check=True, capture_output=True, text=True, shell=True)
            print("编译成功")
            print("输出日志:")
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"编译失败，错误码: {e.returncode}")
            print("错误输出:")
            print(e.stderr)
        # 在窗口显示本次分类结果
        show_result(window)
        # 等待烧录完成后继续执行
        time.sleep(5)


# 创建所有后台线程并执行
def all_threading(sub_window, img_label):
    print("线程函数已执行")
    global img_to_classify
    # 定时器倒计时显示
    clock_label = tk.Label(sub_window, text="开始计时", font=('黑体', 20, 'bold'))
    clock_label.place(x=400, y=500)
    clock(sub_window, clock_label, interval)  # 使用计时器

    # 使用非阻塞的Tkinter方法显示图片和执行分类
    sub_window.after(interval * 1000, lambda: show_img(img_to_classify, img_label, 1))
    threading.Thread(target=main_process, args=(sub_window,)).start()

    sub_window.after(interval * 1000, lambda: all_threading(sub_window, img_label))


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

    # 创建放置实时画面和被分类图片的组件
    img_update_label = tk.Label(top)
    img_update_label.place(x=0, y=0)
    img_tobe_classify_label = tk.Label(top)
    img_tobe_classify_label.place(x=800, y=0)

    # 实时显示图像
    update_pic(cap, img_update_label)

    # 运行主线程
    all_threading(top, img_tobe_classify_label)

    # 关闭窗口时，释放摄像头资源
    def on_closing():
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
    book = get_data.get_data()
    books = ((range(1, len(book[1]))), book)
    # 测试用books=((1,2,3),("离散数学","微积分","ewq"),(15,18,2))
    label_1 = tk.Label(bases, text="ID", font=("宋体", 20))
    label_2 = tk.Label(bases, text="Names", font=("宋体", 20))
    label_3 = tk.Label(bases, text="Numbers", font=("宋体", 20))
    listbox_1 = tk.Listbox(bases, font=("宋体", 20), width=15)
    listbox_2 = tk.Listbox(bases, font=("宋体", 20), width=15)
    listbox_3 = tk.Listbox(bases, font=("宋体", 20), width=15)

    label_1.grid(row=0, column=0, padx=10, pady=10, sticky='ew')
    label_2.grid(row=0, column=1, padx=10, pady=10, sticky='ew')
    label_3.grid(row=0, column=2, padx=10, pady=10, sticky='ew')
    listbox_1.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')
    listbox_2.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')
    listbox_3.grid(row=1, column=2, padx=10, pady=10, sticky='nsew')

    for i in range(len(books[0])):
        listbox_1.insert(tk.END, books[0][i])
        listbox_2.insert(tk.END, books[1][i])
        listbox_3.insert(tk.END, books[2][i])

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
