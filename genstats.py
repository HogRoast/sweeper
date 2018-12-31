import sys
from datetime import datetime
from shimbase.database import Database, AdhocKeys
from shimbase.sqlite3impl import SQLite3Impl

from sweeper.algos import AlgoFactory
from sweeper.logging import Logger
from sweeper.utils import getSweeperConfig
from sweeper.dbos.algo import Algo
from sweeper.dbos.league import League
from sweeper.dbos.match import Match, MatchKeys
from sweeper.dbos.rating import Rating
from sweeper.dbos.statistics import Statistics

def genStats(log:Logger, algoId:int, league:str=None):
    '''
    Generate statistics on the marked matches

    :param log: a logging object
    :param algoId: the algo to apply
    :param league: the league to apply the algo over, all if unset
    '''
    log.info('Generating statistics for league <{}> with algo <{}>'\
            .format(league if league else 'ALL', algoId))

    config = getSweeperConfig()
    dbName = config['dbName']
    log.debug('Opening database: {}'.format(dbName))

    with Database(dbName, SQLite3Impl()) as db, db.transaction() as t:     
        try:
            algo = db.select(Algo(algoId))[0]
            algo = AlgoFactory.create(algo.getName())
        except:
            log.critical('No algo matching the provided id exists')
            sys.exit(3)
        try:
            if league: 
                leagues = db.select(League(league))
            else:
                leagues = db.select(League())
        except:
            log.critical('No league matching the provided mnemonic exists')
            sys.exit(4)

        for league in leagues:
            keys = {'league' : league.getMnemonic()}
            order = ['>date']
            matches = db.select(Match.createAdhoc(keys, order))
            hMatchKeys = [m._keys for m in matches if m.getResult() == 'H']
            dMatchKeys = [m._keys for m in matches if m.getResult() == 'D']
            aMatchKeys = [m._keys for m in matches if m.getResult() == 'A']

            ratings = db.select(Rating(algo_id=algoId)) 
            for mark in set([r.getMark() for r in ratings]):
                hRatings = [r for r in ratings if mark == r.getMark() and \
                        MatchKeys(r.getMatch_Date(), r.getLeague(), \
                        r.getHome_Team(), r.getAway_Team()) in hMatchKeys]
                dRatings = [r for r in ratings if mark == r.getMark() and \
                        MatchKeys(r.getMatch_Date(), r.getLeague(), \
                        r.getHome_Team(), r.getAway_Team()) in dMatchKeys]
                aRatings = [r for r in ratings if mark == r.getMark() and \
                        MatchKeys(r.getMatch_Date(), r.getLeague(), \
                        r.getHome_Team(), r.getAway_Team()) in aMatchKeys]
                totRatings = len(hRatings) + len(dRatings) + len(aRatings)

                db.upsert(Statistics(str(datetime.now().date()), algoId, \
                        league.getMnemonic(), mark, totRatings, len(hRatings), \
                        len(aRatings), len(dRatings)))
        
if __name__ == '__main__':
    from sweeper.utils import getSweeperOptions, SweeperOptions

    log = Logger()
    sopts = getSweeperOptions(log, sys.argv)
    if not sopts.test(SweeperOptions.ALGO):
        print('ERROR: No algo id provided, python genstats -h for help')
        sys.exit(1)
    league = sopts.leagueMnemonic if sopts.test(SweeperOptions.LEAGUE) else None

    genStats(log, sopts.algoId, league)
