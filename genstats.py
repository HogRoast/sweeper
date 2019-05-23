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

def genStats(log:Logger, algoId:int, league:str=None, backtest:bool=False):
    '''
    Generate statistics on the marked matches

    :param log: a logging object
    :param algoId: the algo to apply
    :param league: the league to apply the algo over, all if unset
    :param backtest: run in backtest mode
    '''
    log.info('Generating statistics for league <{}> with algo <{}> and ' \
            'backtest <{}>'.format(league if league else 'ALL', algoId, \
            backtest))

    config = getSweeperConfig()
    dbName = config['dbName']
    log.debug('Opening database: {}'.format(dbName))

    with Database(dbName, SQLite3Impl()) as db, db.transaction() as t:     
        try:
            algo = db.select(Algo(algoId))[0]
            algo = AlgoFactory.create(algo.getName())
            # In backtest mode use the inverse algoId to retrieve config,
            # ratings and stats:
            if backtest: algoId = -algoId
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
            stats = {}

            def getStatisticsForResult(result, setfn, getfn):
                keys = {'league' : league.getMnemonic(), 'result' : result}
                order = ['>date']
                for m in db.select(Match.createAdhoc(keys, order)):
                    rating = db.select(Rating(m.getDate(), m.getLeague(), 
                            m.getHome_Team(), m.getAway_Team(), algoId))
                    if rating:
                        mark = rating[0].getMark()
                        s = stats.get(mark, Statistics(str( \
                                datetime.now().date()), algoId, \
                                league.getMnemonic(), mark, 0, 0, 0, 0))
                        s.setMark_Freq(s.getMark_Freq() + 1)
                        setfn(s, getfn(s) + 1)
                        stats[mark] = s

            getStatisticsForResult('H', Statistics.setHome_Freq, 
                    Statistics.getHome_Freq)
            getStatisticsForResult('D', Statistics.setDraw_Freq, 
                    Statistics.getDraw_Freq)
            getStatisticsForResult('A', Statistics.setAway_Freq, 
                    Statistics.getAway_Freq)

            for k, v in stats.items():
                db.upsert(v)
        
if __name__ == '__main__':
    from sweeper.utils import getSweeperOptions, SweeperOptions

    log = Logger()
    sopts = getSweeperOptions(log, sys.argv)
    if not (sopts.test(SweeperOptions.ALGO) or sopts.algoId < 0):
        print('ERROR: null/negative algo id provided, python genstats ' \
                '-h for help')
        sys.exit(1)
    league = sopts.leagueMnemonic if sopts.test(SweeperOptions.LEAGUE) else None

    genStats(log, sopts.algoId, league, sopts.test(SweeperOptions.BACKTEST))
