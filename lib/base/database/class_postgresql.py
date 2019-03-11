# coding=UTF-8

"""
=========================================
PostgreSQL数据库具体集合类
=========================================

:Author: glen
:Date: 2019.02.19
:Tags: postgresql database
:abstract: 连接postgresql数据库，并进行基本操作。

**类**
==================
PostgreSQL
    连接MongoDB数据库


**使用方法**
==================
PostgreSQL的Python接口
"""
import psycopg2


class PostgreSQL:
    """PostgreSQL的Python接口

    """
    def __init__(self, dbname='Course', user='plutoese', password='z1Yh29', host='47.96.41.8'):
        """初始化

        :param dbname: 数据库名称
        :param user: 用户名
        :param password: 密码
        :param host: 数据库主机
        """
        self._conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
        self._cur = self._conn.cursor()

    def close(self):
        self._cur.close()
        self._conn.close()

    @property
    def conn(self):
        return self._conn

    @property
    def cur(self):
        return self._cur


if __name__ == '__main__':
    conn = psycopg2.connect(dbname="Course", user="plutoese", password="z1Yh29", host="47.96.41.8")
    print(conn.server_version)



