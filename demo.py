#!encoding=utf8

from config import Account
from lib.mt5lib import Mt5Client
from lib.indicator import AppliedPrice
import pandas as pd
# 需要哪些指标就导入哪些指标
from lib.indicator import iSMA


if __name__ == "__main__":
    # 连接MT5获取历史数据
    client = Mt5Client(account_number=Account.username, password=Account.password, server_name=Account.server)
    rates_frame = client.download_data("EURUSD", Mt5Client.M1, "2020-01-18", "2020-11-19")
    client.shutdown()

    # 根据历史数据计算指标
    sma14_frame = iSMA(rates_frame, 100, AppliedPrice.close)
    sma21_frame = iSMA(sma14_frame, 200, AppliedPrice.close)
    # 时间戳转
    sma21_frame['time']=pd.to_datetime(sma21_frame['time'], unit='s')

    total_profit = 0 # 计算总盈利情况
    total_trade_num = 0 # 计算总交易次数
    open_price = 0 # 建仓价格
    close_price = 0 # 平仓价格
    take_profit_num = 0 # 盈利次数
    stop_loss_num = 0 # 亏损次数
    trade_status = 0 # 交易状态 0 空仓， 1 持有多单， 2 持有空单
    print('开始回测')
    for index, data in sma21_frame.iterrows():
        if index == 0:
            continue
        time = data['time']
        close = data['close']
        sma14 = data['SMA100']
        sma21 = data['SMA200']

        # 确保两个均线都有值
        if sma14 == 0 or sma21 == 0:
            continue

        if sma14 > sma21 and trade_status == 0:
            open_price = close
            trade_status = 1
            print('{0} 建仓多单 价格{1}'.format(time, open_price))
        elif trade_status == 1:
            close_price = close
            trade_status = 0
            total_trade_num += 1
            total_profit += close_price - open_price
            if close_price - open_price >= 0:
                take_profit_num += 1
            else:
                stop_loss_num += 1

            print('{2} 平仓多单 价格 {0}, 盈利 {1}'.format(close_price, close_price - open_price, time))

    
    print("总计交易 {0} 笔, 总盈利 {1}, 盈利交易 {2}, 亏损交易 {3}".format(total_trade_num, total_profit, take_profit_num, stop_loss_num))

    