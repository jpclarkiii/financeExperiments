import os
import logging

LOGDIR=os.getenv('LOGDIR')
logFN="/".join([LOGDIR,'fundamentals.log'])
logging.basicConfig(filename=logFN, level=logging.DEBUG,
                    format='%(levelname)s:%(asctime)s %(message)s')

class ExchangeReader(object):
    def __init__(self, debug=False):
        FDIR=os.getenv('FDIR')
        assert FDIR is not None

        dataDir = "/".join([FDIR, "data"])

        self.exchanges = {'NASDAQ':None, 'NYSE':None, 'AMEX':None}
        self.exchangeFNs = {'NASDAQ':"/".join([dataDir, "NASDAQCompleteCompanyList.csv"]), 
                            'NYSE':"/".join([dataDir, "NYSECompleteCompanyList.csv"]), 
                            'AMEX':"/".join([dataDir, "AMEXCompleteCompanyList.csv"])}

        self.exchangeURLs = {
            'NASDAQ':"http://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=NASDAQ&render=download",
            'NYSE':"http://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=NYSE&render=download",
            'AMEX':"http://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=AMEX&render=download"}

    def loadOrGetExchange(self, exchangeName):
        if self.exchanges.get(exchangeName) is None:
            fn = self.exchangeFNs.get(exchangeName)
            if fn is None:
                print "Could not find exchange: {}".format(exchangeName)
            else:
                self.exchanges[exchangeName] = pd.read_csv(fn, sep=',')
        return self.exchanges.get(exchangeName)

    def iterExchangeCompanies(self, exchangeName, fun):
        exchange = self.loadOrGetExchange(exchangeName)
        for i, row in exchange[["Symbol", "Name"]].iterrows():
            yield row

    def iterAllCompanies(self, fun):
        for exchangeName in self.exchanges:
            yield self.iterExchangeCompanies(exchangeName, fun)

    def updateExchangeCompanyList(self, exchangeName):
        for exchangeName, compURL in self.exchangeURLs.items():
            r=requests.get(compURL)
            if r.ok:
            else:
                self.
        
    def updateAllExchangeCompanyLists(self):
        for exchangeName in self.exchanges:
            self.updateExchangeCompanyList(exchangeName)
