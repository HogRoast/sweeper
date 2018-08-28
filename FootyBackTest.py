rangeMap = {
    'E0' : range(-1, 2), 
    #'SC0' : range(-2, 0), # works really well! 11%
    'SC0' : range(0, 0),
    #'B1' : range(-2, -1), # this is fantastic 63%! Maybe better odds when away team is favourite
    'B1' : range(0, 0),
    #'E1' : range(-1, 2), # -2, 3 also works but not as effective
    'E1' : range(0, 0),
    #'I1' : range(1, 2), 
    'I1' : range(0, 0), 
    #'SP1' : range(-6, -5), # strange but yields 10%, however don't trust it enough to go for it
    'SP1' : range(0, 0),
    #'F1' : range(-2, 0), # Similar to Belgium
    'F1' : range(0, 0),
    'D1' : range(0, 4), # If the home team is favourite, it will win!
}

if __name__ == '__main__':
    import urllib.request
    import csv, sys
    import FootyAnalysisTools
    from Logging import Logger

    log = Logger()
    if len(sys.argv) > 1:
        if '-d' in sys.argv: log.toggleMask(Logger.DEBUG | Logger.TIME | Logger.TYPE)
        if '-r' in sys.argv:
            i = sys.argv.index('-r')
            rmErr = True
            if i+1 < len(sys.argv):
                try:
                    rangeMap = eval(sys.argv[i+1])
                    log.debug(rangeMap)
                    if isinstance(rangeMap, dict):
                        rmErr = False
                except BaseException:
                    log.debug('Failed to evaluate rangeMap arg')
            if rmErr:
                log.critical('-r option must be followed by dictionary type representing a rangeMap')
                sys.exit(-1)

    years = ['1718', '1617', '1516', '1415', '1314', '1213', '1112']#, '1011', '0910', '0809', '0708', '0607', '0506', '0405', '0304', '0203', '0102', '0001']

    resultsURLTmpl = 'http://www.football-data.co.uk/mmz4281/{}/{}.csv'

    for league in rangeMap.keys():
        summaryCSV = '{}/{}/Summary.{}.csv'.format(FootyAnalysisTools.analysisDir, league, FootyAnalysisTools.model.__class__.__name__)

        summaryFile = open(summaryCSV, 'r', newline='')
        summaryReader = csv.DictReader(summaryFile, delimiter=',')
        summaryData = {}
        for row in summaryReader:
            mark = int(row['Mark'])
            summaryData[mark] = {   'H' : (float(row['%H']), float(row['HO'])),
                                    'D' : (float(row['%D']), float(row['DO'])),
                                    'A' : (float(row['%A']), float(row['AO']))}

        backTestCSV = '{}/{}/BackTest.{}.csv'.format(FootyAnalysisTools.analysisDir, league, FootyAnalysisTools.model.__class__.__name__)
        backTestFieldNames = ['Date', 'HomeTeam', 'AwayTeam', 'Mark', 'Result', 'MyBet', 'MyOdds', 'Bookie', 'BookieOdds', 'Winnings', 'PnL', 'T_Stk', 'T_W', 'Yield']
        backTestFile = open(backTestCSV, 'w', newline='')
        backTestWriter = csv.writer(backTestFile)
        backTestWriter.writerow(backTestFieldNames)

        ts = tw = y = 0 
        for year in years:
            resultsURL = resultsURLTmpl.format(year, league)
            log.debug('Processing...{}'.format(resultsURL))

            httpResp = urllib.request.urlopen(resultsURL)
            results = str(httpResp.read())
            csvFile = results.split('\\r\\n')

            resultsReader = csv.DictReader(csvFile, delimiter=',')
            data = FootyAnalysisTools.model.processMatches(resultsReader)

            resultsReader = csv.DictReader(csvFile, delimiter=',')
            for row in resultsReader:
                date, ht, at, mark, hForm, aForm = FootyAnalysisTools.model.markMatch(data, row['Date'], row['HomeTeam'], row['AwayTeam'])
                if mark is None:
                    continue

                if mark in rangeMap[league]:
                    bestH = 0
                    bestD = 0
                    bestA = 0
                    bookie = ''
                    try:
                        b365H = float(row['B365H'])
                        b365D = float(row['B365D'])
                        b365A = float(row['B365A'])
                        if b365H > bestH : 
                            bestH = b365H
                            bookie = 'B365'
                    except BaseException:
                        log.error('No B365 data - skipping : ' + date + ht + at)
                    try:
                        bwH = float(row['BWH'])
                        bwD = float(row['BWD'])
                        bwA = float(row['BWA'])
                        if bwH > bestH : 
                            bestH = bwH
                            bookie = 'BW'
                    except BaseException:
                        log.error('No BW data - skipping : ' + date + ht + at)
                    try:
                        iwH = float(row['IWH'])
                        iwD = float(row['IWD'])
                        iwA = float(row['IWA'])
                        if iwH > bestH : 
                            bestH = iwH
                            bookie = 'IW'
                    except BaseException:
                        log.error('No IW data - skipping : ' + date + ht + at)
                    try:
                        lbH = float(row['LBH'])
                        lbD = float(row['LBD'])
                        lbA = float(row['LBA'])
                        if lbH > bestH : 
                            bestH = lbH
                            bookie = 'LB'
                    except BaseException:
                        log.error('No LB data - skipping : ' + date + ht + at)
                    try:
                        whH = float(row['WHH'])
                        whD = float(row['WHD'])
                        whA = float(row['WHA'])
                        if whH > bestH : 
                            bestH = whH
                            bookie = 'WH'
                    except BaseException:
                        log.error('No WH data - skipping : ' + date + ht + at)
                    try:
                        vcH = float(row['VCH'])
                        vcD = float(row['VCD'])
                        vcA = float(row['VCA'])
                        if vcH > bestH : 
                            bestH = vcH
                            bookie = 'VC'
                    except BaseException:
                        log.error('No VC data - skipping : ' + date + ht + at)

                    hSD = summaryData[mark]['H'] 
                    aSD = summaryData[mark]['A'] 
                    dSD = summaryData[mark]['D'] 

                    myBet = ''
                    myOdds = 0.0
                    myPercent = 0.0
                    bookieOdds = 0.0
                    winnings = 0.0
                    pnl = 0.0
                    
                    if bestH > hSD[1]:# and bestH < (hSD[1] * 2):
                        myBet = 'H'
                        myOdds = hSD[1]
                        #myOdds = (1.97*mark+45.42)*0.9
                        myPercent = hSD[0]
                        bookieOdds = bestH
                        winnings = bookieOdds
                        pnl = winnings - 1

                    if False and myPercent < dSD[0] and bestD > dSD[1]:
                    #if myPercent < dSD[0] and b365D > dSD[1]:
                        myBet = 'D'
                        myOdds = dSD[1]
                        myPercent = dSD[0]
                        bookieOdds = bestD
                        winnings = bookieOdds
                        pnl = winnings - 1

                    if False and myPercent < aSD[0] and bestA > aSD[1]:
                    #if myPercent < aSD[0] and b365A > aSD[1]:
                        myBet = 'A'
                        myOdds = aSD[1]
                        myPercent = aSD[0]
                        bookieOdds = bestA
                        winnings = bookieOdds
                        pnl = winnings - 1
                  
                    matchResult = row['FTR']
                    if myBet != '':
                        if matchResult != myBet:
                            winnings = 0.0
                            pnl = -1.0 
                        ts += 1
                        tw += winnings
                        y = (tw-ts)/ts

                    backTestWriter.writerow((date, ht, at, mark, matchResult, myBet, myOdds, bookie, bookieOdds, winnings, pnl, ts, tw, y))
        log.info('{:<5s} - Staked: £{:>6.2f} Won: £{:>6.2f} Yield: {:>6.2f}%'.format(league, ts, tw, y*100))
