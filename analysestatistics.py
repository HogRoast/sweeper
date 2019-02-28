import itertools
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
        log:Logger, algoId:int, league:str=None, lbnd:int=None, ubnd:int=None):
    '''
    Analyse statistics for the algo and league combination

    :param log: a logging object
    :param algoId: the algo subject
    :param league: the league subject, all if unset
    :param lbnd: include marks above this value
    :param ubnd: include marks below this value
    '''
    log.info('Analysing statistics for league <{}> with algo <{}>'\
            .format(league if league else 'ALL', algoId))

    config = getSweeperConfig()
    dbName = config['dbName']
    log.debug('Opening database: {}'.format(dbName))

    with Database(dbName, SQLite3Impl()) as db, db.transaction() as t:     
        try:
            keys = {'algo_id' : algoId}
            order = ['>generation_date']
            if league: 
                keys.update({'league' : league})
                order.append('>league')
            if lbnd and ubnd: keys.update({'>mark' : lbnd, '<mark' : ubnd})
            statistics = db.select(Statistics.createAdhoc(keys, order)) 
            if not statistics: raise Exception('No statistics')
            lastGenDate = statistics[0].getGeneration_Date()
            statistics = [s for s in statistics \
                    if s.getGeneration_Date() == lastGenDate]            
        except:
            log.critical('No statistics matching the provided algo and ' \
                    'league exists')
            sys.exit(2)

        for league, group in itertools.groupby(\
                statistics, lambda x : x.getLeague()):
            statsGrp = list(group)
            x = [s.getMark() for s in statsGrp if s.getMark_Freq() > 0]
            hY = [s.getHome_Freq() / s.getMark_Freq() * 100 \
                    for s in statsGrp if s.getMark_Freq() > 0]
            hF = [s.getHome_Freq() for s in statsGrp if s.getMark_Freq() > 0]
            dY = [s.getDraw_Freq() / s.getMark_Freq() * 100 \
                    for s in statsGrp if s.getMark_Freq() > 0]
            dF = [s.getDraw_Freq() for s in statsGrp if s.getMark_Freq() > 0]
            aY = [s.getAway_Freq() / s.getMark_Freq() * 100 \
                    for s in statsGrp if s.getMark_Freq() > 0]
            aF = [s.getAway_Freq() for s in statsGrp if s.getMark_Freq() > 0]
         
            slope, intercept, r, p, stderr = stats.linregress(x, hY)
            r2 = r**2
            log.info('{:>4} Home: {:>4.2f} {:>4.2f} {:>4.2} {:>4.2f} ' \
                    '{:>4.2f} {:>4.2}'.format(league, slope, intercept, p, \
                    r, r2, stderr))
            createPlot(x, hY, hF, intercept, slope, league + ' home')

            slope, intercept, r, p, stderr = stats.linregress(x, dY)
            r2 = r**2
            log.info('{:>4} Draw: {:>4.2f} {:>4.2f} {:>4.2} {:>4.2f} ' \
                    '{:>4.2f} {:>4.2}'.format(league, slope, intercept, p, \
                    r, r2, stderr))
            createPlot(x, dY, dF, intercept, slope, league + ' draw')
            
            slope, intercept, r, p, stderr = stats.linregress(x, aY)
            r2 = r**2
            log.info('{:>4} Away: {:>4.2f} {:>4.2f} {:>4.2} {:>4.2f} ' \
                    '{:>4.2f} {:>4.2}'.format(league, slope, intercept, p, \
                    r, r2, stderr))
            createPlot(x, aY, aF, intercept, slope, league + ' away')

if __name__ == '__main__':
    from sweeper.utils import getSweeperOptions, SweeperOptions

    log = Logger()
    sopts = getSweeperOptions(log, sys.argv)
    if not sopts.test(SweeperOptions.ALGO):
        print('ERROR: No algo id provided, python analysestatistics ' \
                '-h for help')
        sys.exit(1)
    league = sopts.leagueMnemonic if sopts.test(SweeperOptions.LEAGUE) else None
    lbnd = sopts.lowerBound if sopts.test(SweeperOptions.LOWER_BOUND) else None
    ubnd = sopts.upperBound if sopts.test(SweeperOptions.UPPER_BOUND) else None

    analyseStatistics(log, sopts.algoId, league, lbnd, ubnd)
