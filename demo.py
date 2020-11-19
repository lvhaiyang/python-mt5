#!encoding=utf8

from numpy.lib.twodim_base import mask_indices
from config import Account
from lib.mt5lib import Mt5Client
from lib.indicator import AppliedPrice
import pandas as pd
# 需要哪些指标就导入哪些指标
from lib.indicator import iSMA

def sma_test(data):
    rates_frame = data[0]
    sma1 = data[1]
    sma2 = data[2]
    # 根据历史数据计算指标
    sma1_frame = iSMA(rates_frame, sma1, AppliedPrice.close)
    sma2_frame = iSMA(sma1_frame, sma2, AppliedPrice.close)

    total_profit = 0 # 计算总盈利情况
    total_trade_num = 0 # 计算总交易次数
    open_price = 0 # 建仓价格
    close_price = 0 # 平仓价格
    take_profit_num = 0 # 盈利次数
    stop_loss_num = 0 # 亏损次数
    trade_status = 0 # 交易状态 0 空仓， 1 持有多单， 2 持有空单
    print('开始回测')
    for index, data in sma2_frame.iterrows():
        if index == 0:
            continue
        time = data['time']
        close = data['close']
        sma14 = data['SMA{}'.format(sma1)]
        sma21 = data['SMA{}'.format(sma2)]

        # 确保两个均线都有值
        if sma14 == 0 or sma21 == 0:
            continue

        if sma14 > sma21 and trade_status == 0:
            open_price = close
            trade_status = 1
            # print('{0} 建仓多单 价格{1}'.format(time, open_price))
        elif trade_status == 1:
            close_price = close
            trade_status = 0
            total_trade_num += 1
            total_profit += close_price - open_price
            if close_price - open_price >= 0:
                take_profit_num += 1
            else:
                stop_loss_num += 1

            # print('{2} 平仓多单 价格 {0}, 盈利 {1}'.format(close_price, close_price - open_price, time))

    print('\n=====================================================')
    print('参数对 sma1 = {} ; sma2 = {}'.format(sma1, sma2))
    print("总计交易 {0} 笔, 总盈利 {1}, 盈利交易 {2}, 亏损交易 {3}".format(total_trade_num, total_profit, take_profit_num, stop_loss_num))

if __name__ == "__main__":

    # 策略配置
    symbol = 'EURUSD'
    timeframe = 'M1'
    start_time = '2020-01-18'
    finish_time = '2020-11-19'
    # indicators 格式，每个指标是一个列表， [指标名称， 参数起始值， 终止值， 每增加值]
    iSMA_1 = [50, 101, 50]
    iSMA_2 = [100, 201, 100]

    # 连接MT5获取历史数据
    client = Mt5Client(account_number=Account.username, password=Account.password, server_name=Account.server)
    rates_frame = client.download_data(symbol, timeframe, start_time, finish_time)
    # 时间戳转成年月日格式
    rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s')
    client.shutdown()

    # sma_test(rates_frame, 100, 200)

    # # 生成参数组合
    params = []
    for i in range(iSMA_1[0], iSMA_1[1], iSMA_1[2]):
        for j in range(iSMA_2[0], iSMA_2[1], iSMA_2[2]):
            params.append((rates_frame, i, j))
    
    print(params)

    from multiprocessing import Pool
    pool = Pool()
    pool.map(sma_test, params)
    pool.close()
    pool.join()

