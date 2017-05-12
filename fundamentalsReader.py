import os
import logging
import json

from datamodel import Fundamentals
from exchangeReader import ExchangeReader

LOGDIR=os.getenv('LOGDIR')
logFN="/".join([LOGDIR,'fundamentals.log'])
logger = logging.getLogger('fundamentalsReader')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s [%(name)s] %(message)s')
logging.basicConfig(filename=logFN, level=logging.DEBUG,
                    format='%(levelname)s:%(asctime)s %(message)s')

class dataSource(object):
    def __init__(self):
        self.name='Abstract'
        self.downloadURL=None

    def requestExtractResults(self):
        return None

class yahooFundamentals(dataSource):
    def __init__(self):
        self.name='YahooFundamentals'
        #self.downloadURL="https://query1.finance.yahoo.com/v10/finance/quoteSummary/{}?formatted=true&modules=defaultKeyStatistics,financialData,calendarEvents"
        self.downloadURL="https://query2.finance.yahoo.com/v10/finance/quoteSummary/{}?formatted=true&modules=defaultKeyStatistics,financialData,calendarEventsincomeStatementHistory,cashflowStatementHistory,balanceSheetHistory,incomeStatementHistoryQuarterly,cashflowStatementHistoryQuarterly,balanceSheetHistoryQuarterly,earnings "
        self.extractionMap={
            "priceToSalesTrailing12Months":"priceToSalesTrailing12Months",
            "shortRatio":"shortRatio",
            "52WeekChange":"52WeekChange",
            "bookValue":"bookValue",
            "floatShares":"floatShares",
            "revenueQuarterlyGrowth":"revenueQuarterlyGrowth",
            "forwardPE":"forwardPE",
            "maxAge":"maxAge",
            "profitMargins":"profitMargins",
            "totalAssets":"totalAssets",
            "shortPercentOfFloat":"shortPercentOfFloat",
            "lastDividendValue":"lastDividendValue",
            "lastSplitFactor":"lastSplitFactor",
            "category":"category",
            "heldPercentInsiders":"heldPercentInsiders",
            "trailingEps":"trailingEps",
            "fundFamily":"fundFamily",
            "morningStarOverallRating":"morningStarOverallRating",
            "sharesShortPriorMonth":"sharesShortPriorMonth",
            "netIncomeToCommon":"netIncomeToCommon",
            "fundInceptionDate":"fundInceptionDate",
            "beta3Year":"beta3Year",
            "enterpriseToRevenue":"enterpriseToRevenue",
            "enterpriseToEbitda":"enterpriseToEbitda",
            "priceToBook":"priceToBook",
            "threeYearAverageReturn":"threeYearAverageReturn",
            "morningStarRiskRating":"morningStarRiskRating",
            "legalType":"legalType",
            "enterpriseValue":"enterpriseValue",
            "pegRatio":"pegRatio",
            "lastCapGain":"lastCapGain",
            "mostRecentQuarter":"mostRecentQuarter",
            "beta":"beta",
            "sharesOutstanding":"sharesOutstanding",
            "lastSplitDate":"lastSplitDate",
            "ytdReturn":"ytdReturn",
            "annualHoldingsTurnover":"annualHoldingsTurnover",
            "fiveYearAverageReturn":"fiveYearAverageReturn",
            "nextFiscalYearEnd":"nextFiscalYearEnd",
            "annualReportExpenseRatio":"annualReportExpenseRatio",
            "heldPercentInstitutions":"heldPercentInstitutions",
            "yield":"yield",
            "forwardEps":"forwardEps",
            "lastFiscalYearEnd":"lastFiscalYearEnd",
            "earningsQuarterlyGrowth":"earningsQuarterlyGrowth",
            "SandP52WeekChange":"SandP52WeekChange",
            "sharesShort":"sharesShort",
            "returnOnEquity":"returnOnEquity",
            "totalRevenue":"totalRevenue",
            "maxAge":"maxAge",
            "targetLowPrice":"targetLowPrice",
            "currentPrice":"currentPrice",
            "ebitda":"ebitda",
            "currentRatio":"currentRatio",
            "numberOfAnalystOpinions":"numberOfAnalystOpinions",
            "revenuePerShare":"revenuePerShare",
            "freeCashflow":"freeCashflow",
            "totalCashPerShare":"totalCashPerShare",
            "operatingMargins":"operatingMargins",
            "returnOnAssets":"returnOnAssets",
            "ebitdaMargins":"ebitdaMargins",
            "targetMedianPrice":"targetMedianPrice",
            "totalDebt":"totalDebt",
            "targetHighPrice":"targetHighPrice",
            "totalCash":"totalCash",
            "recommendationKey":"recommendationKey",
            "grossMargins":"grossMargins",
            "grossProfits":"grossProfits",
            "targetMeanPrice":"targetMeanPrice",
            "debtToEquity":"debtToEquity",
            "profitMargins":"profitMargins",
            "operatingCashflow":"operatingCashflow",
            "recommendationMean":"recommendationMean",
            "earningsGrowth":"earningsGrowth",
            "revenueGrowth":"revenueGrowth",
            "quickRatio":"quickRatio"
         }

    def requestExtractResults(self, symbol):
        req_url = self.downloadURL.format(symbol)
        r=requests.get(req_url)
        fundObj=None
        if r.ok:
            marshRes=None
            try:
                marshRes = json.loads(r.content)
            except Exception as e:
                logging.warning("Could not json load request result for {} at {}, exp: {}".format(datasource.name, 
                            req_url, str(e)))
            if marshRes is not None:
                fundObj = Fundamentals()
                dataRes=marshRes['quoteSummary']['result'][0]
                for finName, finVal in dataRes.get('financialData',{}).items():
                    destName = self.extractionMap.get(finName)
                    if destName is not None:
                        if fundObj.__dict__.get(destName) is not None:
                            fundObj.__setattr__(destName, finVal)
                        else:
                            logging.warning("Fundamental item {} is not in datamodel".format(destName))
                    else:
                        logging.debug("NEW data element from Yahoo fundamentals: {}".format(finName))
                for statName, statVal in dataRes.get('defaultKeyStatistics',{}).items():
        else:
            logging.debug("Could not get fundamentals for {} at {}".format(
                 datasource.name, req_url))
        return fundObj

class FundamentalsReader(object):
    def __init__(self, debug=False):
        FDIR=os.getenv('FDIR')
        assert FDIR is not None

        dataDir = "/".join([FDIR, "data"])
        self.dataSources=[]
        self.dataSources.append(yahooFundamentals())

    def read(self, symbol):
        ExchangeReader()
        fundObjs=[]
        for datasource in self.dataSource:
            fundObjs.append(datasource.requestExtractResults(symbol))
        #TODO merge the fundObjs
        
        ## Now store new

if __name__ == '__main__':
    print "Running download of fundamentals"
    logging.debug("Running Download of Fundamentals")
