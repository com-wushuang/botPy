import pymysql


def list_all():
    # 打开数据库连接
    db = pymysql.connect(host='localhost', user='root',
                         password='123456', db='TGBOT', port=3306, charset='utf8')

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 查询语句
    sql = "SELECT * FROM advertisements"

    results = []
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        rows = cursor.fetchall()
        for row in rows:
            item = {}
            item["id"] = row[0]
            item["text"] = row[1]
            item["key"] = row[2]
            item["expire"] = row[3]
            item["interval"] = row[4]
            item["profile"] =item["id"][:10]
            results.append(item)

    except:
        print("Error: unable to fetch data")
        db.close()
        return []

    # 关闭数据库连接
    db.close()
    return results
