import pandas as pd
import os


def count_data(symbol: str, timestamp: str):
    print(f"{symbol} --- time: {timestamp}")
    dir_path = 'D:/GitHub/tryStock/data/' + symbol.replace("/", "") + '/' + timestamp + '/'
    file_list = os.listdir(dir_path)
    total_data = 0
    count = [0, 0, 0, 0]
    for fname in file_list:
        # 读取 Excel 文件
        df = pd.read_csv(dir_path + fname)
        total_data += df.shape[0]
        # 统计值等于 3 的数量
        count[0] += df[df['prediction'] == 0].shape[0]
        count[1] += df[df['prediction'] == 1].shape[0]
        count[2] += df[df['prediction'] == 2].shape[0]
        count[3] += df[df['prediction'] == 3].shape[0]

    print(f"RISE_DROP: {(count[0]/total_data * 100):.2f}%")
    print(f"NORISE_DROP: {(count[1]/total_data * 100):.2f}%")
    print(f"NORISE_NODROP: {(count[2]/total_data * 100):.2f}%")
    print(f"RISE_NODROP: {(count[3]/total_data * 100):.2f}%")


crypto_lst = ['BTC/USDT', 'ETH/USDT', 'BNB/USDT', 'XRP/USDT', 'ADA/USDT', 'DOGE/USDT', 'MATIC/USDT', 'SOL/USDT']
time_frame = ['5m', '15m', '30m']


if __name__ == '__main__':
    for s in crypto_lst:
        for t in time_frame:
            count_data(s, t)
        print('---------------------------------------------------')
