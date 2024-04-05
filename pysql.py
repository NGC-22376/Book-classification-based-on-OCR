import pymysql

# 打开数据库连接
db = pymysql.connect(host='localhost',
                     user='root',
                     password='yufei5312',
                     database='hello')

# 使用cursor()方法获取操作游标
cursor = db.cursor()
# SQL 插入语句
sql = "INSERT INTO EMPLOYEE('书名', \
       '当前时间', '已分类书籍总数') \
       VALUES (%s, %s,  %d)" % \
      (a, b, c)
try:
    # 执行sql语句
    cursor.execute(sql)
    # 执行sql语句
    db.commit()
except Error:
    # 发生错误时回滚
    db.rollback()

# 关闭数据库连接
db.close()
