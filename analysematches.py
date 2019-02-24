import sys, inspect

from datetime import datetime
from shimbase.database import Database, AdhocKeys
from shimbase.sqlite3impl import SQLite3Impl

from sweeper.logging import Logger
from sweeper.algos import AlgoFactory
from sweeper.utils import getSweeperConfig
from sweeper.dbos.match import Match, MatchKeys
from sweeper.dbos.rating import Rating
from sweeper.dbos.algo import Algo
from sweeper.dbos.league import League
from sweeper.dbos.season import Season

def analyseMatches(log:Logger, algoId:int, league:str=None, season:str=None):
    '''
    Mark all unmarked matches

    :param log: a logging object
    :param algoId: the algo to apply
    :param league: the league to apply the algo over, None means ALL
    :param season: the season to apply the algo over, None means ALL
    '''
    log.info('Analysing matches for league <{}>, season <{}> with algo <{}>'\
            .format(league if league else 'ALL', season if season else 'ALL',\
            algoId))

    config = getSweeperConfig()
    dbName = config['dbName']
    log.debug('Opening database: {}'.format(dbName))

    with Database(dbName, SQLite3Impl()) as db, db.transaction() as t:     
        try:
            algo = db.select(Algo(algoId))[0]
            algo = AlgoFactory.create(algo.getName())
        except:
            log.critical('No algo matching the provided id exists')
            sys.exit(2)
        try:
            if league: 
                leagues = db.select(League(league))
            else:
                leagues = db.select(League())
        except:
            log.critical('No league matching the provided mnemonic exists')
            sys.exit(3)
        try:
            if season: season = db.select(Season(season))[0]
        except:
            log.critical('No season matching the provided season exists')
            sys.exit(4)

        ratings = db.select(Rating(algo_id=algoId))
        ratedMatchKeys = [MatchKeys(r.getMatch_Date(), r.getLeague(), \
                r.getHome_Team(), r.getAway_Team()) for r in ratings]
        log.info('Found {} ratings for algo {}'.format(len(ratedMatchKeys), \
                algoId))

        for league in leagues:
            if season:
                keys = {'league' : league.getMnemonic(), \
                        '>date' : season.getL_Bnd_Date(), \
                        '<date' : season.getU_Bnd_Date()}
            else:
                keys = {'league' : league.getMnemonic()}
            order = ['>league', '>date']
            matches = db.select(Match.createAdhoc(keys, order))
            unmarked = list(filter(lambda x : x._keys not in ratedMatchKeys, \
                    matches))
            results = list(filter(lambda x : x.getResult() != '', matches))
            log.info('{} {} matches found unmarked'.format(len(unmarked), \
                    league.getMnemonic()))
            for m in unmarked:
                hTeamMatches = list(filter(lambda x : m.getHome_Team() in \
                        (x.getHome_Team(), x.getAway_Team()) and x.getDate() \
                        < m.getDate(), results))
                aTeamMatches = list(filter(lambda x : m.getAway_Team() in \
                        (x.getHome_Team(), x.getAway_Team()) and x.getDate() \
                        < m.getDate(), results))
                mark = algo.markMatch(m, hTeamMatches, aTeamMatches)
                if mark is not None:
                    db.upsert(Rating(m.getDate(), m.getLeague(), \
                            m.getHome_Team(), m.getAway_Team(), algoId, mark))

if __name__ == '__main__':
    from sweeper.utils import getSweeperOptions, SweeperOptions

    log = Logger()
    sopts = getSweeperOptions(log, sys.argv)
    if not sopts.test(SweeperOptions.ALGO):
        print('ERROR: No algo id provided, python analysematches -h for help')
        sys.exit(1)
    league = sopts.leagueMnemonic if sopts.test(SweeperOptions.LEAGUE) else None
    season = sopts.season if sopts.test(SweeperOptions.SEASON) else None
    analyseMatches(log, sopts.algoId, league, season)
