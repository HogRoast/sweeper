import sys
from configparser import ConfigParser
from Logging import Logger
from FootyUtils import FootyArgsError, getFootyOptions, getFootyConfig, newCSVFile, readCSVFileAsDict
from FootyAnalysisTools import model, analysisDir

def footyBackTest(resultsURLTmpl, opts=sys.argv):
    (algoCfg, mailCfg) = getFootyConfig()
    rangeMap = algoCfg['rangeMap']
    seasons = algoCfg['seasons']

    log = Logger()
    (sm, rm) = getFootyOptions(log, opts)
    rangeMap = rm if rm else rangeMap

    for league in rangeMap.keys():
        summaryData = {}
        with readCSVFileAsDict(
                '{}/{}/Summary.{}.csv'.format(analysisDir, league,
                    model.__class__.__name__)) as summaryReader:
            for row in summaryReader:
                mark = int(row['Mark'])
                summaryData[mark] = {'H' : (float(row['%H']), float(row['HO'])),
                                     'D' : (float(row['%D']), float(row['DO'])),
                                     'A' : (float(row['%A']), float(row['AO']))}
        with newCSVFile(
                '{}/{}/BackTest.{}.csv'.format(analysisDir, league, 
                    model.__class__.__name__),
                ['Date', 'HomeTeam', 'AwayTeam', 'Mark', 'Result', 'MyBet', 
                    'MyOdds', 'Bookie', 'BookieOdds', 'Winnings', 'PnL', 
                    'T_Stk', 'T_W', 'Yield']) as backTestWriter:
            ts = tw = y = 0 
            for season in seasons:
                resultsURL = resultsURLTmpl.format(season, league)
                log.debug('Processing...{}'.format(resultsURL))
                with readCSVFileAsDict(resultsURL) as resultsReader:
                    # Assemble results as list so that we can reuse the iterator
                    res = list(resultsReader)
                    data = model.processMatches(res)
                    for row in res:
                        date, ht, at, mark, hForm, aForm = model.markMatch(
                                data, row['Date'], row['HomeTeam'], 
                                row['AwayTeam'])
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
                                log.error('No B365 data - skipping : {} {} {}'\
                                        .format(date, ht, at))
                            try:
                                bwH = float(row['BWH'])
                                bwD = float(row['BWD'])
                                bwA = float(row['BWA'])
                                if bwH > bestH : 
                                    bestH = bwH
                                    bookie = 'BW'
                            except BaseException:
                                log.error('No BW data - skipping : {} {} {}'\
                                        .format(date, ht, at))
                            try:
                                iwH = float(row['IWH'])
                                iwD = float(row['IWD'])
                                iwA = float(row['IWA'])
                                if iwH > bestH : 
                                    bestH = iwH
                                    bookie = 'IW'
                            except BaseException:
                                log.error('No IW data - skipping : {} {} {}'\
                                        .format(date, ht, at))
                            try:
                                lbH = float(row['LBH'])
                                lbD = float(row['LBD'])
                                lbA = float(row['LBA'])
                                if lbH > bestH : 
                                    bestH = lbH
                                    bookie = 'LB'
                            except BaseException:
                                log.error('No LB data - skipping : {} {} {}'\
                                        .format(date, ht, at))
                            try:
                                whH = float(row['WHH'])
                                whD = float(row['WHD'])
                                whA = float(row['WHA'])
                                if whH > bestH : 
                                    bestH = whH
                                    bookie = 'WH'
                            except BaseException:
                                log.error('No WH data - skipping : {} {} {}'\
                                        .format(date, ht, at))
                            try:
                                vcH = float(row['VCH'])
                                vcD = float(row['VCD'])
                                vcA = float(row['VCA'])
                                if vcH > bestH : 
                                    bestH = vcH
                                    bookie = 'VC'
                            except BaseException:
                                log.error('No VC data - skipping : {} {} {}'\
                                        .format(date, ht, at))

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

                            backTestWriter.writerow(
                                    (date, ht, at, mark, matchResult, myBet, 
                                        myOdds, bookie, bookieOdds, winnings, 
                                        pnl, ts, tw, y))

        log.info('{:<5s} - Staked: GBP{:>6.2f} Won: GBP{:>6.2f} Yield: {:>6.2f}%'.format(league, ts, tw, y*100))
   
if __name__ == '__main__':
    resultsURLTmpl = 'http://www.football-data.co.uk/mmz4281/{}/{}.csv'
    footyBackTest(resultsURLTmpl, sys.argv)
