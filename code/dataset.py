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


def load_factors(dirpath, regenerate=True):
    print('loading factors ...')
    if regenerate == False:
        factor_frame = pd.read_csv(os.path.join('code', 'data', 'factorframe-%s.csv' %(dirpath.split('\\')[-1])), header=0, sep=',')

    else:
        files = os.listdir(dirpath)[:4]
        for index, file in enumerate(files):
            factor4stocks = pd.read_csv(os.path.join(dirpath ,file), header=0, sep=',')
            factor4stocks['date'] = [file.split('.')[0] for i in range(len(factor4stocks))]
            if 'factor_frame' not in vars():
                factor_frame = factor4stocks
            else:
                factor_frame = pd.concat([factor_frame, factor4stocks])
            # print(index, '/', len(files), end='\r', flush=True)
            # factor4stocks = pd.read_csv(os.path.join(dirpath ,file), header=0, sep=',')
            # if 'factor_frame' not in vars():
            #     # 根据第一个文件的股票，建立数据结构
            #     dates = ['-'.join(f.split('.')[0].split('/')) for f in files]
            #     stocks = factor4stocks['stock'].values.tolist()
            #     true_stocks = []
            #     for stock in stocks:
            #         stock = stock.split('.')
            #         stock.reverse()
            #         stock = ''.join(stock)
            #         true_stocks.append(stock)
            #     stocks = true_stocks
            #     iterables = [dates, stocks]
            #     multi_index = pd.MultiIndex.from_product(iterables, names=['date', 'stocks'])
            #     factor_frame = pd.DataFrame([np.NaN for i in range(len(dates)*len(stocks))], index = multi_index, columns=['factor'])

            # for No, stock in enumerate(stocks):
            #     factor_frame.loc[file.split('.')[0], stock] = factor4stocks.loc[No, 'factor_value']
        factor_frame = factor_frame[['date', 'stock', 'factor_value']]
        factor_frame.set_index('date', inplace=True)
        print(factor_frame.head())
        print('-'*64)
        factor_frame = factor_frame.stack()
        factor_frame.index = factor_frame.index.set_names(['date', 'stock'])
        print(factor_frame.head())
        exit()
        factor_frame.to_csv(os.path.join('code', 'data', 'factorframe-%s.csv' %(dirpath.split('\\')[-1])), index=True, sep=',')

    print('load factors finished')
    print('-'*64)
    return factor_frame


def load_prices(dirpath, which_price='Close', regenerate=True):
    '''
        股票一分钟中的数据每一列对应date	Time	Open	High	Low	Close	Volume	Amount

        params:
            which_price: Close or Open，选择开盘或者收盘价来计算收益率
        
    '''

    print('loading prices ...')

    if regenerate == False:
        price_frame = pd.read_csv(os.path.join('code', 'data', 'priceframe-%s.csv' %(dirpath.split('\\')[-1])), header=0, sep=',')

    else:
        files = os.listdir(dirpath)[:4]
        stocks = [file.split('.')[0] for file in files]
        for index, file in enumerate(files):
            print(index, '/', len(files), end='\r', flush=True)
            price4singlestock = pd.read_csv(os.path.join(dirpath, file), header=None)
            price4singlestock.columns = ['date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Amount']
            price4singlestock = price4singlestock[ price4singlestock['Time'] == '15:00' ]
            price4singlestock = price4singlestock[['date', which_price]]
            price4singlestock= price4singlestock.rename(columns={which_price: file.split('.')[0]})

            if 'price_frame' not in vars():
                price_frame = price4singlestock
            else:
                # pd.DataFrame.merge()
                price_frame = pd.merge(price_frame, price4singlestock, how='inner', on='date')
        price_frame['date'] = price_frame['date'].apply(lambda x: '-'.join(x.split('/')))
        price_frame = price_frame.set_index(['date'])
        price_frame.to_csv(os.path.join('code', 'data', 'priceframe-%s.csv' %(dirpath.split('\\')[-1])), index=True, sep=',')

    print('load prices finished')
    print('-'*64)
    return price_frame


def delet_extremes():
    # 去极值
    pass


def normalize():
    # 标准化
    pass


def datapreprocess():
    
    pass


def calc_IC_value():
    # IC的具体值：
    #     可以为'皮尔逊相关系数'，所以IC就是price 和 因子的相关系数，称为normal IC
    #     可以为'斯皮尔曼相关系数'，称为Rank IC
    factor = load_factors('G:\金融数据\多因子数据\consensus_factor\Factor\PNP')
    prices = load_prices('G:\金融数据\√股票一分钟\Stk_1F_2003')
    # ticker_sector, factor = load_factors('G:\金融数据\多因子数据\consensus_factor\Factor\PNP', regenerate=False)
    # prices = load_prices('G:\金融数据\√股票一分钟\Stk_1F_2003', regenerate=False)
    print('start calculate IC value')
    print(factor.head())
    print(prices.head())

    factor_data = alphalens.utils.get_clean_factor_and_forward_returns(factor, 
                                                                    prices, 
                                                                    quantiles=5,
                                                                    # bins=None,
                                                                    # groupby=ticker_sector,
                                                                    # groupby_labels=sector_names,
                                                                    periods=[1,5,10])

    # mean_return_by_q, std_err_by_q = alphalens.performance.mean_return_by_quantile
    # TODO:groupby和groupby_label是什么东西
    print(factor_data.head())
    print(factor_data.dtypes)
    print(factor_data.columns)

def calc_IR_value():
    # 信息比率（IR），即超额收益的均值与标准差之比
    pass



def main():
    calc_IC_value()


if __name__ == '__main__':
    main()
