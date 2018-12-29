import sys
from datetime import datetime, timedelta
from shimbase.database import Database, AdhocKeys
from shimbase.sqlite3impl import SQLite3Impl

from sweeper.logging import Logger
from sweeper.table import Table
from sweeper.utils import getSweeperConfig
from sweeper.dbos.match import Match
from sweeper.dbos.rating import Rating
from sweeper.dbos.statistics import Statistics

def presentFixtures(log:Logger, algoId:int, date:str, league:str=None, \
        show:bool=False):
    '''
    Present the latest set of fixtures with all the appropriate ratings.

    :param log: a logging object
    :param date: include all fixtures from this date and onward
    :param league: the subject league, None signifies all available leagues 
    :param show: displays any tables as HTML when True
    '''
    log.info('Presenting fixtures for algo <{}>, date <{}> and league <{}>\
            '.format(algoId, date, league if league else 'ALL'))

    config = getSweeperConfig()
    dbName = config['dbName']
    log.debug('Opening database: {}'.format(dbName))

    with Database(dbName, SQLite3Impl()) as db, db.transaction() as t:     
        dt = datetime.strptime(date, '%Y-%m-%d') - timedelta(days=1)
        try:
            keys = {'>date' : dt.strftime('%Y-%m-%d'), 'result' : ''}
            if league: keys.update({'league' : league})
            order = ['<date']
            fixtures = db.select(Match.createAdhoc(keys, order))
            if not fixtures: raise Exception('No fixtures')
        except Exception as e:
            log.critical("Couldn't find fixtures for league and date " \
                    "provided, run sourcedata?")
            log.critical('Because...{}'.format(e))
            sys.exit(3)

        try:
            del keys['result']
            keys.update({'>match_date' : keys.pop('>date')})
            keys.update({'algo_id' : algoId})
            order = ['<match_date']
            ratings = db.select(Rating.createAdhoc(keys, order))
            log.debug('Num fixtures {}, ratings {}'.format(len(fixtures), \
                    len(ratings)))
            if len(fixtures) != len(ratings): 
                raise Exception('Mismatched ratings')
        except Exception as e:
            log.critical("Couldn't find algo ratings for all fixtures, " \
                    "run analysematches?")
            log.critical('Because...{}'.format(e))
            sys.exit(4)

        try:
            keys.update({'>generation_date' : keys.pop('>match_date')})
            order = ['>generation_date']
            stats = db.select(Statistics.createAdhoc(keys, order))
            if not stats: raise Exception('No statistics')
            lastGenDate = stats[0].getGeneration_Date()
            stats = [s for s in stats if s.getGeneration_Date() == lastGenDate]
        except Exception as e:
            log.critical("Couldn't find algo statistics for league and date, " \
                    "run genstats?")
            log.critical('Because...{}'.format(e))
            sys.exit(5)

        def statsSummary(s:Statistics):
            homeF = s.getHome_Freq()
            markF = s.getMark_Freq()
            homeP = (homeF / markF) * 100.0
            homeO = 100.0 / homeP
            return markF, homeF, homeP, homeO

        analytics = map(lambda r : [(r, statsSummary(s)) for s in stats \
                if r.getMark() == s.getMark() \
                and r.getLeague() == s.getLeague()], ratings)
        presentation = zip(fixtures, analytics)

        headers = ['Date', 'Home Team', 'Away Team', 'Mark', 'M#', 'H#', \
                'H%', 'HO']
        schema = ['{:<12}', '{:<20}', '{:>20}', '{:>4}', '{:>4}', \
                '{:>4}', '{:>5.3}', '{:>5.3}']
        t = Table(headers=headers, schema=schema)
        t.append([[f.getDate(), f.getHome_Team(), f.getAway_Team(), \
                r.getMark(), mf, hf, hp, ho] \
                for f, [(r, (mf, hf, hp, ho))] in presentation])
        log.info(t)

        if show: t.asHTML(show)
    
if __name__ == '__main__':
    from sweeper.utils import getSweeperOptions, SweeperOptions

    log = Logger()
    sopts = getSweeperOptions(log, sys.argv)
    if not sopts.test(SweeperOptions.ALGO):
        print('ERROR: No algo id provided, python presentfixtures -h for help')
        sys.exit(1)
    if not sopts.test(SweeperOptions.DATE):
        print('ERROR: No fixture date provided, python presentfixtures ' \
                '-h for help')
        sys.exit(2)

    league = None
    if sopts.test(SweeperOptions.LEAGUE): league = sopts.leagueMnemonic

    presentFixtures(log, sopts.algoId, sopts.date, league, \
            sopts.test(SweeperOptions.SHOW))
