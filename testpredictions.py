import copy
import sys

#from createwebpage import createSeasonSummaryPage
from datetime import datetime
from shimbase.database import Database, AdhocKeys
from shimbase.sqlite3impl import SQLite3Impl
from sweeper.algos import AlgoFactory
from sweeper.dbos.algo import Algo
from sweeper.dbos.match import Match
from sweeper.dbos.season import Season
from sweeper.table import Table
from sweeper.utils import getSweeperConfig
from sweeper.logging import Logger

def testPredictions(log:Logger, algoId:int, season:str, predictions:Table, \
        show:bool=False):
    '''
    From the provided table of predictions, generate the actual betting
    outcome and display.

    :param log: a logging object
    :param algo: the algo under test
    :param season: the season under test
    :param predictions: a Table of match predictions with analytics
    :param show: displays any tables as HTML when True
    '''
    log.info('Running testPredictions for algo <{}> and season <{}>'.format( \
            algoId, season))

    config = getSweeperConfig()
    dbName = config['dbName']
    log.debug('Opening database: {}'.format(dbName))

    headers = ['Date', 'Match', 'Mark', 'RO', 'AO', 'Res', 'Stk', \
            'Win', 'Pot', 'Yld']
    schema = ['{:<12}', '{:<40}', '{:>4}', '{:>5.2f}', '{:>5.2f}', \
            '{:>3}', '{:>5}', '{:>5.2f}', '{:>5.2f}', '{:>5.2f}']   
    startPot = 20.0
    winnings = Table(headers=headers, schema=schema, 
            title='{}, starting pot {} units'.format( \
                    predictions.getTitle(), startPot))

    pot = startPot
    with Database(dbName, SQLite3Impl()) as db, db.transaction() as t:     
        try:
            algo = db.select(Algo(algoId))[0]
            algo = AlgoFactory.create(algo.getName())
        except Exception as e:
            log.critical('No algo matching the provided id exists')
            log.critical('Because...%s' % e)
            sys.exit(1)
        try:
            season = db.select(Season(season))[0]
        except Exception as e:
            log.critical('No season matching the provided season exists')
            log.critical('Because...%s' % e)
            sys.exit(2)

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

            keys.update({'<date' : keys.pop('date')})
            keys.update({'>date' : season.getL_Bnd_Date()})
            del keys['home_team']
            del keys['away_team']
            priorMatches = db.select(Match.createAdhoc(keys))
            priorHTMatches = len([m for m in priorMatches \
                    if m.getHome_Team() == match.getHome_Team() \
                    or m.getAway_Team() == match.getHome_Team()])
            priorATMatches = len([m for m in priorMatches \
                    if m.getHome_Team() == match.getAway_Team() \
                    or m.getAway_Team() == match.getAway_Team()])

            incl = not (priorHTMatches < algo.numMatches or \
                    priorATMatches < algo.numMatches)
            colour = None
            row = [dt, fix, m, ro, ao, r]
            if incl and ao >= ro:
                if r == 'H':
                    pot += ao - 1
                    row += [1, ao]
                    colour = Table.Palette.GREEN
                else:
                    pot -= 1
                    row += [1, 0]
                    colour = Table.Palette.RED
            else:
                row += [0, 0] 
            row += [pot, (pot - startPot) / startPot * 100.0]

            if colour:
                winnings.addHighlight(col='Match', pattern=fix, \
                        wholeRow=True, repeat=False, colour=colour)
            if incl:
                winnings.append([row])
    log.info(winnings)

    if show:
        winnings.asHTML(show)

    return winnings

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
    testPredictions(log, 1, '1819', t)
