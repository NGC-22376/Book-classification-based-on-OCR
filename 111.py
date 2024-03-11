# 创建一个元祖，至少包含五个整数
# 将这个元组转换为列表
# 将列表中的第一个元素修改为其相反数
# 打印修改后的列表
my_turple = (1, 2, 3, 4, 5)
my_list = list(my_turple)
my_list[0] = -my_list[0]
print(type(my_list))
print(f"修改后的列表为{my_list}")

# 创建一个列表，包含至少五个字符串，每个字符串是一个水果名称，如apple
# 将列表中的第三个水果名称改为“橙子”
# 使用列表切片操作，打印列表中的前三个元素
my_list = ['apple', 'pear', 'banana', 'orange', 'grapes']
my_list[2] = "橙子"
print(my_list[0:3])

# 定义一个字典student_score存储至少三名学生的姓名和成绩
# 从字典中读取一位给定姓名学生的成绩，并打印输出
student_score = {"张三": "99", "李四": "100", "王五": "80", "赵凯": "88"}
print(student_score['李四'])
