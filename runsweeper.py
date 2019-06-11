import sys

from analysematches import analyseMatches
from createwebpage import createWebPage
from datetime import datetime
from genstats import genStats
from presentfixtures import presentFixtures
from sourcedata import sourceData
from shimbase.database import Database, AdhocKeys
from shimbase.sqlite3impl import SQLite3Impl
from sweeper.dbos.season import Season
from sweeper.logging import Logger
from sweeper.utils import getSweeperConfig
from testpredictions import testPredictions

def runSweeper(log:Logger, algoId:int, league:str=None, season:str=None, \
        show:bool=False, mail:bool=False, backtest:bool=False):
    '''
    Run the entire sweeper suite

    :param log: a logging object
    :param league: the subject league, None signifies all available leagues 
    :param season: the subject season, None current season
    :param show: displays any tables as HTML when True
    :param mail: send as email
    :param backtest: run in backtest mode
    '''
    log.info('Running sweeper suite for algo <{}>, league <{}>, season <{}>, '\
            'backtest <{}>'.format(algoId, league if league else 'ALL', \
            season if season else 'CURRENT', backtest))

    log.info('\nSourcing data...\n')
    sourceData(log=log, target='Football-Data', currentSeason=not season)
    log.info('\nSourcing data...Done\n')
    
    log.info('\nAnalysing matches...\n')
    analyseMatches(log=log, algoId=algoId, league=league, season=season, \
            backtest=backtest) 
    log.info('\nAnalysing matches...Done\n')

    log.info('\nGenerating stats...\n')
    genStats(log=log, algoId=algoId, league=league, backtest=backtest)
    log.info('\nGenerating stats...Done\n')

    if not backtest:
        log.info('\nCreating web page...\n')
        dt = datetime.today().strftime('%Y-%m-%d')
        createWebPage(log=log, algoId=algoId, date=dt, league=league, show=show)
        log.info('\nCreating web page...Done\n')

    log.info('\nPresent fixtures...\n')
    tables = presentFixtures(log=log, algoId=algoId, league=league, \
            show=show, season=season, mail=mail, backtest=backtest)
    log.info('\nPresent fixtures...Done\n')

    if backtest:
        log.info('\nTesting fixtures...\n')
        testPredictions(log=log, algoId=algoId, season=season, \
                predictions=tables, show=show)
        log.info('\nTesting fixtures...Done\n')
        
if __name__ == '__main__':
    from sweeper.utils import getSweeperOptions, SweeperOptions

    log = Logger()
    sopts = getSweeperOptions(log, sys.argv)
    if not (sopts.test(SweeperOptions.ALGO) or sopts.algoId < 0):
        print('ERROR: null/negative algo id provided, python runsweeper ' \
                '-h for help')
        sys.exit(1)
    league = sopts.leagueMnemonic if sopts.test(SweeperOptions.LEAGUE) else None
    season = sopts.season if sopts.test(SweeperOptions.SEASON) else None
    runSweeper(log, sopts.algoId, league, season, \
            sopts.test(SweeperOptions.SHOW), \
            sopts.test(SweeperOptions.MAIL), \
            sopts.test(SweeperOptions.BACKTEST))
