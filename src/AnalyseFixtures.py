import urllib.request
import csv, sys
import smtplib
import configparser
import FootyAnalysisTools
from Logging import Logger

log = Logger()
config = configparser.ConfigParser()
config.read('../config/footy.ini')
algoCfg = config['algo.cfg']
season = algoCfg['season']
rangeMap = eval(algoCfg['rangeMap'])
sendMail = False
if len(sys.argv) > 1:
    if '-d' in sys.argv: log.toggleMask(Logger.DEBUG | Logger.TIME | Logger.TYPE)
    if '-s' in sys.argv: sendMail = True


teamErrorMap = {'Waasland Beveren' : 'Waasland-Beveren',
                '' : ''
}

def fSD(d):
    return '({:>4d} {:>6.2f}% {:>5.2f})'.format(d[0], d[1], d[2])
def fST(d):
    return '({:<4s} {:<7s} {:<5s})'.format(d[0], d[1], d[2])

def hl(s):
    return '\033[1m' + s + '\033[0m'
def mail_hl(s):
    s = s.replace('<td>', '<td bgcolor="yellow">')
    s = s.replace('<td align="right">', '<td align="right" bgcolor="yellow">')
    return s

'''
 How often do the following urls change?
'''
resultsURLTmpl = 'http://www.football-data.co.uk/mmz4281/{}/{}.csv'
fixturesURL = 'http://www.football-data.co.uk/fixtures.csv'
#fixturesURL = 'file:///home/mckone/Documents/Stuff/Footy/fixtures.txt'

mailText = '<table border=1><tr><th>Lge</th><th>Date</th><th>HomeTeam</th><th>AwayTeam</th><th>Mark</th><th>H#</th><th>H%</th><th>H Odds</th><th>HomeTeamForm</th><th>AwayTeamForm</th></tr>'
s = '{:<4s} {:<8s} {:<16s} {:<16s} {:<4s} {:s} {:<37s} {:<37s}'.format('Lge', 'Date', 'HomeTeam', 'AwayTeam', 'Mark', fST(('H#','H%', 'HO')), 'HomeTeamForm', 'AwayTeamForm')
termText = '\n' + hl(s) + '\n'

bettingCSV = '{}/Betting.{}.csv'.format(FootyAnalysisTools.analysisDir, FootyAnalysisTools.model.__class__.__name__)
bettingFieldNames = ['Lge', 'Date', 'HomeTeam', 'AwayTeam', 'Mark', 'H#', 'H%', 'HOdds', 'HomeTeamForm', 'AwayTeamForm']
bettingFile = open(bettingCSV, 'w', newline='')
bettingWriter = csv.writer(bettingFile)
bettingWriter.writerow(bettingFieldNames)

httpResp = urllib.request.urlopen(fixturesURL)
results = str(httpResp.read())
fixturesCSVFile = results.split('\\r\\n')

league = ''
data = {}
summaryData = {}
fixturesReader = csv.DictReader(fixturesCSVFile, delimiter=',')
for fix in fixturesReader:
    log.debug(fix)
    ind = 'b\"Div'
    try:
        fix['b\"Div']
    except:
        ind = 'b\'Div'
        
    if fix[ind] not in rangeMap:
        continue
    if league != fix[ind]:
        league = fix[ind]
        resultsURL = resultsURLTmpl.format(season, league)
        log.info(resultsURL)
        httpResp = urllib.request.urlopen(resultsURL)
        results = str(httpResp.read())
        resultsCSVFile = results.split('\\r\\n')

        resultsReader = csv.DictReader(resultsCSVFile, delimiter=',')
        data = FootyAnalysisTools.model.processMatches(resultsReader)

        summaryCSV = '{}/{}/Summary.{}.csv'.format(FootyAnalysisTools.analysisDir, league, FootyAnalysisTools.model.__class__.__name__)
        summaryFile = open(summaryCSV, 'r', newline='')
        summaryReader = csv.DictReader(summaryFile, delimiter=',')
        for summ in summaryReader:
            mark = int(summ['Mark'])
            f = int(summ['Frequency'])
            hP = float(summ['%H'])
            dP = float(summ['%D'])
            aP = float(summ['%A'])
            summaryData[mark] = {   'H' : (int(f * (hP / 100)), float(summ['%H']), float(summ['HO'])),
                                    'D' : (int(f * (dP / 100)), float(summ['%D']), float(summ['DO'])),
                                    'A' : (int(f * (aP / 100)), float(summ['%A']), float(summ['AO']))}
    ht = fix['HomeTeam']
    if ht in teamErrorMap:
        ht = teamErrorMap[ht]
    at = fix['AwayTeam']
    if at in teamErrorMap:
        at = teamErrorMap[at]
    date, ht, at, mark, hForm, aForm = FootyAnalysisTools.model.markMatch(data, fix['Date'], ht, at)
    if mark is None or mark not in range(-15, 16):
        continue
    hSD = summaryData[mark]['H'] 
    aSD = summaryData[mark]['A'] 
    dSD = summaryData[mark]['D'] 

    s = '{:<4s} {:<8s} {:<16s} {:<16s} {:4d} {:s} ({:s}) ({:s})'.format(league, date, ht, at, mark, fSD(hSD), hForm, aForm)
    mail_s = '<tr><td>{:s}</td><td>{:s}</td><td>{:s}</td><td>{:s}</td><td align="right">{:>4d}</td><td align="right">{:>4d}</td><td align="right">{:>6.2f}%</td><td align="right">{:>5.2f}</td><td align="right">{:s}</td><td align="right">{:s}</td></tr>'.format(league, date, ht, at, mark, hSD[0], hSD[1], hSD[2], hForm, aForm)
    if mark in rangeMap[league]:
        termText += hl(s) + '\n'
        mailText += mail_hl(mail_s)
    else:
        termText += s + '\n'
        mailText += mail_s
    bettingWriter.writerow((league, date, ht, at, mark, hSD[0], hSD[1], hSD[2], hForm, aForm))

log.info(termText)
mailText += '</table>'
mailText = 'MIME-Version: 1.0\nContent-type: text/html\nSubject: Footy Bets\n\n{}'.format(mailText)

if sendMail:
    mailCfg = config['mail.cfg']
    fromAddr = mailCfg['fromAddr']
    toAddrs = eval(mailCfg['toAddrs'])
    server = smtplib.SMTP(mailCfg['svr'], mailCfg.getint('port'))
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(fromAddr, mailCfg['pwd'])
    server.sendmail(fromAddr, toAddrs, mailText)
    server.quit()
    log.info('email sent to: {!s}'.format(toAddrs))
