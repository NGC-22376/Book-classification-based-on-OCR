import pymysql

# 打开数据库连接
db = pymysql.connect(host='localhost',
                     user='root',
                     password='yufei5312',
                     database='hello')

# 使用cursor()方法获取操作游标
cursor = db.cursor()
# SQL 插入语句
sql = "INSERT INTO EMPLOYEE('微积分', \
       '线性代数', '数字逻辑与电路', '离散数学', '大学英语','已分类书籍总数') \
       VALUES (%d, %d,  %d,  %d,  %d , %d)" % \
      (a, b, c, d, e, f)
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
