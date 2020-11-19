#!encoding=utf8

from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import MetaTrader5 as mt5
import pytz, os, csv


class Mt5Client:
    M1 = 'M1'
    M5 = 'M5'
    M15 = 'M15'
    M30 = 'M30'
    H1 = 'H1'
    H4 = 'H4'
    D1 = 'D1'

    def __init__(self, account_number, password, server_name, mt5_path=None):
        """初始化MT5客户端

        Args:
            account_number (int): 登录MT5账户号码
            password (string): 登录MT5密码
            server_name (string): 登录服务器名称
            mt5_path (string, optional): MT5 客户端路径，如果不指定自动寻找. Defaults to None.
        """
        # 连接到MetaTrader 5
        if mt5_path:
            if not mt5.initialize(mt5_path):
                print("MT5 路径：{}".format(mt5_path))
                print("初始化 MT5 客户端失败")
                mt5.shutdown()
                exit(0)
        else:
            if not mt5.initialize():
                print("初始化 MT5 客户端失败")
                print("请指定MT5路径后在尝试")
                mt5.shutdown()
                exit(0)

        mt5_path = mt5.terminal_info()[19]

        # 请求连接状态和参数
        print("初始化 MT5 客户端成功，路径：{}".format(mt5_path))
        # 获取有关MetaTrader 5版本的数据
        # print(mt5.version())

        authorized = mt5.login(account_number, password, server_name)
        if authorized:
            print("用户信息如下：")
            account_info_dict = mt5.account_info()._asdict()
            print("name   = {}".format(account_info_dict['name']))
            print("login  = {}".format(account_info_dict['login']))
            print("server = {}".format(account_info_dict['server']))

    def shutdown(self):
        # 断开与MetaTrader 5的连接
        print("关闭 MT5 客户端")
        mt5.shutdown()

    def download_data(self, symbol, timeframe, start_time, end_time):
        """下载指定品种历史数据

        Args:
            symbol (string): 品种名称
            timeframe (mt5.TIMEFRAME): mt5时间框架,eg mt5.TIMEFRAME_M1
            start_time (string): 下载历史记录的开始时间,eg 2020-01-01
            end_time (string): 下载历史记录的结束时间,eg 2020-01-01
        Return:
            pd.DataFrame
        """
        mt5_timeframe = mt5.TIMEFRAME_M1
        if timeframe == "M1":
            mt5_timeframe = mt5.TIMEFRAME_M1
        elif timeframe == 'M5':
            mt5_timeframe = mt5.TIMEFRAME_M5
        elif timeframe == 'M15':
            mt5_timeframe = mt5.TIMEFRAME_M15
        elif timeframe == 'M30':
            mt5_timeframe = mt5.TIMEFRAME_M30
        elif timeframe == 'H1':
            mt5_timeframe = mt5.TIMEFRAME_H1
        elif timeframe == 'H4':
            mt5_timeframe = mt5.TIMEFRAME_H4
        elif timeframe == 'D1':
            mt5_timeframe = mt5.TIMEFRAME_D1
        # set time zone to UTC
        timezone = pytz.timezone("Etc/UTC")
        # 将字符串时间格式化成列表 2020-01-01 => [2020, 1, 1]
        start_time_list = start_time.split('-')
        end_time_list = end_time.split('-')
        start_time_list_int = list(map(int, start_time_list))
        end_time_list_int = list(map(int, end_time_list))        
        utc_from = datetime(start_time_list_int[0], start_time_list_int[1], start_time_list_int[2], tzinfo=timezone)
        utc_to = datetime(end_time_list_int[0], end_time_list_int[1], end_time_list_int[2], tzinfo=timezone)
        # 获取K线信息
        print("开始下载 {0} 周期 {1} 开始时间 {2}- 结束时间 {3} 的历史数据".format(symbol, timeframe, start_time, end_time))
        rates = mt5.copy_rates_range(symbol, mt5_timeframe, utc_from, utc_to)
        print("历史数据下载完成")
        result = [["symbol", "timestamp", "open", "high", "low", "close", "spread"]]
        for rate in rates:
            value = [symbol]
            value += [rate[0],rate[1],rate[2],rate[3],rate[4],rate[6]]
            result.append(value)

        work_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.abspath(os.path.join(work_dir, '..', 'data', symbol, timeframe))
        if not os.path.exists(csv_path):
            print("目录 {0} 不存在, 自动创建目录".format(csv_path))
            os.makedirs(csv_path)

        csv_filename = "{0}_{1}_{2}_{3}.csv".format(symbol, timeframe, ''.join(start_time_list), ''.join(end_time_list)) 
        csv_filepath = os.path.join(csv_path, csv_filename)
        if not os.path.exists(csv_filepath):
            print("开始将历史数据写入csv文件 {0}".format(csv_filepath))
            with open(csv_filepath, 'w', newline='') as fp:
                csv_writer = csv.writer(fp)
                csv_writer.writerows(result)
            print("历史数据写入成功")
        else:
            print("历史数据已经存在路径 {0}".format(csv_filepath))
        
        rates_frame = pd.DataFrame(rates)
        return rates_frame

if __name__ == "__main__":
    client = Mt5Client(account_number=6042573, password='aqwrds7v', server_name='Swissquote-Server')
    client.download_data("EURUSD", Mt5Client.M1, "2020-11-01", "2020-11-10")
    client.shutdown()

    


