import argparse
import dataset

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--facotrs_path', default='G:\金融数据\多因子数据', help='the root dir of factors resource')
    parser.add_argument('--prices_path', default='G:\金融数据\√股票一分钟', help='the root dir of prices resource')
    args = parser.parse_args()
    return args


def main(args):
    dataset.calc_IC_value()


if __name__ == '__main__':
    args = parse_args()
    main(args)