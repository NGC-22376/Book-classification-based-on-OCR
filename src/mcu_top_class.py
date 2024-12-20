from config import path_msg, out_msg

# 打开目标文件
res_file = open(path_msg['result_path'], 'r')
pre_file = open(path_msg['mcu_pre_path'], 'r', encoding='utf-8')
isp_file = open(path_msg['isp_path'], 'w')
target_line = 9

# 读取结果文件和应该写入mcu.c的文件，并根据读到的result对后者进行修改后写入
result, _, _ = res_file.read()
pretext = pre_file.readlines()
pretext[target_line] = 'unsigned char timer1=' + result + ';' + '\n'

# 写入mcu.c
for i in range(0, len(pretext)):
    isp_file.write(pretext[i])

out_msg("一级分类写入单片机")

# 关闭文件
res_file.close()
pre_file.close()
isp_file.close()
