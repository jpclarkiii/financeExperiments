import os
import logging
import json

from datamodel import Fundamentals

LOGDIR=os.getenv('LOGDIR')
logFN="/".join([LOGDIR,'fundamentals.log'])
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
        self.downloadURL="https://query1.finance.yahoo.com/v10/finance/quoteSummary/NVDA?formatted=true&modules=defaultKeyStatistics"
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

    def requestExtractResults(self):
        r=requests.get(datasource.downloadURL)
        if r.ok:
            marshRes=None
            try:
                marshRes = json.loads(r.content)
            except Exception as e:
                logging.warning("Could not json load request result for {} at {}, exp: {}".format(datasource.name, 
                            datasource.downloadURL, str(e)))
            if marshRes is not None:
                dataRes=marshRes['quoteSummary']['result'][0]
                for finName, finVal in dataRes.get('financialData',{}).items():
                    destName = self.extractionMap.get(finName)
                    if destName is not None:
                    else:
                        logging.debug("NEW data element from Yahoo fundamentals: {}".format(finName))
                for statName, statVal in dataRes.get('defaultKeyStatistics',{}).items():
        else:
            logging.debug("Could not get fundamentals for {} at {}".format(
                 datasource.name, datasource.downloadURL))

{"quoteSummary":{"result":[{"defaultKeyStatistics":{"maxAge":1,"enterpriseValue":{"raw":55980650496,"fmt":"55.98B","longFmt":"55,980,650,496"},"forwardPE":{"raw":31.757486,"fmt":"31.76"},"profitMargins":{"raw":0.24110001,"fmt":"24.11%"},"floatShares":{"raw":564668410,"fmt":"564.67M","longFmt":"564,668,410"},"sharesOutstanding":{"raw":589000000,"fmt":"589M","longFmt":"589,000,000"},"sharesShort":{"raw":22206300,"fmt":"22.21M","longFmt":"22,206,300"},"sharesShortPriorMonth":{"raw":36255300,"fmt":"36.26M","longFmt":"36,255,300"},"heldPercentInsiders":{"raw":0.052470002,"fmt":"5.25%"},"heldPercentInstitutions":{"raw":0.875,"fmt":"87.50%"},"shortRatio":{"raw":1.44,"fmt":"1.44"},"shortPercentOfFloat":{"raw":0.084157,"fmt":"8.42%"},"beta":{"raw":1.48914,"fmt":"1.49"},"morningStarOverallRating":{},"morningStarRiskRating":{},"category":null,"bookValue":{"raw":9.85,"fmt":"9.85"},"priceToBook":{"raw":10.768527,"fmt":"10.77"},"annualReportExpenseRatio":{},"ytdReturn":{},"beta3Year":{},"totalAssets":{},"yield":{},"fundFamily":null,"fundInceptionDate":{},"legalType":null,"ytdReturn":{},"threeYearAverageReturn":{},"fiveYearAverageReturn":{},"priceToSalesTrailing12Months":{},"lastFiscalYearEnd":{"raw":1485648000,"fmt":"2017-01-29"},"nextFiscalYearEnd":{"raw":1548720000,"fmt":"2019-01-29"},"mostRecentQuarter":{"raw":1485648000,"fmt":"2017-01-29"},"earningsQuarterlyGrowth":{"raw":2.144,"fmt":"214.40%"},"revenueQuarterlyGrowth":{},"netIncomeToCommon":{"raw":1666000000,"fmt":"1.67B","longFmt":"1,666,000,000"},"trailingEps":{"raw":2.57,"fmt":"2.57"},"forwardEps":{"raw":3.34,"fmt":"3.34"},"pegRatio":{"raw":3.08,"fmt":"3.08"},"lastSplitFactor":"3/2","lastSplitDate":{"raw":1189468800,"fmt":"2007-09-11"},"enterpriseToRevenue":{"raw":8.101,"fmt":"8.10"},"enterpriseToEbitda":{"raw":26.233,"fmt":"26.23"},"52WeekChange":{"raw":2.0613387,"fmt":"206.13%"},"SandP52WeekChange":{"raw":0.16074276,"fmt":"16.07%"},"lastDividendValue":{},"lastCapGain":{},"annualHoldingsTurnover":{}},"calendarEvents":{"maxAge":1,"earnings":{"earningsDate":[{"raw":1494374400,"fmt":"2017-05-10"},{"raw":1494806400,"fmt":"2017-05-15"}],"earningsAverage":{"raw":0.66,"fmt":"0.66"},"earningsLow":{"raw":0.55,"fmt":"0.55"},"earningsHigh":{"raw":0.8,"fmt":"0.80"},"revenueAverage":{"raw":1908740000,"fmt":"1.91B","longFmt":"1,908,740,000"},"revenueLow":{"raw":1900000000,"fmt":"1.9B","longFmt":"1,900,000,000"},"revenueHigh":{"raw":1942000000,"fmt":"1.94B","longFmt":"1,942,000,000"}},"exDividendDate":{"raw":1487721600,"fmt":"2017-02-22"},"dividendDate":{"raw":1489708800,"fmt":"2017-03-17"}},"financialData":{"maxAge":86400,"currentPrice":{"raw":106.07,"fmt":"106.07"},"targetHighPrice":{"raw":145.0,"fmt":"145.00"},"targetLowPrice":{"raw":38.0,"fmt":"38.00"},"targetMeanPrice":{"raw":113.59,"fmt":"113.59"},"targetMedianPrice":{"raw":120.0,"fmt":"120.00"},"recommendationMean":{"raw":2.4,"fmt":"2.40"},"recommendationKey":"buy","numberOfAnalystOpinions":{"raw":29,"fmt":"29","longFmt":"29"},"totalCash":{"raw":6798000128,"fmt":"6.8B","longFmt":"6,798,000,128"},"totalCashPerShare":{"raw":11.542,"fmt":"11.54"},"ebitda":{"raw":2134000000,"fmt":"2.13B","longFmt":"2,134,000,000"},"totalDebt":{"raw":2788999936,"fmt":"2.79B","longFmt":"2,788,999,936"},"quickRatio":{"raw":4.264,"fmt":"4.26"},"currentRatio":{"raw":4.774,"fmt":"4.77"},"totalRevenue":{"raw":6910000128,"fmt":"6.91B","longFmt":"6,910,000,128"},"debtToEquity":{"raw":48.403,"fmt":"48.40"},"revenuePerShare":{"raw":12.773,"fmt":"12.77"},"returnOnAssets":{"raw":0.14141,"fmt":"14.14%"},"returnOnEquity":{"raw":0.32568002,"fmt":"32.57%"},"grossProfits":{"raw":4063000000,"fmt":"4.06B","longFmt":"4,063,000,000"},"freeCashflow":{"raw":795625024,"fmt":"795.63M","longFmt":"795,625,024"},"operatingCashflow":{"raw":1672000000,"fmt":"1.67B","longFmt":"1,672,000,000"},"earningsGrowth":{"raw":1.821,"fmt":"182.10%"},"revenueGrowth":{"raw":0.551,"fmt":"55.10%"},"grossMargins":{"raw":0.58944,"fmt":"58.94%"},"ebitdaMargins":{"raw":0.30883,"fmt":"30.88%"},"operatingMargins":{"raw":0.28177,"fmt":"28.18%"},"profitMargins":{"raw":0.24110001,"fmt":"24.11%"}}}],"error":null}}


class FundamentalsReader(object):
    def __init__(self, debug=False):
        FDIR=os.getenv('FDIR')
        assert FDIR is not None

        dataDir = "/".join([FDIR, "data"])
        self.dataSources=[]
        self.dataSources.append(yahooFundamentals())

    def read(self, symbol):
        for datasource in self.dataSource:
            datasource.requestExtractResults()
if __name__ == '__main__':
    print "Running download of fundamentals"
    logging.debug("Running Download of Fundamentals")
