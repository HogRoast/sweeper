import urllib.request
import csv

'''
 How often do the following url change?
'''
seasons = ['1617', '1516', '1415', '1314', '1213', '1112', '1011', '0910', '0809', '0708', '0607', '0506', '0405', '0304', '0203', '0102', '0001']
leagues = [ 'E0', 'E1', 'E2', 'E3', 'SC0', 'SC1', 'SC2', 'SC3', 'D1', 'D2', 'I1', 'I2', 'SP1', 'SP2', 'F1', 'F2', 'N1', 'B1', 'P1', 'T1', 'G1'] 

baseURL = 'http://www.football-data.co.uk/mmz4281/{}/{}.csv'
baseOutputFilename = 'Data/{}_{}.csv'
                
for l in leagues:
    for s in seasons:
        resultsURL = baseURL.format(s, l)
        print('Downloading...', resultsURL)
        httpResp = urllib.request.urlopen(resultsURL)
        results = str(httpResp.read())
        csvFile = results.split('\\r\\n')
        resultsReader = csv.reader(csvFile, delimiter=',')
        outputFilename = baseOutputFilename.format(l, s)
        print('Output to...', outputFilename)
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
