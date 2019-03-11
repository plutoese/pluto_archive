# coding=UTF-8

"""
=========================================
YAML导入与解析
=========================================

:Author: glen
:Date: 2019.02.19
:Tags: yaml yml
:abstract: YAML导入与解析

**类**
==================
YAML


**使用方法**
==================

"""
import yaml
from collections import OrderedDict


class YAML:
    def __init__(self, file=None, encoding='UTF-8'):
        f = open(file, encoding=encoding)
        self._content = yaml.load(f)


    @property
    def content(self):
        return self._content

if __name__ == '__main__':
    yml = YAML(file = r'E:\cyberspace\shinyproxy\config\application.yml')
    users = yml.content['proxy']['users']
    users.append({'name': 'Alice', 'password': 'Alice', 'groups': 'pluto'})
    stream = open(r'E:\cyberspace\shinyproxy\config\application3.yml', 'w')
    yaml.dump(users, stream, default_flow_style=False)