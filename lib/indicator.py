#!encoding=utf8

import pandas as pd

class AppliedPrice:
    open = 'open'
    close = 'close'
    high = 'high'
    low = 'low'


def iSMA(rates_frame, sma_period, applied_price):
    """简单移动平均线技术指标
    Args:
        rates_frame (pandas.DataFrame): pandas.DataFrame 价格数据
        sma_period (int): 平均线计算周期
        applied_price (string): 价格或处理器类型, AppliedPrice 中的枚举值
    return:
        rates_frame (pandas.DataFrame) 价格数据，简单移动平均线数据
    """
    rates_frame['SMA{0}'.format(sma_period)] = rates_frame[applied_price].rolling(sma_period, min_periods=sma_period).mean()  
    return rates_frame

def iEMA(rates_frame, ema_period, applied_price):
    """指数移动平均线技术指标
    Args:
        rates_frame (pandas.DataFrame): pandas.DataFrame 价格数据
        ema_period (int): 平均线计算周期
        applied_price (string): 价格或处理器类型, AppliedPrice 中的枚举值
    return:
        rates_frame (pandas.DataFrame) 价格数据，指数移动平均线数据
    """
    rates_frame['EMA{0}'.format(ema_period)] = rates_frame[applied_price].ewm(ema_period, span=ema_period).mean()  
    return rates_frame

def iBands(rates_frame, bands_period, deviation, applied_price):
    """保力加通道技术指标, 布林带
    Args:
        rates_frame (pandas.DataFrame): pandas.DataFrame 价格数据
        bands_period (int): 平均线计算周期
        deviation (int): 标准差数
        applied_price (string): 价格或处理器类型, AppliedPrice 中的枚举值
    return:
        rates_frame (pandas.DataFrame) 价格数据，布林带数据
    """
    # 计算均线
    rates_frame['median'] = rates_frame[applied_price].rolling(bands_period, min_periods=bands_period).mean()  
    # 计算上轨、下轨道
    rates_frame['std'] = rates_frame[applied_price].rolling(bands_period, min_periods=bands_period).std(ddof=0)  # ddof代表标准差自由度
    rates_frame['upper'] = rates_frame['median'] + deviation * rates_frame['std']
    rates_frame['lower'] = rates_frame['median'] - deviation * rates_frame['std']

    return rates_frame