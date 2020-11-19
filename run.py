#!encoding=utf8

from config import AccountConfig as Account
from lib.mt5lib import Mt5Client




if __name__ == "__main__":
    client = Mt5Client(account_number=Account.username, password=Account.password, server_name=Account.server)
    client.download_data("GBPUSD", "M1", "2018-11-19", "2020-11-19")
    client.shutdown()