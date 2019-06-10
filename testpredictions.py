import sys

#from createwebpage import createSeasonSummaryPage
from datetime import datetime
from shimbase.database import Database, AdhocKeys
from shimbase.sqlite3impl import SQLite3Impl
from sweeper.dbos.match import Match
from sweeper.table import Table
from sweeper.utils import getSweeperConfig
from sweeper.logging import Logger

def testPredictions(log:Logger, predictions:Table, show:bool=False):
    '''
    From the provided table of predictions, generate the actual betting
    outcome and display.

    :param log: a logging object
    :param predictions: a Table of match predictions with analytics
    :param show: displays any tables as HTML when True
    '''
    log.info('Running testPredictions...')
    
    config = getSweeperConfig()
    dbName = config['dbName']
    log.debug('Opening database: {}'.format(dbName))

    headers = ['Date', 'Match', 'Mark', 'RO', 'AO', 'Res', 'Stk', 'Win', \
            'Pot', 'Yld']
    schema = ['{:<12}', '{:<40}', '{:>4}', '{:>5.2f}', '{:>5.2f}', '{:>3}', \
            '{:>5}', '{:>5.2f}', '{:>5.2f}', '{:>5.2f}']   
    startPot = 20.0
    winnings = Table(headers=headers, schema=schema, 
            title='Backtest: {}, starting pot {} units'.format( \
                    predictions.getTitle(), startPot))

    pot = startPot
    with Database(dbName, SQLite3Impl()) as db, db.transaction() as t:     
        # Get the match result and best odds for each prediction and then
        # calculate winnings
        for p in predictions.getRows():
            dt = p[predictions.getHeaders().index('Date')]
            fix = p[predictions.getHeaders().index('Match')]
            ht, at = fix.split(' (vs) ')
            m = p[predictions.getHeaders().index('Mark')]
            ro = p[predictions.getHeaders().index('HO')]

            keys = {'date' : dt, 'home_team' : ht, 'away_team' : at}
            match = db.select(Match.createAdhoc(keys))[0]
            ao = match.getBest_Odds_H()
            r = match.getResult()

            row = [dt, fix, m, ro, ao, r]
            if ao >= ro:
                if r == 'H':
                    pot += ao
                    row += [1, ao]
                    colour = Table.Palette.GREEN
                else:
                    pot -= 1
                    row += [1, 0]
                    colour = Table.Palette.RED
                winnings.addHighlight(col='Match', pattern=fix, \
                        wholeRow=True, repeat=False, colour=colour)
            else:
                row += [0, 0] 
            row += [pot, (pot - startPot) / startPot * 100.0]
            winnings.append([row])
    log.info(winnings)

    if show:
        winnings.asHTML(show)

if __name__ == '__main__':
    log = Logger()
    headers = ['Date', 'Match', 'Mark', 'M#', \
            'H#', 'H%', 'HO', 'D#', 'D%', 'DO', 'A#', 'A%', 'AO']
    schema = ['{:<12}', '{:<40}', '{:>4}', '{:>4}', \
            '{:>4}', '{:>5.2f}', '{:>5.2f}', '{:>4}', '{:>5.2f}', \
            '{:>5.2f}', '{:>4}', '{:>5.2f}', '{:>5.2f}']
    t = Table(headers=headers, schema=schema, title='Test Fixture Table')
    t.append([['2019-01-30', 'Bournemouth (vs) Chelsea', 2, 20, 10, 50, \
            1.2, 6, 30, 2.4, 4, 20, 3.6]])
    t.append([['2019-05-04', 'Bournemouth (vs) Tottenham', -1, 10, 3, 30, \
            3.4, 4, 40, 2.3, 3, 30, 3.4]])
    testPredictions(log, t)
