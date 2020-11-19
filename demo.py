#!encoding=utf8

from config import Account
from lib.mt5lib import Mt5Client
from lib.indicator import AppliedPrice
# 需要哪些指标就导入哪些指标
from lib.indicator import iSMA


if __name__ == "__main__":
    # 连接MT5获取历史数据
    client = Mt5Client(account_number=Account.username, password=Account.password, server_name=Account.server)
    rates_frame = client.download_data("EURUSD", Mt5Client.M1, "2020-11-18", "2020-11-19")
    client.shutdown()

    # 根据历史数据计算指标
    sma14_frame = iSMA(rates_frame, 14, AppliedPrice.close)
    sma21_frame = iSMA(sma14_frame, 21, AppliedPrice.close)
    print(sma21_frame.head(50))


    