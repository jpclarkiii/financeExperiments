import json

class DMEntity(object):
    Rename = {}
    types = {}
    m_fields = []
    ignore = []
    linked_pos = {}

    def __init__(self, d=None):
        if d is not None:
            self.__from_jdict__(d)

    def __to_jdict__(self):
        del_lst = []
        d={}
        for atr in self.__dict__.keys():
            if atr not in self.__class__.ignore:
                val = self.__getattribute__(atr)
                s_i = None
                if isinstance(val, set):
                    val=list(val)
                if isinstance(val, list):
                    #print "Object {} attribute {} was a list".format(self.__class__, atr)
                    s_i = self.__serialize_lst__(val)
                elif isinstance(val, dict):
                    #print "Object {} attribute {} was a dict".format(self.__class__, atr)
                    s_i = self.__serialize_dict__(val)
                else:
                    try:
                        #print "Object {} attribute {} NOT dict or list".format(self.__class__, atr)
                        s_i = val.__to_json__()
                    except:
                        s_i = val
                if not self.__remove_val__(s_i):
                    rnm = self.__class__.Rename.get(atr)
                    if rnm is not None:
                        d[rnm] = s_i
                    else:
                        d[atr] = s_i
        return d
    def __from_jdict__(self, d):
        s = d
        if isinstance(d, basestring):
            s = json.loads(d)

        for atr in self.__dict__.keys():
            rnm = self.__class__.Rename.get(atr)
            rnatr = atr
            if rnm is not None:
                rnatr = rnm
            val = d.get(rnatr)
            if val is not None:
                atr_type = self.__class__.types.get(atr)
                if atr_type is None:
                    self.__setattr__(atr, val)
                elif isinstance(atr_type, collections.MutableSequence):
                    atr_type = atr_type[0]
                    self.__setattr__(atr, [])
                    atr_val = self.__getattribute__(atr)
                    assert isinstance(val, collections.MutableSequence)
                    for sd in val:
                        sub_class = atr_type(sd)
                        atr_val.append(sub_class)
                else:
                    sub_class = atr_type(val)
                    self.__setattr__(atr, sub_class)
    def __serialize_lst__(self, lst):
        s_lst = []
        for i in lst:
            s_i = None
            if isinstance(i, list):
                s_i = self.__serialize_lst__(i)
            elif isinstance(i, dict):
                s_i = self.__serialize_dict__(i)
            else:
                try:
                    s_i = i.__to_json__()
                except:
                    s_i = i
            if not self.__remove_val__(s_i):
                s_lst.append(s_i)
        return s_lst
                
        
    def __serialize_dict__(self, dct):
        s_dct = {}
        for key, i in dct.iteritems():
            s_i = None
            if isinstance(i, list):
                s_i = self.__serialize_lst__(i)
            elif isinstance(i, dict):
                s_i = self.__serialize_dict__(i)
            else:
                try:
                    s_i = i.__to_json__()
                except:
                    s_i = i
            if not self.__remove_val__(s_i):
                s_dct[key] = s_i
        return s_dct
    def __remove_val__(self, val):
        ret = False
        if val is None:
            ret = True
        if isinstance(val, list) or isinstance(val, dict):
            if len(val) == 0:
                ret = True
        if val == '':
            ret = True
        return ret
    def __to_json__(self):
        return json.dumps(self.__to_jdict__())
    def __from_json__(self, jsonStr):
        self.__from_jdict__(json.loads(jsonStr))


class Fundamentals(DMEntity):
    def __init__(self, d=None):
        self.returnOnEquity=None
        self.totalRevenue=None
        self.maxAge=None
        self.targetLowPrice=None
        self.currentPrice=None
        self.ebitda=None
        self.currentRatio=None
        self.numberOfAnalystOpinions=None
        self.revenuePerShare=None
        self.freeCashflow=None
        self.totalCashPerShare=None
        self.operatingMargins=None
        self.returnOnAssets=None
        self.ebitdaMargins=None
        self.targetMedianPrice=None
        self.totalDebt=None
        self.targetHighPrice=None
        self.totalCash=None
        self.recommendationKey=None
        self.grossMargins=None
        self.grossProfits=None
        self.targetMeanPrice=None
        self.debtToEquity=None
        self.profitMargins=None
        self.operatingCashflow=None
        self.recommendationMean=None
        self.earningsGrowth=None
        self.revenueGrowth=None
        self.quickRatio=None
        self.priceToSalesTrailing12Months=None
        self.shortRatio=None
        self.52WeekChange=None
        self.bookValue=None
        self.floatShares=None
        self.revenueQuarterlyGrowth=None
        self.forwardPE=None
        self.maxAge=None
        self.profitMargins=None
        self.totalAssets=None
        self.shortPercentOfFloat=None
        self.lastDividendValue=None
        self.lastSplitFactor=None
        self.category=None
        self.heldPercentInsiders=None
        self.trailingEps=None
        self.fundFamily=None
        self.morningStarOverallRating=None
        self.sharesShortPriorMonth=None
        self.netIncomeToCommon=None
        self.fundInceptionDate=None
        self.beta3Year=None
        self.enterpriseToRevenue=None
        self.enterpriseToEbitda=None
        self.priceToBook=None
        self.threeYearAverageReturn=None
        self.morningStarRiskRating=None
        self.legalType=None
        self.enterpriseValue=None
        self.pegRatio=None
        self.lastCapGain=None
        self.mostRecentQuarter=None
        self.beta=None
        self.sharesOutstanding=None
        self.lastSplitDate=None
        self.ytdReturn=None
        self.annualHoldingsTurnover=None
        self.fiveYearAverageReturn=None
        self.nextFiscalYearEnd=None
        self.annualReportExpenseRatio=None
        self.heldPercentInstitutions=None
        self.yield=None
        self.forwardEps=None
        self.lastFiscalYearEnd=None
        self.earningsQuarterlyGrowth=None
        self.SandP52WeekChange=None
        self.sharesShort=None
        super(Fundamentals, self).__init__(d=d)
