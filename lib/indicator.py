#!encoding=utf8

import pandas as pd

class AppliedPrice:
    open = 'open'
    close = 'close'
    high = 'high'
    low = 'low'

def iBands(rates, bands_period, deviation, applied_price):
    """保力加通道技术指标, 布林带

    Args:
        rates (): Mt5Client 类中 download_data 返回值
        bands_period (int): 平均线计算周期
        deviation (int): 标准差数
        applied_price (string): 价格或处理器类型, AppliedPrice 中的枚举值
    
    return:
        rates_frame (pandas.DataFrame) 价格数据，布林带数据
    """
    rates_frame = pd.DataFrame(rates)
    # 计算均线
    rates_frame['median'] = rates_frame[applied_price].rolling(bands_period, min_periods=bands_period).mean()  
    # 计算上轨、下轨道
    rates_frame['std'] = rates_frame[applied_price].rolling(bands_period, min_periods=bands_period).std(ddof=0)  # ddof代表标准差自由度
    rates_frame['upper'] = rates_frame['median'] + deviation * rates_frame['std']
    rates_frame['lower'] = rates_frame['median'] - deviation * rates_frame['std']

    return rates_frame