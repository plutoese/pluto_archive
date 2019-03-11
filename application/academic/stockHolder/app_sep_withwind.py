# coding = UTF-8

import os
import numpy as np
import pandas as pd

PROJECT_DATA_PATH = r'E:\datahouse\projectdata\shareholder'

# 参数设置
# 提炼数据到新Excel文件
STEP1 = False
# 添加Wind行业代码
STEP2 = False
# 匹配wind行业代码
STEP3 = False
# 匹配行业
STEP4 = False
# 匹配原数据
STEP5 = True

if STEP1:
    file_path = os.path.join(PROJECT_DATA_PATH,'stage_three_full_table.xlsx')
    data_table = pd.read_excel(file_path)

    current_data_table = data_table.loc[:,
                         ['上市公司代码_ComCd','股东上市公司代码_SHComCd']]

    current_data_table.to_excel(os.path.join(PROJECT_DATA_PATH, 'to_check_code_dframe.xlsx'))

if STEP2:
    file_path = os.path.join(PROJECT_DATA_PATH, 'windcode.xlsx')
    data_table = pd.read_excel(file_path,dtype={'stockcode':str, 'windindustrycode':str})
    print(data_table)

    stock_code = [''.join(['C',item]) for item in data_table.loc[:,'stockcode']]
    stock_wind_industry = data_table['windindustrycode']

    stock_industry_dict = dict(zip(stock_code,stock_wind_industry))

if STEP3:
    to_check_file_path = os.path.join(PROJECT_DATA_PATH, 'to_check_code_dframe.xlsx')
    to_check_data_table = pd.read_excel(to_check_file_path)

    wind1 = to_check_data_table['上市公司代码_ComCd'].apply(lambda x: stock_industry_dict.get(x))
    wind2 = to_check_data_table['股东上市公司代码_SHComCd'].apply(lambda x: stock_industry_dict.get(x))

    to_check_data_table['comcd_wind_industry_code'] = wind1
    to_check_data_table['shcomcd_wind_industry_code'] = wind2

    to_check_data_table.to_excel(os.path.join(PROJECT_DATA_PATH, 'to_check_code_dframe_with_wind.xlsx'))

if STEP4:
    up_and_down_industry = {'25101010': ('25102010', '25102020'),
                            '25101020': ('25102010', '25102020')}
    down_and_up_industry = {'25102010': ('25101010', '25101020'),
                            '25102020': ('25101010', '25101010')}

    to_check_with_wind_file_path = os.path.join(PROJECT_DATA_PATH, 'to_check_code_dframe_with_wind.xlsx')
    to_check_with_wind_data_table = pd.read_excel(to_check_with_wind_file_path,
                                                  dtype={'上市公司代码_ComCd':str, '股东上市公司代码_SHComCd':str,
                                                         'comcd_wind_industry_code':str, 'shcomcd_wind_industry_code':str})

    count = 0
    for ind in to_check_with_wind_data_table.index:
        found_code = to_check_with_wind_data_table.loc[ind,'comcd_wind_industry_code']
        if found_code in up_and_down_industry:
            print(ind, found_code, up_and_down_industry)
            match_code = to_check_with_wind_data_table.loc[ind,'shcomcd_wind_industry_code']
            if match_code in up_and_down_industry[found_code]:
                count += 1
                to_check_with_wind_data_table.loc[ind,'up_hold_down'] = 1
    print(count)

    count2 = 0
    for ind in to_check_with_wind_data_table.index:
        found_code = to_check_with_wind_data_table.loc[ind, 'comcd_wind_industry_code']
        if found_code in down_and_up_industry:
            print(ind, found_code, down_and_up_industry)
            match_code = to_check_with_wind_data_table.loc[ind, 'shcomcd_wind_industry_code']
            if match_code in down_and_up_industry[found_code]:
                count2 += 1
                to_check_with_wind_data_table.loc[ind, 'down_hold_up'] = 1
    print(count2)

    to_check_with_wind_data_table.to_excel(os.path.join(PROJECT_DATA_PATH, 'to_check_code_dframe_with_wind_dummy.xlsx'))

if STEP5:
    file_path = os.path.join(PROJECT_DATA_PATH, 'stage_three_full_table.xlsx')
    data_table = pd.read_excel(file_path)

    file_path = os.path.join(PROJECT_DATA_PATH, 'to_check_code_dframe_with_wind.xlsx')
    dframe_with_wind = pd.read_excel(file_path)

    file_path = os.path.join(PROJECT_DATA_PATH, 'to_check_code_dframe_with_wind_dummy.xlsx')
    dframe_with_dummy = pd.read_excel(file_path)

    data_table['comcd_wind_industry_code'] = dframe_with_wind['comcd_wind_industry_code']
    data_table['shcomcd_wind_industry_code'] = dframe_with_wind['shcomcd_wind_industry_code']
    data_table['up_hold_down'] = dframe_with_dummy['up_hold_down']

    data_table.to_excel(os.path.join(PROJECT_DATA_PATH, 'stage_four_full_table.xlsx'))