import argparse
import sys
import os

from code import dataset
from code.model.multifactors import alphamodel

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--facotrs_path', default='G:\金融数据\多因子数据', help='the root dir of factors resource')
    parser.add_argument('--prices_path', default='G:\金融数据\√股票一分钟', help='the root dir of prices resource')
    parser.add_argument('--start_year', default=2003, help='多因子数据的时间段位2008年到2017年')
    parser.add_argument('--end_year', default=2003, help='the root dir of prices resource')
    args = parser.parse_args()
    return args




def main(args):
    alphamodel.calc_all_factors_IC_value(args.factors_path, args.prices_path, args.start_year, args.end_year)

if __name__ == '__main__':
    args = parse_args()
    main(args)