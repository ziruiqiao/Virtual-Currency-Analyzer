from enum import Enum
from pathlib import Path
import ccxt

xP_KEY = 'lLQSh4yYChRMsBDk'
xP_SECRET = 'ckt0sa12fHHzBIya1zk7Ylb4bNZrDKDr'


# phemex = ccxt.phemex({
#     'enableRateLimit': True,
#     'apiKey': xP_KEY,
#     'secret': xP_SECRET
# })


class TFrame(Enum):
    # t1M = ('1m', 150)
    t5M = ('5m', 30)
    t15M = ('15m', 10)
    t30M = ('30m', 5)

    def __init__(self, name: str, size: int):
        self._name = name
        self._size = size

    @property
    def name(self):
        return self._name

    @property
    def size(self):
        return self._size


def get_project_root_path() -> Path:
    """
    get the root path of this project
    :return: path of the root dir
    """
    return Path(__file__).parent


crypto_lst = ['BTC/USDT', 'ETH/USDT', 'BNB/USDT', 'XRP/USDT', 'ADA/USDT', 'DOGE/USDT', 'MATIC/USDT', 'SOL/USDT']
time_frame = [TFrame.t5M, TFrame.t15M, TFrame.t30M]
