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

def runSweeper(log:Logger, algoId:int, league:str=None, show:bool=False, \
        mail:bool=False):
    '''
    Run the entire sweeper suite

    :param log: a logging object
    :param league: the subject league, None signifies all available leagues 
    :param show: displays any tables as HTML when True
    :param mail: send as email
    '''
    log.info('Running sweeper suite for algo <{}>, league <{}>'\
            .format(algoId, league if league else 'ALL'))

    log.info('\nSourcing data...\n')
    sourceData(log=log, target='Football-Data', currentSeason=True)
    log.info('\nSourcing data...Done\n')
    
    config = getSweeperConfig()
    dbName = config['dbName']
    log.debug('Opening database: {}'.format(dbName))
    with Database(dbName, SQLite3Impl()) as db:
        season = db.select(Season.createAdhoc(\
                order=('>l_bnd_date',)))[0].getName()

    log.info('\nAnalysing matches...\n')
    analyseMatches(log=log, algoId=algoId, league=league, season=season) 
    log.info('\nAnalysing matches...Done\n')

    log.info('\nGenerating stats...\n')
    genStats(log=log, algoId=algoId, league=league)
    log.info('\nGenerating stats...Done\n')

    log.info('\nCreating web page...\n')
    dt = datetime.today().strftime('%Y-%m-%d')
    createWebPage(log=log, algoId=algoId, date=dt, league=league, show=show) 
    log.info('\nCreating web page...Done\n')

    log.info('\nPresent fixtures...\n')
    tables = presentFixtures(\
            log=log, algoId=algoId, league=league, season=season, mail=mail)
    log.info('\nPresent fixtures...Done\n')

if __name__ == '__main__':
    from sweeper.utils import getSweeperOptions, SweeperOptions

    log = Logger()
    sopts = getSweeperOptions(log, sys.argv)
    if not (sopts.test(SweeperOptions.ALGO) or sopts.algoId < 0):
        print('ERROR: null/negative algo id provided, python runsweeper ' \
                '-h for help')
        sys.exit(1)
    league = sopts.leagueMnemonic if sopts.test(SweeperOptions.LEAGUE) else None
    runSweeper(log, sopts.algoId, league, sopts.test(SweeperOptions.SHOW), \
            sopts.test(SweeperOptions.MAIL))
