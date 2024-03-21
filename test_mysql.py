from pymysql import Connection


# 获取MySQL数据库的链接对象
conn = Connection(
    host='localhost',     # 主机名
    port=3306,      # 端口，默认为3306
    user='root',    # 账户名
    password=''    # 密码
)


# 打印MySQL数据库软件版本信息
print(conn.get_server_info())

# 关闭链接
conn.close()