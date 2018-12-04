import matplotlib.pyplot as plt
import sys
from scipy import stats
from datetime import datetime
from shimbase.database import Database, AdhocKeys
from shimbase.sqlite3impl import SQLite3Impl

from sweeper.algos import AlgoFactory
from sweeper.logging import Logger
from sweeper.utils import getSweeperConfig
from sweeper.dbos.statistics import Statistics

def createPlot(
        x:list, yp:list, yf:list, intercept:float, slope:float, label:str):
    plt.plot(x, yp, 'o', label='{} percentage'.format(label))
    plt.plot(x, yf, 'go', label='{} frequency'.format(label))
    plt.plot(x, [intercept + slope*n for n in x], 'r', label='fitted line')
    plt.legend()
    plt.show()

def analyseStatistics(
        log:Logger, algoId:int, league:str, lbnd:int=None, ubnd:int=None):
    '''
    Analyse statistics for the algo and league combination

    :param log: a logging object
    :param algoId: the algo subject
    :param league: the league subject
    '''
    log.info('Analysing statistics for ' \
            'league <{}> with algo <{}>'.format(league, algoId))

    config = getSweeperConfig()
    dbName = config['dbName']
    log.debug('Opening database: {}'.format(dbName))

    with Database(dbName, SQLite3Impl()) as db, db.transaction() as t:     
        try:
            if None in (lbnd, ubnd):
                keys = {'algo_id' : algoId, 'league' : league}
            else:
                keys = {'algo_id' : algoId, 'league' : league, '>mark' : lbnd, \
                        '<mark' : ubnd}
            statistics = db.select(Statistics.createAdhoc(keys)) 
        except:
            log.critical('No statistics matching the provided algo and ' \
                    'league exists')
            sys.exit(3)

        x = [s.getMark() for s in statistics]
        hY = [s.getHome_Freq() / s.getMark_Freq() * 100 for s in statistics]
        hF = [s.getHome_Freq() for s in statistics]
        dY = [s.getDraw_Freq() / s.getMark_Freq() * 100 for s in statistics]
        dF = [s.getDraw_Freq() for s in statistics]
        aY = [s.getAway_Freq() / s.getMark_Freq() * 100 for s in statistics]
        aF = [s.getAway_Freq() for s in statistics]

        slope, intercept, r, p, stderr = stats.linregress(x, hY)
        r2 = r**2
        log.info('Home: {:>4.2f} {:>4.2f} {:>4.2} {:>4.2f} {:>4.2f} ' \
                    '{:>4.2}'.format(slope, intercept, p, r, r2, stderr))
        createPlot(x, hY, hF, intercept, slope, 'home')

        slope, intercept, r, p, stderr = stats.linregress(x, dY)
        r2 = r**2
        log.info('Draw: {:>4.2f} {:>4.2f} {:>4.2} {:>4.2f} {:>4.2f} ' \
                    '{:>4.2}'.format(slope, intercept, p, r, r2, stderr))
        createPlot(x, dY, dF, intercept, slope, 'draw')
        
        slope, intercept, r, p, stderr = stats.linregress(x, aY)
        r2 = r**2
        log.info('Away: {:>4.2f} {:>4.2f} {:>4.2} {:>4.2f} {:>4.2f} ' \
                    '{:>4.2}'.format(slope, intercept, p, r, r2, stderr))
        createPlot(x, aY, aF, intercept, slope, 'away')

if __name__ == '__main__':
    from sweeper.utils import getSweeperOptions, SweeperOptions

    log = Logger()
    sopts = getSweeperOptions(log, sys.argv)
    if not sopts.test(SweeperOptions.ALGO):
        print('ERROR: No algo id provided, python analysestatistics ' \
                '-h for help')
        sys.exit(1)
    if not sopts.test(SweeperOptions.LEAGUE):
        print('ERROR: No league provided, python analysestatistics -h for help')
        sys.exit(2)

    lbnd = sopts.lowerBound if sopts.test(SweeperOptions.LOWER_BOUND) else None
    ubnd = sopts.upperBound if sopts.test(SweeperOptions.UPPER_BOUND) else None
    analyseStatistics(log, sopts.algoId, sopts.leagueMnemonic, lbnd, ubnd)
