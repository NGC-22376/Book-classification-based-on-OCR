# 打开目标文件
res_file = open(r"C:\Users\30744\Desktop\ComputerVision\result.txt", 'r')
pre_file = open(r"C:\Users\30744\Desktop\ComputerVision\CV.txt", 'r')
isp_file = open(r"C:\Users\30744\Desktop\ComputerVision\mcu.c", 'w')
target_line = 8

# 读取结果文件和应该写入mcu.c的文件，并根据读到的result对后者进行修改后写入
result = res_file.read(1)
pretext = pre_file.readlines()
pretext[target_line] = 'unsigned char timer1=' + result + ';' + '\n'

# 写入mcu.c
for i in range(0, len(pretext)):
    isp_file.write(pretext[i])