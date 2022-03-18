import pymysql


class MysqlConnection():
    def __init__(self, host, user, passw, port, database, charset="utf8"):
        self.db = pymysql.connect(host=host, user=user, password=passw, port=port,
                                  database=database, charset=charset)
        self.cursor = self.db.cursor()

    # 查
    def query(self, sql):
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        return results

    # 增删改
    def update(self, sql):
        try:
            self.cursor.execute(sql)
            self.db.commit()
            return 1
        except Exception as e:
            print(e)
            self.db.rollback()
            return 0

    # 关闭连接
    def close(self):
        self.cursor.close()
        self.db.close()