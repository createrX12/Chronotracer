# coding=utf-8
"""
@author B1lli
@date 2023年02月03日 00:06:34
@File:save_to_sqlite.py
"""
import sqlite3

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class Sqlite_interact():
    def __init__(self):
        # 创建一个数据库引擎，并设置连接池大小为10
        self.engine = create_engine ( "sqlite:///F:\CLR_backup\CLR.db", pool_size=10 )

        # 创建一个会话工厂，用于生成会话对象
        self.Session = sessionmaker ( bind=self.engine )


    def write_to_db(self,table_name, field_values):
        self.session = self.Session ()
        self.session.execute(f"INSERT INTO {table_name} ({', '.join(field_values.keys())}) VALUES ({', '.join(['?' for value in field_values.values()])})", tuple([str(value) for value in field_values.values()]))
        self.session.commit()
        self.session.close()

    def query_db(self, table_name, query_values, output_fields) :
        '''
        query_db
        :param table_name:你要在该sqlite数据库中查询的表名。接受一个字符串
        :param query_values: 你要查询的字段名和该字段对应的值，对于一条数据，在该字段中，只要包含此数据便可被查询到。多个键值对需要同时被满足才能被查询到，是AND关系。接受一个字典
        :param output_fields: 输出的字段，查询完毕后将会以嵌套列表形式返回所有符合条件的行的这些字段。接受一个列表
        :return :
        '''
        self.session = self.Session ()
        query_text = "SELECT " + ", ".join ( output_fields ) + " FROM " + table_name + " WHERE "
        conditions = []
        for key, value in query_values.items () :
            if key == 'pic_date':
                conditions.append ( key + " = '" + value + "'" )
            else:
                conditions.append ( key + " LIKE '%" + value + "%'" )

        query_text += " AND ".join ( conditions )
        # print(query_text)
        result = self.session.query(sqlalchemy.text(query_text))
        # self.session.close()
        return result

    def close_db(self):
        self.session.close()

if __name__ == '__main__':
    a = Sqlite_interact()
    b = a.query_db('pic_data', {'pic_text' : f'上海','pic_date' : f'2023-2-1'},['pic_seq','pic_date','pic_resolution'])
    print(b)

# class Sqlite_interact():
#     def __init__(self):
#         self.conn = sqlite3.connect ( "F:\CLR_backup\CLR.db", check_same_thread=False)
#         self.c = self.conn.cursor ()
#
#     def write_to_db(self,table_name, field_values):
#         # c.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT, {', '.join([f'{key} TEXT' for key in field_values.keys()])})")
#         self.c.execute(f"INSERT INTO {table_name} ({', '.join(field_values.keys())}) VALUES ({', '.join(['?' for value in field_values.values()])})", tuple([str(value) for value in field_values.values()]))
#         self.conn.commit()
#
#     def query_db(self, table_name, query_values, output_fields) :#改成键值对
#         '''
#         query_db
#         :param table_name:你要在该sqlite数据库中查询的表名。接受一个字符串
#         :param query_values: 你要查询的字段名和该字段对应的值，对于一条数据，在该字段中，只要包含此数据便可被查询到。多个键值对需要同时被满足才能被查询到，是AND关系。接受一个字典
#         :param output_fields: 输出的字段，查询完毕后将会以嵌套列表形式返回所有符合条件的行的这些字段。接受一个列表
#         :return:
#         '''
#         query = "SELECT " + ", ".join ( output_fields ) + " FROM " + table_name + " WHERE "
#         conditions = []
#         for key, value in query_values.items () :
#             conditions.append ( key + " LIKE '%" + value + "%'" )
#         query += " AND ".join ( conditions )
#         self.c.execute ( query )
#         result = self.c.fetchall ()
#         return result
#
#     def close_db(self):
#         self.conn.close()


