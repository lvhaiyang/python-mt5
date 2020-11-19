#!encoding=utf8

from config import Account
from lib.mt5lib import Mt5Client
from lib.indicator import AppliedPrice, iBands




if __name__ == "__main__":
    client = Mt5Client(account_number=Account.username, password=Account.password, server_name=Account.server)
    rates = client.download_data("GBPUSD", Mt5Client.M1, "2020-11-18", "2020-11-19")
    client.shutdown()

    bands_frame = iBands(rates, 20, 2, AppliedPrice.close)

    print(bands_frame.head(50))


    