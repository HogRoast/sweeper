import sys
from configparser import ConfigParser
from Logging import Logger
from FootyUtils import getFootyOptions, getFootyConfig, FootyArgsError, \
        newCSVFile, readCSVFileAsDict

def downloadData(baseURL, baseOutputFilename, opts=sys.argv):
    log = Logger()
    getFootyOptions(log, opts)

    (algoCfg, mailCfg) = getFootyConfig()
    seasons = algoCfg['seasons']
    rangeMap = algoCfg['rangeMap']
    leagues = rangeMap.keys()

    for l in leagues:
        for s in seasons:
            resultsURL = baseURL.format(s, l)
            log.info('Downloading...' + resultsURL)
            with readCSVFileAsDict(resultsURL) as resultsReader:
                outputFilename = baseOutputFilename.format(l, s)
                log.info('Output to...' + outputFilename)
                # Correct the first header field
                i = resultsReader.__iter__()
                headers = i.__next__()
                headers[0] = 'Div'
                with newCSVFile(outputFilename, headers) as outputWriter:
                    for row in i:
                        outputWriter.writerow(row)

if __name__ == '__main__':
    baseURL = 'http://www.football-data.co.uk/mmz4281/{}/{}.csv'
    baseOutputFilename = '../Data/{}_{}.csv'

    downloadData(baseURL, baseOutputFilename, sys.argv)
