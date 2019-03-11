# coding = UTF-8

import re
from pymongo import ASCENDING
import pandas as pd
from lib.base.database.class_mongodb import MongoDB, MonCollection

# 0. 学校名称转换
college_tranform = {'中国科技大学':'中国科学技术大学',
                    '中国矿业大学':'中国矿业大学(北京)',
                    '中国地质大学':'中国地质大学(北京)',
                    '中国石油大学':'中国石油大学(北京)',
                    '河北医科大学':'河北中医学院',
                    '温州医学院':'温州医科大学',
                    '重庆工学院':'重庆理工大学(原重庆工学院)',
                    '江西中医学院':'江西中医药大学',
                    '北京建筑工程学院':'北京建筑大学',
                    '武汉工业学院':'武汉轻工大学',
                    '贵阳医学院':'贵州医科大学',
                    '山东轻工业学院':'齐鲁工业大学',
                    '中国计量学院':'中国计量大学',
                    '浙江财经学院':'浙江财经大学',
                    '泸州医学院':'四川医科大学',
                    '安徽中医学院':'安徽中医药大学',
                    '山东经济学院':'山东财经大学',
                    '广东商学院':'广东财经大学',
                    '大理学院':'大理大学',
                    '天津城市建设学院':'天津城建大学',
                    '内蒙古医学院':'内蒙古医科大学',
                    '华北水利水电学院':'华北水利水电大学',
                    '黑龙江科技学院':'黑龙江科技大学',
                    '四川外语学院':'四川外国语大学',
                    '安徽建筑工业学院':'安徽建筑大学',
                    '广西工学院':'广西科技大学',
                    '河南中医学院':'河南中医药大学',
                    '兰州商学院':'兰州财经大学',
                    '大连外国语学院':'大连外国语大学',
                    '大连民族学院':'大连民族大学',
                    '上海对外贸易学院':'上海对外经贸大学',
                    '陕西中医学院':'陕西中医药大学',
                    '成都信息工程学院':'成都信息工程大学',
                    '吉林建筑工程学院':'吉林建筑大学',
                    '漳州师范学院':'闽南师范大学',
                    '阜阳师范学院':'阜阳师范学院信息工程学院',
                    '长春师范学院':'长春师范大学',
                    '喀什师范学院':'喀什大学',
                    '江苏技术师范学院':'江苏理工学院',
                    '上海金融学院':'上海立信会计金融学院',
                    '咸宁学院':'湖北科技学院',
                    '孝感学院':'湖北工程学院',
                    '上海立信会计学院':'上海立信会计金融学院',
                    '昆明学院':'昆明大学',
                    '襄樊学院':'湖北文理学院',
                    '东北石油大学':'大庆石油学院',
                    '桂林理工大学':'桂林工学院',
                    '石家庄铁道大学':'石家庄铁道学院',
                    '宁夏医科大学':'宁夏医学院',
                    '武汉纺织大学':'武汉科技学院',
                    '浙江农林大学':'浙江林学院',
                    '重庆理工大学':'重庆理工大学(原重庆工学院)',
                    '湖北中医药大学':'湖北中医学院',
                    '河北联合大学':'河北理工大学',
                    '沈阳航空航天大学':'沈阳航空工业学院',
                    '常州大学':'江苏工业学院',
                    '河南财经政法大学':'河南财经学院 ',
                    '西南林业大学':'西南林学院',
                    '福建中医药大学':'福建中医学院',
                    '沈阳化工大学':'沈阳化工学院',
                    '青海民族大学':'青海民族学院',
                    '大连海洋大学':'大连水产学院',
                    '淮北师范大学':'淮北煤炭师范学院',
                    '安徽工程大学':'安徽工程科技学院',
                    '临沂大学':'临沂师范学院',
                    '黄石理工学院':'湖北理工学院',
                    '成都学院':'成都大学',
                    '茂名学院':'广东石油化工学院',
                    '太原工业大学':'太原理工大学',
                    '江苏师范大学':'徐州师范大学',
                    '昆明医科大学':'昆明医学院',
                    '广西中医药大学 ':'广西中医学院',
                    '贵州财经大学':'贵州财经学院',
                    '贵州民族大学':'贵州民族学院',
                    '吉林财经大学':'长春税务学院',
                    '西安邮电大学':'西安邮电学院',
                    '江西科技师范大学':'江西科技师范学院',
                    '天津外国语大学':'天津工程师范学院',
                    '内蒙古财经大学':'内蒙古财经学院',
                    '贵州师范学院':'贵州师范大学',
                    }


def college_replace(college_name):
    if college_name in college_tranform:
        return college_tranform[college_name]
    else:
        return college_name

# 1. 数据库连接
mongo = MongoDB(conn_str='localhost:27017')
college_info_con = MonCollection(mongo, database='webdata', collection_name='college_info').collection
entrance_score_con = MonCollection(mongo, database='webdata', collection_name='gaokao_entrancescore').collection

# 2. 数据库大学集合
entrance_colleges = entrance_score_con.find().distinct('university')

# 3. 导入校友会大学
college_rate_2011_filepath = r'E:\cyberspace\worklot\college\2011年校友会大学排名.xlsx'
college_2011 = pd.read_excel(college_rate_2011_filepath)
college_2011['学校名称'] = college_2011['学校名称'].apply(college_replace)
for item in college_2011['学校名称']:
    if item not in entrance_colleges:
        print(item)

college_rate_2012_filepath = r'E:\cyberspace\worklot\college\2012年校友会大学排名.xlsx'
college_2012 = pd.read_excel(college_rate_2012_filepath)
college_2012['学校名称'] = college_2012['学校名称'].apply(college_replace)
for item in college_2012['学校名称']:
    if item not in entrance_colleges:
        print(item)

college_rate_2013_filepath = r'E:\cyberspace\worklot\college\2013年校友会大学排名.xlsx'
college_2013 = pd.read_excel(college_rate_2013_filepath)
college_2013['学校名称'] = college_2013['学校名称'].apply(college_replace)
for item in college_2013['学校名称']:
    if item not in entrance_colleges:
        print(item)

college_2011.to_excel(r'E:\cyberspace\worklot\college\2011年校友会大学排名_rename.xlsx')
college_2012.to_excel(r'E:\cyberspace\worklot\college\2012年校友会大学排名_rename.xlsx')
college_2013.to_excel(r'E:\cyberspace\worklot\college\2013年校友会大学排名_rename.xlsx')