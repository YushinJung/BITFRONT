class COINPAIRS:
    BTC_MARKET = ['ETH.BTC', 'LTC.BTC', 'BCH.BTC', 'LN.BTC']
    USDT_MARKET = ['ETH.USDT', 'BTC.USDT', 'LTC.USDT', 'BCH.USDT', 'LN.USDT']

    def all(self):
        ALL_MARKET = self.BTC_MARKET + self.USDT_MARKET
        return ALL_MARKET

    def check_exist(self, coinpair):
        for pair in self.all():
            if pair == coinpair:
                return True
        else:
            return False
