# coding = UTF-8

import re
import pysal
from pymongo import ASCENDING
import pandas as pd
from lib.base.database.class_mongodb import MongoDB, MonCollection
from application.dataworld.admindivision.class_admindivision import AdminDivision

# 1. 数据库连接
mongo = MongoDB(conn_str='localhost:27017')
college_info_con = MonCollection(mongo, database='webdata', collection_name='college_info').collection
entrance_score_con = MonCollection(mongo, database='webdata', collection_name='gaokao_entrancescore').collection

# 2. 步骤参数设置
# a. 导出每年的高考分数数据
IS_EXPORT_RAW_EXAM_SCORE = False
# b. 导出高校信息数据
IS_EXPORT_RAW_COLLEGE_INFO = False
# c. 2011-2013年面板数据
IS_MERGE_INTO_PANEL = False
# d. 合并高校信息数据
IS_MERGE_COLLEGE_INFO = False
# e. 合并大学排名信息
IS_MERGE_COLLEGE_RATE = False
# f. 合并省级经济信息
IS_MERGE_PROVINCE_PERGDP = False
# g. 合并地级市信息
TEMP1 = False
TEMP2 = False
IS_MERGE_CITY_STAT = False
# h. 合并大学创立的年份
IS_MERGE_START_YEAR = False
# i. 添加本地和附近高校的虚拟变量
IS_ADD_LOCAL_VAR = False
IS_ADD_NEARBY_VAR = False
# j. 添加本地的人均实际GDP信息
IS_ADD_LOCAL_PERGDP = True


if IS_EXPORT_RAW_EXAM_SCORE:
    for year in range(2010, 2018):
        found = entrance_score_con.find({'年份':year, 'type':'文科', "录取批次" : "第一批"},
                                        sort=[('regioncode',ASCENDING),('university',ASCENDING)])
        raw_dataframe = pd.DataFrame(list(found))
        raw_dataframe.to_excel(r'E:\cyberspace\worklot\college\dataset\raw\{}年高考文科第一批录取分数横截面数据.xlsx'.format(str(year)))

        found = entrance_score_con.find({'年份': year, 'type': '文科', "录取批次": "第二批"},
                                        sort=[('regioncode', ASCENDING), ('university', ASCENDING)])
        raw_dataframe = pd.DataFrame(list(found))
        raw_dataframe.to_excel(r'E:\cyberspace\worklot\college\dataset\raw\{}年高考文科第二批录取分数横截面数据.xlsx'.format(str(year)))

        found = entrance_score_con.find({'年份': year, 'type': '理科', "录取批次" : "第一批"},
                                        sort=[('regioncode', ASCENDING), ('university', ASCENDING)])
        raw_dataframe = pd.DataFrame(list(found))
        raw_dataframe.to_excel(r'E:\cyberspace\worklot\college\dataset\raw\{}年高考理科第一批录取分数横截面数据.xlsx'.format(str(year)))

        found = entrance_score_con.find({'年份': year, 'type': '理科', "录取批次": "第二批"},
                                        sort=[('regioncode', ASCENDING), ('university', ASCENDING)])
        raw_dataframe = pd.DataFrame(list(found))
        raw_dataframe.to_excel(r'E:\cyberspace\worklot\college\dataset\raw\{}年高考理科第二批录取分数横截面数据.xlsx'.format(str(year)))

if IS_EXPORT_RAW_COLLEGE_INFO:
    found = college_info_con.find(sort=[('高校所在地行政代码',ASCENDING)])
    raw_dataframe = pd.DataFrame(list(found))

    raw_dataframe.to_excel(r'E:\cyberspace\worklot\college\dataset\raw\高校信息数据.xlsx')

if IS_MERGE_INTO_PANEL:
    # 2011-2013理科第一批录取分数面板数据
    exam_score_science_first_2011 = pd.read_excel(r'E:\cyberspace\worklot\college\dataset\process\2011年高考理科第一批录取分数横截面数据.xlsx')
    exam_score_science_first_2012 = pd.read_excel(r'E:\cyberspace\worklot\college\dataset\process\2012年高考理科第一批录取分数横截面数据.xlsx')
    exam_score_science_first_2013 = pd.read_excel(r'E:\cyberspace\worklot\college\dataset\process\2013年高考理科第一批录取分数横截面数据.xlsx')

    pdataframe_science_first = pd.concat([exam_score_science_first_2011,
                                          exam_score_science_first_2012,
                                          exam_score_science_first_2013])

    pdataframe_science_first.to_excel(r'E:\cyberspace\worklot\college\dataset\process\2011-2013高考理科第一批录取分数面板数据.xlsx')

    # 2011-2013理科第一批录取分数面板数据
    exam_score_science_second_2011 = pd.read_excel(
        r'E:\cyberspace\worklot\college\dataset\process\2011年高考理科第二批录取分数横截面数据.xlsx')
    exam_score_science_second_2012 = pd.read_excel(
        r'E:\cyberspace\worklot\college\dataset\process\2012年高考理科第二批录取分数横截面数据.xlsx')
    exam_score_science_second_2013 = pd.read_excel(
        r'E:\cyberspace\worklot\college\dataset\process\2013年高考理科第二批录取分数横截面数据.xlsx')

    pdataframe_science_second = pd.concat([exam_score_science_second_2011,
                                           exam_score_science_second_2012,
                                           exam_score_science_second_2013])

    pdataframe_science_second.to_excel(r'E:\cyberspace\worklot\college\dataset\process\2011-2013高考理科第二批录取分数面板数据.xlsx')

    # 2011-2013文科第一批录取分数面板数据
    exam_score_art_first_2011 = pd.read_excel(
        r'E:\cyberspace\worklot\college\dataset\process\2011年高考文科第一批录取分数横截面数据.xlsx')
    exam_score_art_first_2012 = pd.read_excel(
        r'E:\cyberspace\worklot\college\dataset\process\2012年高考文科第一批录取分数横截面数据.xlsx')
    exam_score_art_first_2013 = pd.read_excel(
        r'E:\cyberspace\worklot\college\dataset\process\2013年高考文科第一批录取分数横截面数据.xlsx')

    pdataframe_art_first = pd.concat([exam_score_art_first_2011,
                                          exam_score_art_first_2012,
                                          exam_score_art_first_2013])

    pdataframe_art_first.to_excel(r'E:\cyberspace\worklot\college\dataset\process\2011-2013高考文科第一批录取分数面板数据.xlsx')

    # 2011-2013文科第二批录取分数面板数据
    exam_score_art_second_2011 = pd.read_excel(
        r'E:\cyberspace\worklot\college\dataset\process\2011年高考文科第二批录取分数横截面数据.xlsx')
    exam_score_art_second_2012 = pd.read_excel(
        r'E:\cyberspace\worklot\college\dataset\process\2012年高考文科第二批录取分数横截面数据.xlsx')
    exam_score_art_second_2013 = pd.read_excel(
        r'E:\cyberspace\worklot\college\dataset\process\2013年高考文科第二批录取分数横截面数据.xlsx')

    pdataframe_art_second = pd.concat([exam_score_art_second_2011,
                                       exam_score_art_second_2012,
                                       exam_score_art_second_2013])

    pdataframe_art_second.to_excel(r'E:\cyberspace\worklot\college\dataset\process\2011-2013高考文科第二批录取分数面板数据.xlsx')

if IS_MERGE_COLLEGE_INFO:
    university_info = pd.read_excel(
        r'E:\cyberspace\worklot\college\dataset\process\高校信息第一次处理数据.xlsx')

    pdataframe_science_first = pd.read_excel(
        r'E:\cyberspace\worklot\college\dataset\process\2011-2013高考理科第一批录取分数面板数据.xlsx')
    pdataframe_science_first_merged_info = pd.merge(pdataframe_science_first, university_info, how='left', on='university')
    pdataframe_science_first_merged_info.to_excel(r'E:\cyberspace\worklot\college\dataset\process\2011-2013高考理科第一批录取分数面板数据_添加大学信息.xlsx')

    pdataframe_science_second = pd.read_excel(
        r'E:\cyberspace\worklot\college\dataset\process\2011-2013高考理科第二批录取分数面板数据.xlsx')
    pdataframe_science_second_merged_info = pd.merge(pdataframe_science_second, university_info, how='left',
                                                    on='university')
    pdataframe_science_second_merged_info.to_excel(
        r'E:\cyberspace\worklot\college\dataset\process\2011-2013高考理科第二批录取分数面板数据_添加大学信息.xlsx')

    pdataframe_art_first = pd.read_excel(
        r'E:\cyberspace\worklot\college\dataset\process\2011-2013高考文科第一批录取分数面板数据.xlsx')
    pdataframe_art_first_merged_info = pd.merge(pdataframe_art_first, university_info, how='left',
                                                    on='university')
    pdataframe_art_first_merged_info.to_excel(
        r'E:\cyberspace\worklot\college\dataset\process\2011-2013高考文科第一批录取分数面板数据_添加大学信息.xlsx')

    pdataframe_art_second = pd.read_excel(
        r'E:\cyberspace\worklot\college\dataset\process\2011-2013高考文科第二批录取分数面板数据.xlsx')
    pdataframe_art_second_merged_info = pd.merge(pdataframe_art_second, university_info, how='left',
                                                on='university')
    pdataframe_art_second_merged_info.to_excel(
        r'E:\cyberspace\worklot\college\dataset\process\2011-2013高考文科第二批录取分数面板数据_添加大学信息.xlsx')

if IS_MERGE_COLLEGE_RATE:
    university_rate_2011 = pd.read_excel(
        r'E:\cyberspace\worklot\college\dataset\raw\2011年校友会大学排名_v2.xlsx')
    university_rate_2012 = pd.read_excel(
        r'E:\cyberspace\worklot\college\dataset\raw\2012年校友会大学排名_v2.xlsx')
    university_rate_2013 = pd.read_excel(
        r'E:\cyberspace\worklot\college\dataset\raw\2013年校友会大学排名_v2.xlsx')

    university_rate = pd.concat([university_rate_2011,
                                 university_rate_2012,
                                 university_rate_2013])

    pdataframe_science_first_v1 = pd.read_excel(
        r'E:\cyberspace\worklot\college\dataset\process\2011-2013高考理科第一批录取分数面板数据_添加大学信息.xlsx')
    pdataframe_science_first_v1_merged_rate = pd.merge(pdataframe_science_first_v1, university_rate, how='left',
                                                    on=['university','年份'])
    pdataframe_science_first_v1_merged_rate.to_excel(
        r'E:\cyberspace\worklot\college\dataset\process\2011-2013高考理科第一批录取分数面板数据_v2.xlsx')

    pdataframe_science_second_v1 = pd.read_excel(
        r'E:\cyberspace\worklot\college\dataset\process\2011-2013高考理科第二批录取分数面板数据_添加大学信息.xlsx')
    pdataframe_science_second_v1_merged_rate = pd.merge(pdataframe_science_second_v1, university_rate, how='left',
                                                       on=['university', '年份'])
    pdataframe_science_second_v1_merged_rate.to_excel(
        r'E:\cyberspace\worklot\college\dataset\process\2011-2013高考理科第二批录取分数面板数据_v2.xlsx')

    pdataframe_art_first_v1 = pd.read_excel(
        r'E:\cyberspace\worklot\college\dataset\process\2011-2013高考文科第一批录取分数面板数据_添加大学信息.xlsx')
    pdataframe_art_first_v1_merged_rate = pd.merge(pdataframe_art_first_v1, university_rate, how='left',
                                                       on=['university', '年份'])
    pdataframe_art_first_v1_merged_rate.to_excel(
        r'E:\cyberspace\worklot\college\dataset\process\2011-2013高考文科第一批录取分数面板数据_v2.xlsx')

    pdataframe_art_second_v1 = pd.read_excel(
        r'E:\cyberspace\worklot\college\dataset\process\2011-2013高考文科第二批录取分数面板数据_添加大学信息.xlsx')
    pdataframe_art_second_v1_merged_rate = pd.merge(pdataframe_art_second_v1, university_rate, how='left',
                                                        on=['university', '年份'])
    pdataframe_art_second_v1_merged_rate.to_excel(
        r'E:\cyberspace\worklot\college\dataset\process\2011-2013高考文科第二批录取分数面板数据_v2.xlsx')

if IS_MERGE_PROVINCE_PERGDP:
    province_real_perGDP = pd.read_excel(
        r'E:\cyberspace\worklot\college\dataset\raw\province_real_perGDP.xlsx')

    pdataframe_science_first_v2 = pd.read_excel(
        r'E:\cyberspace\worklot\college\dataset\process\2011-2013高考理科第一批录取分数面板数据_v2.xlsx')
    pdataframe_science_first_v2_merged_rate = pd.merge(pdataframe_science_first_v2, province_real_perGDP, how='left',
                                                       on=['高校所在地行政代码', '年份'])
    pdataframe_science_first_v2_merged_rate.to_excel(
        r'E:\cyberspace\worklot\college\dataset\process\2011-2013高考理科第一批录取分数面板数据_v3.xlsx')

    pdataframe_science_second_v2 = pd.read_excel(
        r'E:\cyberspace\worklot\college\dataset\process\2011-2013高考理科第二批录取分数面板数据_v2.xlsx')
    pdataframe_science_second_v2_merged_rate = pd.merge(pdataframe_science_second_v2, province_real_perGDP, how='left',
                                                       on=['高校所在地行政代码', '年份'])
    pdataframe_science_second_v2_merged_rate.to_excel(
        r'E:\cyberspace\worklot\college\dataset\process\2011-2013高考理科第二批录取分数面板数据_v3.xlsx')

    pdataframe_art_first_v2 = pd.read_excel(
        r'E:\cyberspace\worklot\college\dataset\process\2011-2013高考文科第一批录取分数面板数据_v2.xlsx')
    pdataframe_art_first_v2_merged_rate = pd.merge(pdataframe_art_first_v2, province_real_perGDP, how='left',
                                                       on=['高校所在地行政代码', '年份'])
    pdataframe_art_first_v2_merged_rate.to_excel(
        r'E:\cyberspace\worklot\college\dataset\process\2011-2013高考文科第一批录取分数面板数据_v3.xlsx')

    pdataframe_art_second_v2 = pd.read_excel(
        r'E:\cyberspace\worklot\college\dataset\process\2011-2013高考文科第二批录取分数面板数据_v2.xlsx')
    pdataframe_art_second_v2_merged_rate = pd.merge(pdataframe_art_second_v2, province_real_perGDP, how='left',
                                                   on=['高校所在地行政代码', '年份'])
    pdataframe_art_second_v2_merged_rate.to_excel(
        r'E:\cyberspace\worklot\college\dataset\process\2011-2013高考文科第二批录取分数面板数据_v3.xlsx')

if TEMP1:
    city_raw_stat = pd.read_excel(
        r'E:\cyberspace\worklot\college\dataset\raw\中国城市统计年鉴GDP数据.xlsx')

    city_raw_stat['人均GDP2011'] = city_raw_stat['地区生产总值2011'].div(city_raw_stat['年末总人口2011'])
    city_raw_stat['GDP2012'] = city_raw_stat['地区生产总值2011'].mul(1+city_raw_stat['地区生产总值增长率2012']/100)
    city_raw_stat['人均GDP2012'] = city_raw_stat['GDP2012'].div(city_raw_stat['年末总人口2012'])
    city_raw_stat['GDP2013'] = city_raw_stat['GDP2012'].mul(1 + city_raw_stat['地区生产总值增长率2013'] / 100)
    city_raw_stat['人均GDP2013'] = city_raw_stat['GDP2013'].div(city_raw_stat['年末总人口2013'])

    city_raw_stat.to_excel(
        r'E:\cyberspace\worklot\college\dataset\raw\中国城市统计年鉴真实GDP数据.xlsx')

if TEMP2:
    city_info = pd.read_excel(
        r'E:\cyberspace\worklot\college\dataset\raw\colleges_with_city.xlsx')

    adivision = AdminDivision(year='2012')
    cities = list(city_info['city'])

    city_code = []
    for city in cities:
        result = adivision[city]
        city_code.append(result['acode'].values[0])

    city_info['city_code'] = city_code

    city_info.to_excel(
        r'E:\cyberspace\worklot\college\dataset\raw\大学所在的地级城市.xlsx')

if IS_MERGE_CITY_STAT:
    city_info = pd.read_excel(
        r'E:\cyberspace\worklot\college\dataset\raw\大学所在的地级城市.xlsx')
    city_stat = pd.read_excel(
        r'E:\cyberspace\worklot\college\dataset\raw\中国城市统计数据v1.xlsx')

    pdataframe_science_first_v3 = pd.read_excel(
        r'E:\cyberspace\worklot\college\dataset\process\2011-2013高考理科第一批录取分数面板数据_v3.xlsx')
    pdataframe_science_first_v3_merged_rate = pd.merge(pdataframe_science_first_v3, city_info, how='left',
                                                       on='university')
    pdataframe_science_first_v4_merged_rate = pd.merge(pdataframe_science_first_v3_merged_rate, city_stat, how='left',
                                                       on=['city_code','年份'])
    pdataframe_science_first_v3_merged_rate.to_excel(
        r'E:\cyberspace\worklot\college\dataset\process\2011-2013高考理科第一批录取分数面板数据_v4.xlsx')
    pdataframe_science_first_v4_merged_rate.to_excel(
        r'E:\cyberspace\worklot\college\dataset\process\2011-2013高考理科第一批录取分数面板数据_v5.xlsx')

    pdataframe_science_second_v3 = pd.read_excel(
        r'E:\cyberspace\worklot\college\dataset\process\2011-2013高考理科第二批录取分数面板数据_v3.xlsx')
    pdataframe_science_second_v3_merged_rate = pd.merge(pdataframe_science_second_v3, city_info, how='left',
                                                       on='university')
    pdataframe_science_second_v4_merged_rate = pd.merge(pdataframe_science_second_v3_merged_rate, city_stat, how='left',
                                                       on=['city_code', '年份'])
    pdataframe_science_second_v3_merged_rate.to_excel(
        r'E:\cyberspace\worklot\college\dataset\process\2011-2013高考理科第二批录取分数面板数据_v4.xlsx')
    pdataframe_science_second_v4_merged_rate.to_excel(
        r'E:\cyberspace\worklot\college\dataset\process\2011-2013高考理科第二批录取分数面板数据_v5.xlsx')

    pdataframe_art_first_v3 = pd.read_excel(
        r'E:\cyberspace\worklot\college\dataset\process\2011-2013高考文科第一批录取分数面板数据_v3.xlsx')
    pdataframe_art_first_v3_merged_rate = pd.merge(pdataframe_art_first_v3, city_info, how='left',
                                                       on='university')
    pdataframe_art_first_v4_merged_rate = pd.merge(pdataframe_art_first_v3_merged_rate, city_stat, how='left',
                                                       on=['city_code', '年份'])
    pdataframe_art_first_v3_merged_rate.to_excel(
        r'E:\cyberspace\worklot\college\dataset\process\2011-2013高考文科第一批录取分数面板数据_v4.xlsx')
    pdataframe_art_first_v4_merged_rate.to_excel(
        r'E:\cyberspace\worklot\college\dataset\process\2011-2013高考文科第一批录取分数面板数据_v5.xlsx')

    pdataframe_art_second_v3 = pd.read_excel(
        r'E:\cyberspace\worklot\college\dataset\process\2011-2013高考文科第二批录取分数面板数据_v3.xlsx')
    pdataframe_art_second_v3_merged_rate = pd.merge(pdataframe_art_second_v3, city_info, how='left',
                                                   on='university')
    pdataframe_art_second_v4_merged_rate = pd.merge(pdataframe_art_second_v3_merged_rate, city_stat, how='left',
                                                   on=['city_code', '年份'])
    pdataframe_art_second_v3_merged_rate.to_excel(
        r'E:\cyberspace\worklot\college\dataset\process\2011-2013高考文科第二批录取分数面板数据_v4.xlsx')
    pdataframe_art_second_v4_merged_rate.to_excel(
        r'E:\cyberspace\worklot\college\dataset\process\2011-2013高考文科第二批录取分数面板数据_v5.xlsx')

if IS_MERGE_START_YEAR:
    college_start_year = pd.read_excel(
        r'E:\cyberspace\worklot\college\dataset\raw\colleges_start_date.xlsx')

    pdataframe_science_first_v5 = pd.read_excel(
        r'E:\cyberspace\worklot\college\dataset\process\2011-2013高考理科第一批录取分数面板数据_v5.xlsx')
    pdataframe_science_first_v5_merged_start_year = pd.merge(pdataframe_science_first_v5, college_start_year,
                                                             how='left',
                                                             on='university')
    pdataframe_science_first_v5_merged_start_year.to_excel(
        r'E:\cyberspace\worklot\college\dataset\process\2011-2013高考理科第一批录取分数面板数据_v6.xlsx')

    pdataframe_science_second_v5 = pd.read_excel(
        r'E:\cyberspace\worklot\college\dataset\process\2011-2013高考理科第二批录取分数面板数据_v5.xlsx')
    pdataframe_science_second_v5_merged_start_year = pd.merge(pdataframe_science_second_v5, college_start_year,
                                                             how='left',
                                                             on='university')
    pdataframe_science_second_v5_merged_start_year.to_excel(
        r'E:\cyberspace\worklot\college\dataset\process\2011-2013高考理科第二批录取分数面板数据_v6.xlsx')

    pdataframe_art_first_v5 = pd.read_excel(
        r'E:\cyberspace\worklot\college\dataset\process\2011-2013高考文科第一批录取分数面板数据_v5.xlsx')
    pdataframe_art_first_v5_merged_start_year = pd.merge(pdataframe_art_first_v5, college_start_year,
                                                         how='left',
                                                         on='university')
    pdataframe_art_first_v5_merged_start_year.to_excel(
        r'E:\cyberspace\worklot\college\dataset\process\2011-2013高考文科第一批录取分数面板数据_v6.xlsx')

    pdataframe_art_second_v5 = pd.read_excel(
        r'E:\cyberspace\worklot\college\dataset\process\2011-2013高考文科第二批录取分数面板数据_v5.xlsx')
    pdataframe_art_second_v5_merged_start_year = pd.merge(pdataframe_art_second_v5, college_start_year,
                                                          how='left',
                                                          on='university')
    pdataframe_art_second_v5_merged_start_year.to_excel(
        r'E:\cyberspace\worklot\college\dataset\process\2011-2013高考文科第二批录取分数面板数据_v6.xlsx')

if IS_ADD_LOCAL_VAR:
    pdataframe_science_first_v6 = pd.read_excel(
        r'E:\cyberspace\worklot\college\dataset\process\2011-2013高考理科第一批录取分数面板数据_v6.xlsx')
    pdataframe_science_first_v6['local'] = 0
    pdataframe_science_first_v6.loc[pdataframe_science_first_v6['regioncode'].eq(pdataframe_science_first_v6['高校所在地行政代码']), 'local'] = 1
    pdataframe_science_first_v6.to_excel(
        r'E:\cyberspace\worklot\college\dataset\process\2011-2013高考理科第一批录取分数面板数据_v7.xlsx')

    pdataframe_science_second_v6 = pd.read_excel(
        r'E:\cyberspace\worklot\college\dataset\process\2011-2013高考理科第二批录取分数面板数据_v6.xlsx')
    pdataframe_science_second_v6['local'] = 0
    pdataframe_science_second_v6.loc[
        pdataframe_science_second_v6['regioncode'].eq(pdataframe_science_second_v6['高校所在地行政代码']), 'local'] = 1
    pdataframe_science_second_v6.to_excel(
        r'E:\cyberspace\worklot\college\dataset\process\2011-2013高考理科第二批录取分数面板数据_v7.xlsx')

    pdataframe_art_first_v6 = pd.read_excel(
        r'E:\cyberspace\worklot\college\dataset\process\2011-2013高考文科第一批录取分数面板数据_v6.xlsx')
    pdataframe_art_first_v6['local'] = 0
    pdataframe_art_first_v6.loc[
        pdataframe_art_first_v6['regioncode'].eq(pdataframe_art_first_v6['高校所在地行政代码']), 'local'] = 1
    pdataframe_art_first_v6.to_excel(
        r'E:\cyberspace\worklot\college\dataset\process\2011-2013高考文科第一批录取分数面板数据_v7.xlsx')

    pdataframe_art_second_v6 = pd.read_excel(
        r'E:\cyberspace\worklot\college\dataset\process\2011-2013高考文科第二批录取分数面板数据_v6.xlsx')
    pdataframe_art_second_v6['local'] = 0
    pdataframe_art_second_v6.loc[
        pdataframe_art_second_v6['regioncode'].eq(pdataframe_art_second_v6['高校所在地行政代码']), 'local'] = 1
    pdataframe_art_second_v6.to_excel(
        r'E:\cyberspace\worklot\college\dataset\process\2011-2013高考文科第二批录取分数面板数据_v7.xlsx')

if IS_ADD_NEARBY_VAR:
    stata_txt = pysal.open(r'E:\cyberspace\worklot\college\dataset\raw\province2004W.txt', 'r',
                           'stata_text')
    w = stata_txt.read()
    stata_txt.close()

    neighbors = dict()
    for key in w.neighbors:
        neighbors[key] = [item for item in w.neighbors[key]]
    neighbors[460000] = [440000]

    pdataframe_science_first_v7 = pd.read_excel(
        r'E:\cyberspace\worklot\college\dataset\process\2011-2013高考理科第一批录取分数面板数据_v7.xlsx')
    pdataframe_science_first_v7['nearby'] = 0
    for ind in pdataframe_science_first_v7.index:
        exam_region = pdataframe_science_first_v7.loc[ind,'regioncode']
        college_region = pdataframe_science_first_v7.loc[ind,'高校所在地行政代码']
        if college_region in neighbors[exam_region]:
            pdataframe_science_first_v7.loc[ind, 'nearby'] = 1
    pdataframe_science_first_v7.to_excel(
        r'E:\cyberspace\worklot\college\dataset\process\2011-2013高考理科第一批录取分数面板数据_v8.xlsx')

    pdataframe_science_second_v7 = pd.read_excel(
        r'E:\cyberspace\worklot\college\dataset\process\2011-2013高考理科第二批录取分数面板数据_v7.xlsx')
    pdataframe_science_second_v7['nearby'] = 0
    for ind in pdataframe_science_second_v7.index:
        exam_region = pdataframe_science_second_v7.loc[ind, 'regioncode']
        college_region = pdataframe_science_second_v7.loc[ind, '高校所在地行政代码']
        if college_region in neighbors[exam_region]:
            pdataframe_science_second_v7.loc[ind, 'nearby'] = 1
    pdataframe_science_second_v7.to_excel(
        r'E:\cyberspace\worklot\college\dataset\process\2011-2013高考理科第二批录取分数面板数据_v8.xlsx')

    pdataframe_art_first_v7 = pd.read_excel(
        r'E:\cyberspace\worklot\college\dataset\process\2011-2013高考文科第一批录取分数面板数据_v7.xlsx')
    pdataframe_art_first_v7['nearby'] = 0
    for ind in pdataframe_art_first_v7.index:
        exam_region = pdataframe_art_first_v7.loc[ind, 'regioncode']
        college_region = pdataframe_art_first_v7.loc[ind, '高校所在地行政代码']
        if college_region in neighbors[exam_region]:
            pdataframe_art_first_v7.loc[ind, 'nearby'] = 1
    pdataframe_art_first_v7.to_excel(
        r'E:\cyberspace\worklot\college\dataset\process\2011-2013高考文科第一批录取分数面板数据_v8.xlsx')

    pdataframe_art_second_v7 = pd.read_excel(
        r'E:\cyberspace\worklot\college\dataset\process\2011-2013高考文科第二批录取分数面板数据_v7.xlsx')
    pdataframe_art_second_v7['nearby'] = 0
    for ind in pdataframe_art_second_v7.index:
        exam_region = pdataframe_art_second_v7.loc[ind, 'regioncode']
        college_region = pdataframe_art_second_v7.loc[ind, '高校所在地行政代码']
        if college_region in neighbors[exam_region]:
            pdataframe_art_second_v7.loc[ind, 'nearby'] = 1
    pdataframe_art_second_v7.to_excel(
        r'E:\cyberspace\worklot\college\dataset\process\2011-2013高考文科第二批录取分数面板数据_v8.xlsx')

if IS_ADD_LOCAL_PERGDP:
    local_province_real_perGDP = pd.read_excel(
        r'E:\cyberspace\worklot\college\dataset\raw\province_real_perGDP2.xlsx')

    pdataframe_science_first_v8 = pd.read_excel(
        r'E:\cyberspace\worklot\college\dataset\process\2011-2013高考理科第一批录取分数面板数据_v8.xlsx')
    pdataframe_science_first_v8_add_local_PERGDP = pd.merge(pdataframe_science_first_v8, local_province_real_perGDP, how='left',
                                                       on=['regioncode', '年份'])
    pdataframe_science_first_v8_add_local_PERGDP.to_excel(
        r'E:\cyberspace\worklot\college\dataset\process\2011-2013高考理科第一批录取分数面板数据_v9.xlsx')

    pdataframe_science_second_v8 = pd.read_excel(
        r'E:\cyberspace\worklot\college\dataset\process\2011-2013高考理科第二批录取分数面板数据_v8.xlsx')
    pdataframe_science_second_v8_add_local_PERGDP = pd.merge(pdataframe_science_second_v8, local_province_real_perGDP,
                                                            how='left',
                                                            on=['regioncode', '年份'])
    pdataframe_science_second_v8_add_local_PERGDP.to_excel(
        r'E:\cyberspace\worklot\college\dataset\process\2011-2013高考理科第二批录取分数面板数据_v9.xlsx')

    pdataframe_art_first_v8 = pd.read_excel(
        r'E:\cyberspace\worklot\college\dataset\process\2011-2013高考文科第一批录取分数面板数据_v8.xlsx')
    pdataframe_art_first_v8_add_local_PERGDP = pd.merge(pdataframe_art_first_v8, local_province_real_perGDP,
                                                            how='left',
                                                            on=['regioncode', '年份'])
    pdataframe_art_first_v8_add_local_PERGDP.to_excel(
        r'E:\cyberspace\worklot\college\dataset\process\2011-2013高考文科第一批录取分数面板数据_v9.xlsx')

    pdataframe_art_second_v8 = pd.read_excel(
        r'E:\cyberspace\worklot\college\dataset\process\2011-2013高考文科第二批录取分数面板数据_v8.xlsx')
    pdataframe_art_second_v8_add_local_PERGDP = pd.merge(pdataframe_art_second_v8, local_province_real_perGDP,
                                                        how='left',
                                                        on=['regioncode', '年份'])
    pdataframe_art_second_v8_add_local_PERGDP.to_excel(
        r'E:\cyberspace\worklot\college\dataset\process\2011-2013高考文科第二批录取分数面板数据_v9.xlsx')