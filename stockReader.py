class StockReader(object):
    def __init__(self, debug=False):
        pass

    def downloadSymbols(self, symbols):

        fromday="01"
        frommonth="00"
        fromyear="2006"
        today="24"
        tomonth="03"
        toyear="2016"

        for symbol in symbols:
            r=requests.get("http://real-chart.finance.yahoo.com/table.csv?s={}&a={}&b={}&c={}&d={}&e={}&f={}&g=d&ignore=.csv".format(symbol, frommonth, fromday, fromyear, tomonth, today, toyear))
            if r.ok:
                f=open(FDIR+'/data/{}_{}_{}_{}_{}_{}_{}.csv'.format(symbol, frommonth, fromday, fromyear, tomonth, today, toyear),'w')
                f.write(r.content)
                f.close()
            
    def loadSymbols(self, symbols):
        rootdir=FDIR+"/data"
        symbolFiles=os.listdir(rootdir)

        for symbolFile in symbolFiles:
            symbol=symbolFile.split('_')[0]
            item=symbols.get(symbol)
            if item is not None:
                item['file']=symbolFile
            
        print "Found {} files, loading symbols: {}".format(len(symbolFiles), ", ".join(symbols.keys()))

        print "Loading all symbols..."
        for symbol, pkg in symbols.items():
            fname=pkg['file']
            pkg['data']=pd.read_csv("/".join([rootdir,fname]), index_col=0, 
                                   parse_dates=[0], infer_datetime_format=True)
        
    def dateExists(self, rs, date):
        exists=True
        for equity, item in rs.items():
            try:
                row=item['data'].loc[date]
            except:
                exists=False
        return exists

    def getPricePerShare(self, item, date):
        row = None
        price = None
        try:
            row=item['data'].loc[date]
        except:
            print "Equity did not have data for {}".format(date)
        # Should use spread to choose random time during day for price
        #spread=row['high']-row['low']
        ## starting with worst case: buy highest price each day
        if row is not None:
            try:
                price=row['High']
            except:
                print "No high value"
            try:
                price=row['Low']
            except:
                print "No low value"
            try: 
                price=row['Open']
            except:
                print "No open value"
            try:
                price=row['Close']
            except:
                print "No close value"
        return price
            
    def purchaseEquity(self, item, date, amount):
        price = getPricePerShare(item, date)
        if price is not None:
            sharesPurchased=np.floor(float(amount)/float(price))
            item['amountSpent'] += sharesPurchased*price
            item['sharesOwned'] += sharesPurchased
        
    def buyIntoEquities(self, rs, date):
        for equity, item in rs.items():
            purchaseEquity(item, date, item['min'])
        
    def getPurchaseAlloc(self, rs, date):
        portfolioPercent = 0.7
        purchaseAlloc={}
        underAllocItems=[]
        total=0.0
        for equity, item in rs.items():
            price = getPricePerShare(item, date)
            total += item['sharesOwned']*price
        
        exceedAllocPercent=0.0
        for equity, item in rs.items():
            price = getPricePerShare(item, date)
            alloc = item['sharesOwned']*price
            allocPercentage = (alloc/total)
            if allocPercentage > item['alloc']:
                purchaseAlloc[equity] = 0.0
                exceedAllocPercent += item['alloc']
            else:
                if allocPercentage < item['alloc']:
                    underAllocItems.append(equity)
                purchaseAlloc[equity] = item['alloc']
        if exceedAllocPercent > 0.0:
            if len(underAllocItems) > 0:
                distributeAlloc = float(exceedAllocPercent)/float(len(underAllocItems))
            else:
                distributeAlloc = 0.0
            for equity in underAllocItems:
                purchaseAlloc[equity] += distributeAlloc
            
        print "----exceedAllocPercent: {}, distributelloc: {}".format(exceedAllocPercent, distributeAlloc)
        purchaseAllocTotal = sum(purchaseAlloc.values())
        print "----Total purchase Alloc percent: {}".format(purchaseAllocTotal)
        print "----Equities exceeding alloc: {}".format([a for a,i in purchaseAlloc.items() if i==0.0])
        print "----Equities under alloc: {}".format(underAllocItems)
        assert purchaseAllocTotal==0.7   
        return purchaseAlloc
