import urllib.request
import csv, sys
from Logging import Logger
from configparser import ConfigParser

def downloadData(baseURL, baseOutputFilename):
    log = Logger()
    if len(sys.argv) > 1:
        if '-d' in sys.argv: log.toggleMask(Logger.DEBUG | Logger.TIME | Logger.TYPE)

    config = ConfigParser()
    config.read('../config/footy.ini')
    algoCfg = config['algo.cfg']
    seasons = eval(algoCfg['seasons'])
    rangeMap = eval(algoCfg['rangeMap'])
    leagues = rangeMap.keys()

    for l in leagues:
        for s in seasons:
            resultsURL = baseURL.format(s, l)
            log.info('Downloading...' + resultsURL)
            httpResp = urllib.request.urlopen(resultsURL)
            results = str(httpResp.read())
            csvFile = results.split('\\r\\n')
            resultsReader = csv.reader(csvFile, delimiter=',')
            outputFilename = baseOutputFilename.format(l, s)
            log.info('Output to...' + outputFilename)
            outputFile = open(outputFilename, 'w')    
            outputWriter = csv.writer(outputFile)
            firstRow = True
            for row in resultsReader:
                if firstRow:
                    row[0] = 'Div'
                    outputWriter.writerow(row)
                    firstRow = False
                else:
                    outputWriter.writerow(row)

if __name__ == '__main__':
    baseURL = 'http://www.football-data.co.uk/mmz4281/{}/{}.csv'
    baseOutputFilename = '../Data/{}_{}.csv'

    downloadData(baseURL, baseOutputFilename)
