# coding:utf-8
import numpy as np
import pandas as pd
import csv
import time
import sys
import os
import alphalens
import matplotlib.pyplot as plt

root = os.path.join('G:', '金融数据')

def load_one_minute_seq(filename, start_time, end_time):
    '''
        读取股票一分钟的数据
    '''

    base_features = pd.read_csv(filename, header=0, sep=',')

    base_features['date_str'] = base_features['date'] + ' '+ base_features['Time']
    base_features['date_num'] = base_features.date_str.map(lambda x:time.mktime(time.strptime(x, "%Y/%m/%d %H:%M")))
    columns = list(base_features.columns)

    item = columns.pop(-1)
    columns.insert(0, item)
    item = columns.pop(-1)
    columns.insert(0, item)

    base_features = base_features[columns]
    base_features = base_features.drop(columns=['date', 'Time'])

    print( base_features.head(2))


def load_barra_factors():
    pass


def load_single_factor(dirpath, start_year, end_year, regenerate=True):
    print('loading factors ...')
    if regenerate == False:
        factor_frame = pd.read_csv(os.path.join('code', 'data', 'factorframe-%s.csv' %(dirpath.split('\\')[-1])), header=0, sep=',')

    else:
        files = os.listdir(dirpath)
        for file in files:
            if int(file.split('-')[0]) < start_year or int(file.split('-')[0]) > end_year:
                continue
                # 只读取指定日期内的数据

            factor4stocks = pd.read_csv(os.path.join(dirpath ,file), header=0, sep=',')
            factor4stocks['date'] = [file.split('.')[0] for i in range(len(factor4stocks))]
            if 'factor_frame' not in vars():
                factor_frame = factor4stocks
            else:
                factor_frame = pd.concat([factor_frame, factor4stocks])
        factor_frame = factor_frame[['date', 'stock', 'factor_value']]
        factor_frame['date'] = pd.to_datetime(factor_frame['date'])
        factor_frame.set_index('date', inplace=True)
        factor_frame = factor_frame.stack()
        factor_frame.index = factor_frame.index.set_names(['date', 'stock'])
        factor_frame.to_csv(os.path.join('code', 'data', 'factorframe-%s.csv' %(dirpath.split('\\')[-1])), index=True, sep=',')

    print('load factors finished')
    print('-'*64)
    return factor_frame


def load_period_prices(dirpath, start_year, end_year, which_price='close', regenerate=True):
    print('loading prices ...')
    if regenerate == False:
        if os.path.exists(os.path.join('codes', 'data', which_price + '-prices-' + str(start_year) + '-' + str(end_year) + '.csv')):
            prices_frame = pd.read_csv(os.path.join('codes', 'data', which_price + '-prices-' + str(start_year) + '-' + str(end_year) + '.csv'))
        else:
            regenerate = True
            print('there is not price_frame file existed, generating ...')

    if regenerate == True:
        total_files_num = 0
        for year in range(start_year, end_year + 1):
            single_year_pricesdir = os.path.join(dirpath, 'Stk_1F_' + str(year))
            files = os.listdir(single_year_pricesdir)
            total_files_num = total_files_num + len(files)

        for year in range(start_year, end_year + 1):
            single_year_pricesdir = os.path.join(dirpath, 'Stk_1F_' + str(year))
            
            files = os.listdir(single_year_pricesdir)
            stocks = [file.split('.')[0] for file in files]

            for index, file in enumerate(files):
                print(index, '/', total_files_num, end='\r', flush=True)
                price4singlestock = pd.read_csv(os.path.join(single_year_pricesdir, file), header=None)
                price4singlestock.columns = ['date', 'time', 'open', 'high', 'low', 'close', 'volume', 'amount']
                price4singlestock = price4singlestock[ price4singlestock['time'] == '15:00' ]
                price4singlestock = price4singlestock[['date', which_price]]
                price4singlestock= price4singlestock.rename(columns={which_price: file.split('.')[0]})

                if 'single_year_prices_frame' not in vars():
                    single_year_prices_frame = price4singlestock
                else:
                    # pd.DataFrame.merge()
                    single_year_prices_frame = pd.merge(single_year_prices_frame, price4singlestock, how='inner', on='date')
            if 'prices_frame' not in vars():
                prices_frame = single_year_prices_frame
            else:
                prices_frame = pd.concat([prices_frame, single_year_prices_frame])

        prices_frame['date'] = pd.to_datetime(prices_frame['date'])
        prices_frame = prices_frame.set_index(['date'], inplace=True)
        prices_frame.to_csv(os.path.join('codes', 'data', which_price + '-prices-' + str(start_year) + '-' + str(end_year) + '.csv'),
            index = True,
            sep = ','
        )
    print('load prices finished')
    print('-'*64)
    return prices_frame
        # price_frames.to_csv(os.path.join('code', 'data', 'priceframe-%s.csv' %(dirpath.split('\\')[-1])), index=True, sep=',')



def delet_extremes():
    # 去极值
    pass


def normalize():
    # 标准化
    pass


def datapreprocess():
    pass



def calc_IR_value():
    # 信息比率（IR），即超额收益的均值与标准差之比
    pass



# def main():
#     calc_IC_value()


# if __name__ == '__main__':
#     main()
