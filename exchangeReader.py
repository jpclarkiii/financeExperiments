import os
from os.path import join
import logging
import requests
import json
import pandas as pd

LOGDIR="/Users/johnclark/Galaxy/financeExperiments/data"
logFN=join(LOGDIR,'fundamentals.log')
logging.basicConfig(filename=logFN, level=logging.DEBUG,
                    format='%(levelname)s:%(asctime)s %(message)s')

class ExchangeReader(object):
    def __init__(self, debug=False):
        FDIR="/Users/johnclark/Galaxy/financeExperiments"
        dataDir = join(FDIR, "data")

        self.exchanges = {'NASDAQ':None, 'NYSE':None, 'AMEX':None}
        self.exchangeFNs = {'NASDAQ':join(dataDir, "NASDAQCompleteCompanyList.csv"), 
                            'NYSE':join(dataDir, "NYSECompleteCompanyList.csv"), 
                            'AMEX':join(dataDir, "AMEXCompleteCompanyList.csv")}

        self.exchangeURLs = {
            'NASDAQ':"https://www.nasdaq.com/api/screener/stocks?tableonly=true&limit=25&offset=0&exchange=NASDAQ&download=true",
            'NYSE':"https://www.nasdaq.com/api/screener/stocks?tableonly=true&limit=25&offset=0&exchange=NYSE&download=true",
            'AMEX':"https://www.nasdaq.com/api/screener/stocks?tableonly=true&limit=25&offset=0&exchange=AMEX&download=true"}
    
        self.headers = {
            "Accept": "application/json, text/plain, */*",
            "Origin": "https://www.nasdaq.com",
            "Accept-Encoding": "gzip, deflate, br",
            "Host": "api.nasdaq.com",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
            "Accept-Language": "en-us",
            "Referer": "https://www.nasdaq.com/",
            "Connection": "keep-alive"}

    def loadExchange(self, exchangeName):
        if exchangeName in self.exchangeFNs:
            fn = self.exchangeFNs[exchangeName]
            self.exchanges[exchangeName] = pd.read_csv(fn, index_col=False)
        else:
            raise Exception("Exchange {} not in list of known exchages".format(exchangeName))
        return self.exchanges.get(exchangeName)

    def downloadExchangeCompanyList(self, exchangeName):
        df_nasdaq_comps = None
        if exchangeName in self.exchangeURLs:
            exchangeURL = self.exchangeURLs[exchangeName]

            resp = requests.get(exchangeURL, headers=self.headers)
            if resp.ok:
                resp_json = json.loads(resp.content)
                nasdaq_comps = resp_json["data"]["rows"]
                df_nasdaq_comps = pd.DataFrame(nasdaq_comps)
            else:
                raise Exception("Exchange download failed: {}".format(resp))
        else:
            raise Exception("Exchange {} not in list of known exchages".format(exchangeName))
        exchange_path = self.exchangeFNs[exchangeName]
        df_nasdaq_comps.to_csv(exchange_path, index=False)

    def downloadAllExchangeCompanyLists(self):
        for exchangeName, compURL in self.exchangeURLs.items():
            self.downloadExchangeCompanyList(exchangeName)






