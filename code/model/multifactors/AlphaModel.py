import pandas
import os
import alphalens
from code import dataset

# TODO:这里其实应该写成一个类的形式把这些函数都丢到alpha modle类中

def calc_single_factor_IC_value(factor_path, prices_frame, start_year, end_year):
    '''
        IC的具体值：
            可以为'皮尔逊相关系数'，所以IC就是price 和 因子的相关系数，称为normal IC
            可以为'斯皮尔曼相关系数'，称为Rank IC
        tips:
            factor的时间一定要和price的时间对应上，不然无法计算
        params:
            factor_path是存储指定factor的众多csv文件的文件夹
            price_frame是已经做好的price结构
    '''
    factor = dataset.load_single_factor(factor_path, start_year, end_year)
    prices = prices_frame

    print('start calculate IC value')
    factor_data = alphalens.utils.get_clean_factor_and_forward_returns(factor, 
                                                                    prices, 
                                                                    quantiles=5,
                                                                    # bins=None,
                                                                    # groupby=ticker_sector,
                                                                    # groupby_labels=sector_names,
                                                                    periods=[1,5,10])

    # mean_return_by_q, std_err_by_q = alphalens.performance.mean_return_by_quantile
    # TODO:groupby和groupby_label是什么东西
    print('calculate IC value finished')
    return factor_data


def calc_all_factors_IC_value(facotrs_path, prices_path, start_year, end_year):
    factors_dirs = os.listdir(facotrs_path)

    prices_frame = dataset.load_period_prices(prices_path, start_year, end_year)

    factors_data_dict = {}
    for factors_dir in factors_dirs:
        if factors_dir.split('_')[0] == 'barra':
            # TODO:计算barra facotrs
            pass
        else:
            factors = os.listdir(os.path.join(factors_dir, 'Factor'))
            for factor in factors:
                factor_data = calc_single_factor_IC_value(os.path.join(factors_dir, 'Factor', factor), prices_frame, start_year, end_year)
                factors_data_dict[factor] = factor_data
    # TODO:各个factor的IC值(IC其实还没算出来，只是factor_data可以用来算IC了)都计算出来，如何选择和比较


