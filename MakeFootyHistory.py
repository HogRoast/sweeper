import urllib.request
import csv, sys, os
import FootyAnalysisTools
import numpy
from scipy import stats
from Logging import Logger
from FootyBackTest import rangeMap

log = Logger()
if len(sys.argv) > 1:
    if '-d' in sys.argv: log.toggleMask(Logger.DEBUG | Logger.TIME | Logger.TYPE)

'''
 How often do the following url change?
 Looks like if you go back too far with the historical data it starts to mess up the data, I suspect this is because the
 league composition has changed enough to mean that the newer and older season data don't play well together...
'''
years = ['1617', '1516', '1415', '1314', '1213', '1112', '1011', '0910', '0809', '0708', '0607', '0506', '0405', '0304', '0203', '0102', '0001']
leagues = [ 'E0', 'E1', 'E2', 'E3', 'EC', 'SC0', 'SC1', 'SC2', 'SC3', 'D1', 'D2', 'I1', 'I2', 'SP1', 'SP2', 'F1', 'F2', 'N1', 'B1', 'P1', 'T1', 'G1'] 

log.info(__name__ + ' : ' + FootyAnalysisTools.model.__class__.__name__)

resultsURLTmpl = 'http://www.football-data.co.uk/mmz4281/{}/{}.csv'
                
for league in rangeMap.keys():
    log.info('League : {}...'.format(league))
    os.makedirs('{}/{}'.format(FootyAnalysisTools.analysisDir, league), exist_ok = True)
    summaryData = {}
    historyCSV = '{}/{}/History.{}.csv'.format(FootyAnalysisTools.analysisDir, league, FootyAnalysisTools.model.__class__.__name__)
    historyFieldNames = ['Date', 'HomeTeam', 'AwayTeam', 'Mark', 'Result']
    historyFile = open(historyCSV, 'w', newline='')
    historyWriter = csv.writer(historyFile)
    historyWriter.writerow(historyFieldNames)

    for year in years:
        resultsURL = resultsURLTmpl.format(year, league)
        log.debug('Processing...{}'.format(resultsURL))

        try:
            httpResp = urllib.request.urlopen(resultsURL)
        except BaseException:
            log.error(sys.exc_info()[0:1])
            continue
        results = str(httpResp.read())
        csvFile = results.split('\\r\\n')

        resultsReader = csv.DictReader(csvFile, delimiter=',')
        data = FootyAnalysisTools.model.processMatches(resultsReader)

        resultsReader = csv.DictReader(csvFile, delimiter=',')
        for row in resultsReader:
            try:
                date, ht, at, mark, hForm, aForm = FootyAnalysisTools.model.markMatch(data, row['Date'], row['HomeTeam'], row['AwayTeam'])
            except KeyError:
                continue
            if mark is None or row['FTR'] == '':
                continue
            mark = int(mark)
            matchResult = row['FTR'].strip()
            historyWriter.writerow([date, ht, at, mark, matchResult])

            if mark in summaryData:
                summaryData[mark][matchResult] += 1
            else:
                summaryData[mark] = {'A' : 1, 'D' : 1, 'H': 1}

    log.info('Writing summary data...')
    summaryCSV = '{}/{}/Summary.{}.csv'.format(FootyAnalysisTools.analysisDir, league, FootyAnalysisTools.model.__class__.__name__)
    summaryFieldNames = ['Mark', 'Frequency', '%H','HO', '%D', 'DO', '%A', 'AO']
    summaryFile = open(summaryCSV, 'w', newline='')
    summaryWriter = csv.writer(summaryFile)
    summaryWriter.writerow(summaryFieldNames)

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

        awayO = 100 / awayP 
        drawO = 100 / drawP 
        homeO = 100 / homeP 

        hist[mark] = (homeF, homeP)
        summaryWriter.writerow([mark, totalF, 
            '{:>4.2f}'.format(homeP), '{:>4.2f}'.format(homeO),
            '{:>4.2f}'.format(drawP), '{:>4.2f}'.format(drawO),
            '{:>4.2f}'.format(awayP), '{:>4.2f}'.format(awayO)])

    s = ''
    for h in sorted(hist.items(), key = lambda x : x[1][0], reverse = True):
        s += '{:d} ({:d} {:>5.2f}) '.format(h[0], h[1][0], h[1][1])
    log.info(s)

    statsCSV = '{}/{}/Stats.{}.csv'.format(FootyAnalysisTools.analysisDir, league, FootyAnalysisTools.model.__class__.__name__)
    statsFieldNames = ['Result', 'Slope', 'Intercept', 'P', 'R', 'R^2', 'Err']
    statsFile = open(statsCSV, 'w', newline='')
    statsWriter = csv.writer(statsFile)
    statsWriter.writerow(statsFieldNames)

    slope, intercept, r, p, stderr = stats.linregress(x, hY)
    r2 = r**2
    log.info('Home: {:>4.2f} {:>4.2f} {:>4.2} {:>4.2f} {:>4.2f} {:>4.2}'.format(slope, intercept, p, r, r2, stderr))
    statsWriter.writerow(['H', '{:>4.2f}'.format(slope), '{:>4.2f}'.format(intercept), '{:>4.2f}'.format(p), '{:>4.2f}'.format(r), '{:>4.2f}'.format(r2), '{:>4.2f}'.format(stderr)])

    slope, intercept, r, p, stderr = stats.linregress(x, dY)
    r2 = r**2
    log.info('Draw: {:>4.2f} {:>4.2f} {:>4.2} {:>4.2f} {:>4.2f} {:>4.2}'.format(slope, intercept, p, r, r2, stderr))
    statsWriter.writerow(['D', '{:>4.2f}'.format(slope), '{:>4.2f}'.format(intercept), '{:>4.2f}'.format(p), '{:>4.2f}'.format(r), '{:>4.2f}'.format(r2), '{:>4.2f}'.format(stderr)])

    slope, intercept, r, p, stderr = stats.linregress(x, aY)
    r2 = r**2
    log.info('Away: {:>4.2f} {:>4.2f} {:>4.2} {:>4.2f} {:>4.2f} {:>4.2}'.format(slope, intercept, p, r, r2, stderr))
    statsWriter.writerow(['A', '{:>4.2f}'.format(slope), '{:>4.2f}'.format(intercept), '{:>4.2f}'.format(p), '{:>4.2f}'.format(r), '{:>4.2f}'.format(r2), '{:>4.2f}'.format(stderr)])

