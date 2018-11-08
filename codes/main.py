# coding:utf-8
import argparse
import sys
import os
sys.path.append(os.getcwd())

import codes.dataset
from codes.model.multifactors.alphamodel import Alphamodel 

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--factors_path', default='G:\\金融数据\\多因子数据', help='the root dir of factors resource')
    parser.add_argument('--prices_path', default='G:\\金融数据\\√股票一分钟', help='the root dir of prices resource')
    parser.add_argument('--start_year', default=2003, help='多因子数据的时间段位2008年到2017年')
    parser.add_argument('--end_year', default=2003, help='the root dir of prices resource')
    args = parser.parse_args()
    return args




def main(args):
    alpha = Alphamodel()
    alpha.calc_all_factors_IC_value(args.factors_path, args.prices_path, args.start_year, args.end_year)

if __name__ == '__main__':
    args = parse_args()
    main(args)