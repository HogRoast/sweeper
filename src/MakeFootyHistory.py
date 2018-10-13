import sys, os
import numpy
from scipy import stats
from Logging import Logger
from FootyUtils import getFootyOptions, getFootyConfig, newCSVFile, \
        readCSVFileAsDict
from FootyAnalysisTools import model, analysisDir

def makeFootyHistory(resultsURLTmpl, opts=sys.argv):
    log = Logger()
    getFootyOptions(log, opts)

    (algoCfg, mailCfg) = getFootyConfig()
    rangeMap = algoCfg['rangeMap']
    seasons = algoCfg['seasons']

    '''
    Looks like if you go back too far with the historical data it starts to 
    mess up the results, I suspect this is because the league composition has 
    changed enough to mean that the newer and older season data don't play 
    well together...
    '''
    log.info(__name__ + ' : ' + model.__class__.__name__)
    for league in rangeMap.keys():
        log.info('League : {}...'.format(league))
        os.makedirs('{}/{}'.format(analysisDir, league), exist_ok = True)
        summaryData = {}
        with newCSVFile('{}/{}/History.{}.csv'.format(analysisDir, league, 
                    model.__class__.__name__), 
                    ['Date', 'HomeTeam', 'AwayTeam', 'Mark', 'Result']) \
                        as historyWriter:
            for season in seasons:
                resultsURL = resultsURLTmpl.format(season, league)
                log.debug('Processing...{}'.format(resultsURL))
                try:
                    with readCSVFileAsDict(resultsURL) as resultsReader:
                        # Assembling as list so that the iterator can be reused
                        res = list(resultsReader)
                        data = model.processMatches(res)
                        for row in res:
                            try:
                                date, ht, at, mark, hForm, aForm = \
                                        model.markMatch(data, 
                                                row['Date'], 
                                                row['HomeTeam'], 
                                                row['AwayTeam'])
                            except KeyError:
                                continue
                            if mark is None or row['FTR'] == '':
                                continue
                            mark = int(mark)
                            matchResult = row['FTR'].strip()
                            historyWriter.writerow(
                                    [date, ht, at, mark, matchResult])

                            if mark not in summaryData:
                                summaryData[mark] = {'A' : 0, 'D' : 0, 'H': 0}
                            summaryData[mark][matchResult] += 1
                except BaseException:
                    log.error(sys.exc_info()[0:1])
                    continue

        log.info('Writing summary data...')

        with newCSVFile('{}/{}/Summary.{}.csv'.format(analysisDir, league, 
                    model.__class__.__name__), 
                    ['Mark', 'Frequency', '%H','HO', '%D', 'DO', '%A', 'AO']) \
                        as summaryWriter:
            x = []
            hY = []
            dY = []
            aY = []
            hist = {} 
            for mark in summaryData:
                if mark >15 or mark <-15:
                    continue
                awayF = summaryData[mark]['A']
                drawF = summaryData[mark]['D']
                homeF = summaryData[mark]['H']

                totalF = awayF + drawF + homeF
                awayP = awayF / totalF * 100
                drawP = drawF / totalF * 100
                homeP = homeF / totalF * 100

                x.append(mark)
                hY.append(homeP)
                dY.append(drawP)
                aY.append(awayP)

                awayO = awayP if awayP == 0 else 100 / awayP 
                drawO = drawP if drawP == 0 else 100 / drawP 
                homeO = homeP if homeP == 0 else 100 / homeP 

                hist[mark] = (homeF, homeP)
                summaryWriter.writerow([mark, totalF, 
                    '{:>4.2f}'.format(homeP), '{:>4.2f}'.format(homeO),
                    '{:>4.2f}'.format(drawP), '{:>4.2f}'.format(drawO),
                    '{:>4.2f}'.format(awayP), '{:>4.2f}'.format(awayO)])

        s = ''
        for h in sorted(hist.items(), key = lambda x : x[1][0], reverse = True):
            s += '{:d} ({:d} {:>5.2f}) '.format(h[0], h[1][0], h[1][1])
        log.info(s)

        with newCSVFile('{}/{}/Stats.{}.csv'.format(analysisDir, league, 
                    model.__class__.__name__),
                    ['Result', 'Slope', 'Intercept', 'P', 'R', 'R^2', 'Err']) \
                        as statsWriter:
            slope, intercept, r, p, stderr = stats.linregress(x, hY)
            r2 = r**2
            log.info('Home: {:>4.2f} {:>4.2f} {:>4.2} {:>4.2f} {:>4.2f} {:>4.2}'.format(slope, intercept, p, r, r2, stderr))
            statsWriter.writerow(['H', '{:>4.2f}'.format(slope), 
                '{:>4.2f}'.format(intercept), '{:>4.2f}'.format(p), 
                '{:>4.2f}'.format(r), '{:>4.2f}'.format(r2), 
                '{:>4.2f}'.format(stderr)])

            slope, intercept, r, p, stderr = stats.linregress(x, dY)
            r2 = r**2
            log.info('Draw: {:>4.2f} {:>4.2f} {:>4.2} {:>4.2f} {:>4.2f} {:>4.2}'.format(slope, intercept, p, r, r2, stderr))
            statsWriter.writerow(['D', '{:>4.2f}'.format(slope), 
                '{:>4.2f}'.format(intercept), '{:>4.2f}'.format(p), 
                '{:>4.2f}'.format(r), '{:>4.2f}'.format(r2), 
                '{:>4.2f}'.format(stderr)])

            slope, intercept, r, p, stderr = stats.linregress(x, aY)
            r2 = r**2
            log.info('Away: {:>4.2f} {:>4.2f} {:>4.2} {:>4.2f} {:>4.2f} {:>4.2}'.format(slope, intercept, p, r, r2, stderr))
            statsWriter.writerow(['A', '{:>4.2f}'.format(slope), 
                '{:>4.2f}'.format(intercept), '{:>4.2f}'.format(p), 
                '{:>4.2f}'.format(r), '{:>4.2f}'.format(r2), 
                '{:>4.2f}'.format(stderr)])

if __name__ == '__main__':
    ''' How often do the following url change? '''
    resultsURLTmpl = 'http://www.football-data.co.uk/mmz4281/{}/{}.csv'
    makeFootyHistory(resultsURLTmpl, sys.argv)
