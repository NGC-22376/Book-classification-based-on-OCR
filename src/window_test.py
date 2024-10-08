import tkinter as tk
import cv2
from PIL import Image, ImageTk
import subprocess
from config import path_msg
import gene_window

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
count = 1  # 画面更新次数的计数器，每5s归零

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


# 存图-识别-显示结果
def main_process(window, frame):
    # 存图
    cv2.imwrite(path_msg['photo_path'], frame)
    # 显示被分类的图片
    img = tk.Label(window)
    img.place(x=800, y=0)
    show_img(frame, img)
    subprocess.run(["python", "./main.py"])
    subprocess.run(["python", "./write_into_mcu.py"])


# 单本入库
def camera():
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

    # 定义获取摄像头画面的局部函数
    def update_pic():
        # 获取每帧
        ret, frame = cap.read()
        if ret:
            show_img(frame, time_frame)
        global count
        count += 1
        if count % 500 == 0:
            main_process(top, frame)
        # 每隔十毫秒执行一次：获取图像并显示，模拟实时显示
        time_frame.after(10, update_pic)

    # 启动画面更新
    update_pic()
    # 启动单片机
    keil_command = [
        path_msg["Keil_path"],  # Keil 编译器路径
        "-b", path_msg["mcu_proj_path"],  # 项目文件路径
        "-o", path_msg["output_log_path"]  # 输出日志文件路径
    ]

    # 调用 Keil 编译器
    try:
        result = subprocess.run(keil_command, check=True, capture_output=True, text=True)
        print("编译成功")
        print("输出日志:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"编译失败，错误码: {e.returncode}")
        print("错误输出:")
        print(e.stderr)

    # 结束后，显示菜单窗口
    init_window.deiconify()


def folder():
    pass


def database():
    bases = tk.Toplevel()
    bases.title("仓库")
    bases.geometry("800x600+400+300")
    book=gene_window.select()
    books=((range(1,len(book[1]))),book)
    #测试用books=((1,2,3),("离散数学","微积分","ewq"),(15,18,2))
    label_1 = tk.Label(bases, text="ID", font=("宋体", 20))
    label_2 = tk.Label(bases, text="Names", font=("宋体", 20))
    label_3 = tk.Label(bases, text="Numbers", font=("宋体", 20))
    listbox_1 = tk.Listbox(bases, font=("宋体", 20),width=15)
    listbox_2 = tk.Listbox(bases, font=("宋体", 20),width=15)
    listbox_3 = tk.Listbox(bases, font=("宋体", 20),width=15)

    label_1.grid(row=0, column=0, padx=10, pady=10, sticky='ew')
    label_2.grid(row=0, column=1, padx=10, pady=10, sticky='ew')
    label_3.grid(row=0, column=2, padx=10, pady=10, sticky='ew')
    listbox_1.grid(row=1, column=0, padx=10, pady=10,sticky='nsew')
    listbox_2.grid(row=1, column=1, padx=10, pady=10,sticky='nsew')
    listbox_3.grid(row=1, column=2, padx=10, pady=10,sticky='nsew')

    for i in range(len(books[0])):
        listbox_1.insert(tk.END, books[0][i])
        listbox_2.insert(tk.END, books[1][i])
        listbox_3.insert(tk.END, books[2][i])

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
