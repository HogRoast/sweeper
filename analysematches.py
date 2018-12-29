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

def analyseMatches(log:Logger, algoId:int, league:str, season:str=None):
    '''
    Mark all unmarked matches

    :param log: a logging object
    :param algoId: the algo to apply
    :param league: the league to apply the algo over
    :param season: the season to apply the algo over, None means ALL
    '''
    log.info('Analysing matches for league <{}>, season <{}> with algo <{}>'\
            .format(league, season if season else 'ALL', algoId))

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
        try:
            if season: season = db.select(Season(season))[0]
        except:
            log.critical('No season matching the provided season exists')
            sys.exit(6)

        ratings = db.select(Rating(algo_id=algoId))
        ratedMatchKeys = [MatchKeys(r.getMatch_Date(), r.getLeague(), \
                r.getHome_Team(), r.getAway_Team()) for r in ratings]
        log.info('Found {} ratings for algo {}'.format(len(ratedMatchKeys), \
                algoId))

        if season:
            keys = {'league' : league.getMnemonic(), '>date' : \
                    season.getL_Bnd_Date(), '<date' : season.getU_Bnd_Date()}
        else:
            keys = {'league' : league.getMnemonic()}
        order = {'>date'}
        matches = [m for m in db.select(Match.createAdhoc(keys, order)) \
                if m._keys not in ratedMatchKeys]
        log.info('{} {} matches found unmarked'.format(len(matches), \
                league.getMnemonic()))

        for i in range(len(matches)):
            m = matches[i]
            hTeamMatches = [hm for hm in matches[i+1:] if m.getHome_Team() \
                    in (hm.getHome_Team(), hm.getAway_Team())]
            aTeamMatches = [am for am in matches[i+1:] if m.getAway_Team() \
                    in (am.getHome_Team(), am.getAway_Team())]
            mark = algo.markMatch(m, hTeamMatches, aTeamMatches)
            if mark is not None:
                db.upsert(Rating(m.getDate(), m.getLeague(), m.getHome_Team(), \
                        m.getAway_Team(), algoId, mark))

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
    season = None
    if sopts.test(SweeperOptions.SEASON):
        season = sopts.season

    analyseMatches(log, sopts.algoId, sopts.leagueMnemonic, season)
