import sys, inspect

from datetime import datetime
from shimbase.database import Database, AdhocKeys
from shimbase.sqlite3impl import SQLite3Impl

from sweeper.logging import Logger
from sweeper.algos import AlgoFactory
from sweeper.utils import getSweeperConfig
from sweeper.dbos.match import Match
from sweeper.dbos.rating import Rating
from sweeper.dbos.algo import Algo
from sweeper.dbos.league import League

def analyseMatches(log:Logger, algoId:int, league:str):
    '''
    Mark all unmarked matches

    :param log: a logging object
    :param algoId: the algo to apply
    :param league: the league to apply the algo over
    '''
    log.info('Analysing matches for league <{}> with algo <{}>'.format( \
            league, algoId))

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
            league = db.select(League(league))[0]
        except:
            log.critical('No league matching the provided mnemonic exists')
            sys.exit(4)

        ratings = db.select(Rating.createAdhoc(order=('>match_id',)))
        matchId = 0
        if ratings:
            matchId = ratings[0].getMatch_Id()
        log.debug('Last rating for match {}'.format(matchId))

        keys = {'>id' : matchId, 'league' : league.getMnemonic()}
        order = ('>id',)
        matches = db.select(Match.createAdhoc(keys, order))
        log.debug('{} matches found to mark'.format(len(matches)))

        chunkSz = algo.numMatches 
        for i in range(0, len(matches)-chunkSz+1):
            # print(matches[i:i+chunkSz])
            algo.processMatches(matches[i:i+chunkSz])
        
if __name__ == '__main__':
    from sweeper.utils import getSweeperOptions, SweeperOptions

    log = Logger()
    sopts = getSweeperOptions(log, sys.argv)
    if not sopts.test(SweeperOptions.ALGO):
        print('ERROR: No algo id provided, python analysematches -h for help')
        sys.exit(1)
    if not sopts.test(SweeperOptions.LEAGUE):
        print('ERROR: No league provided, python analysematches -h for help')
        sys.exit(2)

    analyseMatches(log, sopts.algoId, sopts.leagueMnemonic)
