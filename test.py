import tkinter as tk


def center_window(root, width, height):
    # 获取屏幕的宽度和高度
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # 计算窗口左上角的位置，使窗口居中
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    # 设置窗口的大小和位置
    root.geometry(f'{width}x{height}+{x}+{y}')


# 创建主窗口
root = tk.Tk()

# 设置窗口大小
window_width = 400
window_height = 300

# 调用居中函数
center_window(root, window_width, window_height)

# 进入主循环
root.mainloop()
