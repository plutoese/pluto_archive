# coding=UTF-8

# --------------------------------------------------
# @title: config users
# @intro: to generate users in application.yml
# @author: Glen
# @date: 2019.02.20
# @tag: shiny
# --------------------------------------------------

import yaml
import csv
import os


# 0. param
ENCODING = 'UTF-8'
YML_PATH = r'E:\cyberspace\shinyproxy\config'
user_csv_file = os.path.join(YML_PATH, 'users.csv')
user_yml_file = os.path.join(YML_PATH, 'users.yml')

# 1. to read from users.csv
csvfile = open(user_csv_file, 'r')
reader = csv.reader(csvfile)
users = []
usernames = set()
for item in [line for line in reader][1:]:
    if item[0] not in usernames:
        usernames.add(item[0])
        users.append(dict(zip(['name','password','groups'],item)))

# 2. to export users
stream = open(user_yml_file, 'w')
yaml.dump(users, stream, default_flow_style=False)
