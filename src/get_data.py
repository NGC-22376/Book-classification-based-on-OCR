from config import sql_msg
import pymysql


def get_data():
    # 打开数据库连接

    db = pymysql.connect(host=sql_msg['my_host'],
                         user=sql_msg['my_root'],
                         password=sql_msg['my_password'],
                         database=sql_msg['book_database'])

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    sql1 = "SELECT * FROM `books_count` WHERE `name` = '微积分'"
    sql2 = "SELECT * FROM `books_count` WHERE `name` = '线性代数'"
    sql3 = "SELECT * FROM `books_count` WHERE `name` = '论语'"
    sql4 = "SELECT * FROM `books_count` WHERE `name` = '中国近代史纲要'"
    sql5 = "SELECT * FROM `books_count` WHERE `name` = '计算机组成原理与结构'"
    sql6 = "SELECT * FROM `books_count` WHERE `name` = '离散数学'"
    sql7 = "SELECT * FROM `books_count` WHERE `name` = '哈利·波特'"
    sql8 = "SELECT * FROM `books_count` WHERE `name` = '朝花夕拾'"
    sql9 = ("SELECT SUM(`count`)\
    FROM `books_count`\
    GROUP BY `name`\
    ORDER BY `count_id`;")
    sql10 = ("SELECT SUM(`count`)\
    FROM `books_count`\
    GROUP BY `id_2`\
    ORDER BY `count_id`;")
    try:
        # 执行sql语句
        cursor.execute(sql1)
        # 获取记录列表
        result1 = cursor.fetchone()
        if not result1:
            insert_sql1 = "INSERT INTO `books` VALUES ('2','0','0','%s','1')" % "微积分"
            cursor.execute(insert_sql1)
            cursor.commit()

    except Exception:
        print("Error:unable to insert data")

    try:
        # 执行sql语句
        cursor.execute(sql2)
        # 获取记录列表
        result2 = cursor.fetchone()
        if not result2:
            insert_sql2 = "INSERT INTO `books` VALUES ('3','0','0','%s','1')" % "线性代数"
            cursor.execute(insert_sql2)
            cursor.commit()

    except Exception:
        print("Error:unable to insert data")

    try:
        # 执行sql语句
        cursor.execute(sql3)
        # 获取记录列表
        result3 = cursor.fetchone()
        if not result3:
            insert_sql3 = "INSERT INTO `books` VALUES ('5','0','0','%s','4')" % "论语"
            cursor.execute(insert_sql3)
            cursor.commit()

    except Exception:
        print("Error:unable to insert data")

    try:
        # 执行sql语句
        cursor.execute(sql4)
        # 获取记录列表
        result4 = cursor.fetchone()
        if not result4:
            insert_sql4 = "INSERT INTO `books` VALUES ('6','0','0','%s','4')" % "中国近代史纲要"
            cursor.execute(insert_sql4)
            cursor.commit()

    except Exception:
        print("Error:unable to insert data")

    try:
        # 执行sql语句
        cursor.execute(sql5)
        # 获取记录列表
        result5 = cursor.fetchone()
        if not result5:
            insert_sql5 = "INSERT INTO `books` VALUES ('8','0','0','%s','7')" % "计算机组成原理与结构"
            cursor.execute(insert_sql4)
            cursor.commit()

    except Exception:
        print("Error:unable to insert data")

    try:
        # 执行sql语句
        cursor.execute(sql6)
        # 获取记录列表
        result6 = cursor.fetchone()
        if not result6:
            insert_sql6 = "INSERT INTO `books` VALUES ('9','0','0','%s','7')" % "离散数学"
            cursor.execute(insert_sql4)
            cursor.commit()

    except Exception:
        print("Error:unable to insert data")

    try:
        # 执行sql语句
        cursor.execute(sql7)
        # 获取记录列表
        result7 = cursor.fetchone()
        if not result7:
            insert_sql7 = "INSERT INTO `books` VALUES ('11','0','0','%s','10')" % "哈利·波特"
            cursor.execute(insert_sql4)
            cursor.commit()

    except Exception:
        print("Error:unable to insert data")

    try:
        # 执行sql语句
        cursor.execute(sql8)
        # 获取记录列表
        result8 = cursor.fetchone()
        if not result8:
            insert_sql4 = "INSERT INTO `books` VALUES ('12','0','0','%s','10')" % "朝花夕拾"
            cursor.execute(insert_sql4)
            cursor.commit()

    except Exception:
        print("Error:unable to insert data")

    try:
        # 执行sql语句
        cursor.execute(sql10)
        # 获取所有记录列表
        results_1 = cursor.fetchall()
    except Exception:
        print("Error:unable to fetch data")

    try:
        # 执行sql语句
        cursor.execute(sql9)
        # 获取所有记录列表
        results_2 = cursor.fetchall()
    except Exception:
        print("Error:unable to fetch data")

    # 关闭数据库
    cursor.close()
    db.close()
    results_3 = results_1 + results_2
    return results_3
