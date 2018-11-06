# coding:utf-8
import numpy as np
import pandas as pd
import csv
import time
import sys
import os
import io
# sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')


root = os.path.join('G:', '金融数据')

def load_one_minute_seq(filename, start_time, end_time):
    '''
        读取股票一分钟的数据
    '''

    base_features = pd.read_csv(filename, header=0, sep=',')

    base_features['date_str'] = base_features['Date'] + ' '+ base_features['Time']
    base_features['date_num'] = base_features.date_str.map(lambda x:time.mktime(time.strptime(x, "%Y/%m/%d %H:%M")))
    columns = list(base_features.columns)

    item = columns.pop(-1)
    columns.insert(0, item)
    item = columns.pop(-1)
    columns.insert(0, item)

    base_features = base_features[columns]
    base_features = base_features.drop(columns=['Date', 'Time'])

    print( base_features.head(2))


def calc_single_factor(base_features, factor):
    if factor == 'SIZE': # 市值因子
        pass
    if factor == 'BETA': # 贝塔因子
        pass
    if factor == 'MOMENTUM': # 动量因子
        pass
    if factor == 'RESIDUAL VOLATILITY': # 残差波动因子
        pass
    if factor == 'NON-LINEAR-SIZE': # 非线性市值因子
        pass
    if factor == 'BOOK-TO-PRICE': # 账面市值比因子
        pass
    if factor == 'LIQUIDITY': # 流动性因子
        pass
    if factor == 'EARNING YEILD': # 盈利预期因子
        pass
    if factor == 'GROWTH': # 成长因子
        pass
    if factor == 'LEVERAGE': # 杠杆因子
        pass


def calc_factors(base_features, factor_list):
    for factor in factor_list:
        calc_single_factor(base_features, factor)


def load_multifactors_seq(filename):
    '''
        读取多因子数据
    '''
    facotrs = pd.read_csv(filename, header=0, sep=',')

    print(facotrs.head(2))


# load_one_minute_seq()
load_multifactors_seq(
    os.path.join(
        root, '多因子数据', 'barra_factor', 'barrafactor_20080102.csv'
    )
)
