import pandas as pd
import os
import openpyxl
from db_connection_util import MysqlConnection
from config_utils import Configure
from tqdm import tqdm


class ExportMysqlTableStructureInfoToExcel():
    def __init__(self):
        conf = Configure()
        self.__host, self.__port, self.__username, self.__password, self.__charset, self.db_names = conf.get_db_config()
        self.__excel_title, self.__save_dir = conf.get_excel_title()

    def __connect_to_mysql(self, database):
        connect = MysqlConnection(self.__host,
                                  self.__username,
                                  self.__password,
                                  self.__port, database,
                                  self.__charset)
        return connect

    def __struct_of_table_generator(self, con, db_name):
        tb_list = self.__get_all_tables(con)
        for index, tb_name in enumerate(tb_list):
            sql = "SELECT COLUMN_NAME,COLUMN_TYPE,COLUMN_KEY,IS_NULLABLE, COLUMN_COMMENT " \
              "FROM information_schema.`COLUMNS` WHERE TABLE_SCHEMA='{}' AND TABLE_NAME='{}'".format(db_name, tb_name)
            res = con.query(sql)
            struct_list = []
            for item in res:
                column_name, column_type, column_key, is_nullable, column_comment = item
                length = "0"
                if str(column_type).find('(') > -1:
                    column_type, length = str(column_type).replace(")", '').split('(')
                if column_key == 'PRI':
                    column_key = "是"
                else:
                    column_key = ''
                if is_nullable == 'YES':
                    is_nullable = '是'
                else:
                    is_nullable = '否'
                struct_list.append([column_name, column_type, length, column_key, is_nullable, column_comment])
            yield [struct_list, tb_name]

    def __get_all_tables(self, con):
        res = con.query("SHOW TABLES")
        tb_list = []
        for item in res:
            tb_list.append(item[0])
        return tb_list

    def export(self):
        if len(self.db_names) == 0:
            print("请配置数据库列表")
        for i, db_name in enumerate(self.db_names):
            connect = self.__connect_to_mysql(db_name)
            if not os.path.exists(self.__save_dir):
                os.mkdir(self.__save_dir)

            file_name = os.path.join(self.__save_dir,'{}.xlsx'.format(db_name))
            if not os.path.exists(file_name):  # 文件不存在时自动创建文件 excel
                wrokb = openpyxl.Workbook()
                wrokb.save(file_name)
                wrokb.close()
            wb = openpyxl.load_workbook(file_name)
            writer = pd.ExcelWriter(file_name, engine='openpyxl')
            writer.book = wb

            struct_generator = self.__struct_of_table_generator(connect, db_name)

            for tb_info in tqdm(struct_generator, desc=db_name):
                s_list, tb_name = tb_info
                data = pd.DataFrame(s_list, columns=self.__excel_title)
                data.to_excel(writer, sheet_name=tb_name)
            writer.close()

            connect.close()


if __name__ == '__main__':
    apps = ExportMysqlTableStructureInfoToExcel()
    apps.export()

