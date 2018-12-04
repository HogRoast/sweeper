import sys
from datetime import datetime
from shimbase.database import Database, AdhocKeys
from shimbase.sqlite3impl import SQLite3Impl

from sweeper.algos import AlgoFactory
from sweeper.logging import Logger
from sweeper.utils import getSweeperConfig
from sweeper.dbos.algo import Algo
from sweeper.dbos.league import League
from sweeper.dbos.match import Match
from sweeper.dbos.rating import Rating
from sweeper.dbos.statistics import Statistics

def generateStats(log:Logger, algoId:int, league:str):
    '''
    Generate statistics on the marked matches

    :param log: a logging object
    :param algoId: the algo to apply
    :param league: the league to apply the algo over
    '''
    log.info('Generating statistics for ' \
            'league <{}> with algo <{}>'.format(league, algoId))

    config = getSweeperConfig()
    dbName = config['dbName']
    log.debug('Opening database: {}'.format(dbName))

    with Database(dbName, SQLite3Impl()) as db, db.transaction() as t:     
        try:
            algo = db.select(Algo(algoId))[0]
            algo = AlgoFactory.create(algo.getName())
        except:
            log.critical('No algo matching the provided id exists')
            sys.exit(4)
        try:
            league = db.select(League(league))[0]
        except:
            log.critical('No league matching the provided mnemonic exists')
            sys.exit(5)

        keys = {'league' : league.getMnemonic()}
        order = {'>date'}
        matches = db.select(Match.createAdhoc(keys, order))
        matchids = [m.getId() for m in matches]
        hMatchIds = [m.getId() for m in matches if m.getResult() == 'H']
        dMatchIds = [m.getId() for m in matches if m.getResult() == 'D']
        aMatchIds = [m.getId() for m in matches if m.getResult() == 'A']

        ratings = db.select(Rating(algo_id=algoId)) 
        for mark in set([r.getMark() for r in ratings]):
            hRatings = [r for r in ratings if r.getMatch_Id() in hMatchIds \
                    and mark == r.getMark()]
            dRatings = [r for r in ratings if r.getMatch_Id() in dMatchIds \
                    and mark == r.getMark()]
            aRatings = [r for r in ratings if r.getMatch_Id() in aMatchIds \
                    and mark == r.getMark()]
            totRatings = len(hRatings) + len(dRatings) + len(aRatings)

            db.upsert(Statistics(str(datetime.now().date()), algoId, \
                    league.getMnemonic(), mark, totRatings, len(hRatings), \
                    len(aRatings), len(dRatings)))
        
if __name__ == '__main__':
    from sweeper.utils import getSweeperOptions, SweeperOptions

    log = Logger()
    sopts = getSweeperOptions(log, sys.argv)
    if not sopts.test(SweeperOptions.ALGO):
        print('ERROR: No algo id provided, python generatestats -h for help')
        sys.exit(1)
    if not sopts.test(SweeperOptions.LEAGUE):
        print('ERROR: No league provided, python generatestats -h for help')
        sys.exit(2)

    generateStats(log, sopts.algoId, sopts.leagueMnemonic)
