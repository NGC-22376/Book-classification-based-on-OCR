# 数据库配置相关信息
sql_msg = {
    'my_host': 'localhost',
    'my_root': 'root',
    'my_password': 'MySQL08091221',
    'book_database': 'hello'
}

# 路径相关信息
path_msg = {
    "photo_path": r'..\output\book_photo.jpg',
    "result_path": r"..\output\result.txt",
    "output_log_path": r'..\output',
    "mcu_pre_path": r"..\output\CV.txt",
    "isp_path": r".\mcu.c",
    "background_path": r"..\output\init_background.png",
    "keil_path":r"C:\Keil_v5\UV4\UV4.exe",
    "mcu_proj_path":r"C:\Users\30744\Desktop\CodeFiles\MCU_C51\MCU_C51.uvproj",
    "mcu_obj_path":r"C:\Users\30744\Desktop\CodeFiles\MCU_C51\Objects"
}

keil_command = [
            path_msg["keil_path"],  # Keil 编译器路径
            "-b", path_msg["mcu_proj_path"],  # 项目文件路径
            "-o", path_msg["output_log_path"]  # 输出日志文件路径
        ]

book_classes = ['数理基础类', '历史哲学类', '计算机专业类', '小说文学类']

book_names = {
    '数理基础类': ['微积分', '线性代数'],
    '历史哲学类': ['论语', '中国近现代史纲要'],
    '计算机专业类': ['计算机组成与系统结构', '离散数学'],
    '小说文学类': ['哈利·波特', '朝花夕拾']
}

# 拍照间隔(s)
interval = 20
