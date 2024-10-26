import concurrent.futures
import os.path
import threading
import time
import tkinter as tk
import tkinter.messagebox as messagebox
import cv2
from PIL import Image, ImageTk
import subprocess
from config import path_msg, book_names, book_classes, interval
import classify
import get_data


# 工具函数
def get_info(entry, top):
    """
    批量入库的按钮绑定事件
    :param entry: 需要获取输入的文本框
    """
    info = entry.get()
    if not os.path.exists(info):
        # 如果路径非法，打开会话框提示用户重新输入
        messagebox.showerror(title="ERROR", message="文件夹路径不合法")
    else:
        messagebox.showinfo(title="提示", message="正在分类中，这需要一些时间\n分类结束后将弹窗提醒您")
        img_files = os.listdir(info)
        for img in img_files:
            img = os.path.join(info, img)
            classify.classify(img)
    messagebox.showinfo(title="提示", message="分类完成\n感谢您的使用！")
    top.destroy()


def clock(window, clock_label, remaining_time):
    """
    计时器: 使用Tkinter的after方法来避免阻塞
    :param window: 单本入库的窗口
    :param clock_label: 显示计时提示信息的label
    :param remaining_time: 倒计时信息
    :return:
    """
    if remaining_time > 0:
        clock_label.config(text=f"下一次拍照:{remaining_time}秒后")
        # 每1000ms更新一次倒计时（1秒）
        window.after(1000, clock, window, clock_label, remaining_time - 1)
    else:
        clock_label.config(text="拍照")


def show_img(frame, widget, opt_code):
    """
    显示图像，包括实时帧和被分类图
    :param frame: 输入的图片，帧或图片
    :param widget: 图片显示的组件位置
    :param opt_code:操作码，选择显示实时图片或被分类的图片
    :return:
    """
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


global img_to_classif


def update_pic(cap, widget):
    """
    实时画面显示（左上角窗口）
    :param cap: 摄像头对象
    :param widget: 显示图片的组件
    :return:
    """
    global img_to_classify
    ret, img_to_classify = cap.read()
    if ret:
        show_img(img_to_classify, widget, 0)
    # 每10ms运行一次，模拟实时显示
    widget.after(10, update_pic, cap, widget)


def show_result(window):
    """
    显示分类结果（右下角窗口）
    :param window: 单本入库的窗口
    :return:
    """
    print("结果显示函数")
    result_file = open(path_msg["result_path"], "r")
    top_class, _, sub_class = result_file.read()
    top_class = book_classes[ord(top_class) - ord('0')]
    sub_class = book_names[top_class][ord(sub_class) - ord('0')]
    result_frame = tk.Label(window, text=f"一级类别：{top_class}\n二级类别：{sub_class}", font={'黑体', 20, 'bold'})
    result_frame.place(x=800, y=500, width=int(window_width / 2), height=300)
    result_file.close()


def main_process(window, img):
    """
    识别并显示结果
    :param window: 单本入库的窗口
    :return:
    """
    print("主线函数")
    # 进行分类识别，并将分类结果写入对应文件
    classify.classify(img)
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        future2 = executor.submit(subprocess.run, ["python", r".\mcu_top_class.py"])
        # 等待分类完成后显示分类结果
        future2.result()
        show_result(window)
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
        # 等待烧录完成后继续执行
        time.sleep(5)


def all_threading(sub_window, img_label):
    """
    创建所有后台线程并执行
    :param sub_window: 单本入库的窗口
    :param img_label: 显示被分类图片的组件
    :return:
    """
    print("线程函数已执行")
    global img_to_classify
    # 定时器倒计时显示
    clock_label = tk.Label(sub_window, text="开始计时", font=('黑体', 20, 'bold'))
    clock_label.place(x=400, y=500)
    clock(sub_window, clock_label, interval)  # 使用计时器

    # 使用非阻塞的Tkinter方法显示图片和执行分类
    sub_window.after(interval * 1000, lambda: show_img(img_to_classify, img_label, 1))
    threading.Thread(target=main_process, args=(sub_window, img_to_classify)).start()

    sub_window.after(interval * 1000, lambda: all_threading(sub_window, img_label))


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


def camera():
    """单本入库"""
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
    """批量入库"""
    # 创建新窗口
    top = tk.Toplevel()
    top.title("文件夹-批量入库")
    width = screen_width // 2
    height = screen_height // 5
    pos_x = (screen_width - width) // 2
    pos_y = (screen_height - height) // 2
    top.geometry(f'{width}x{height}+{pos_x}+{pos_y}')

    # 显示提示语句
    tip = tk.Label(top, text="请输入需要分类的图片所在的文件夹路径！", font=('黑体', 20, 'bold'))
    tip.pack(padx=0, pady=0, side='top', anchor='center')
    # 创建输入框，获取用户输入的文件夹
    user_input = tk.Entry(top, font=('宋体', 15))
    user_input.pack(padx=30, pady=20, side='top', anchor='center', ipadx=5, ipady=15, fill='x')

    # 输入完毕后，进行之后的操作，在按钮绑定事件中完成
    confirm_button = tk.Button(top, text="确认", font=('黑体', 15, 'bold'), command=lambda: get_info(user_input, top))
    confirm_button.pack(side='top', anchor='center')


def database():
    bases = tk.Toplevel()
    bases.title("仓库")
    bases.geometry("800x600+400+300")
    num_book = get_data.get_data()
    # num_book=((10,20),(15,25),(5,10),(7,9))
    num_books = {i + 1: list(t) for i, t in enumerate(num_book)}
    # num_books={  1: [10, 20], 2: [15, 25], 3: [5, 10],4:[7,9]}#测试用
    book_numbers = {
        '数理基础类': num_books.get(1, []),
        '历史哲学类': num_books.get(2, []),
        '计算机专业类': num_books.get(3, []),
        '小说文学类': num_books.get(4, [])
    }
    listboxes = []

    for i, (key, books) in enumerate(book_names.items()):
        frame = tk.Frame(bases)
        frame.grid(row=0, column=i, padx=10, pady=10, sticky="nsew")

        bases.columnconfigure(i, weight=1)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)

        label = tk.Label(frame, text=key, font=("黑体", 10))
        label.grid(row=0, column=0, sticky="w")

        listbox = tk.Listbox(frame, font=("黑体", 10))
        listbox.grid(row=1, column=0, sticky="nsew")

        numbers = book_numbers[key]

        total_number = 0
        for book, number in zip(books, numbers):
            listbox.insert(tk.END, f"{book} - {number}")
            total_number += number

        listbox.insert(tk.END, f"Total number: {total_number}")

        # 存储 Listbox 控件
        listboxes.append(listbox)

    # 设置主窗口的权重，使其可以调整大小
    for i in range(len(book_names)):
        bases.columnconfigure(i, weight=1)
    bases.rowconfigure(0, weight=1)

    # 运行主循环
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
