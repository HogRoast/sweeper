import sys
from datetime import datetime
from shimbase.database import Database, AdhocKeys
from shimbase.sqlite3impl import SQLite3Impl

from sweeper.logging import Logger
from sweeper.utils import getSweeperConfig, readCSVFileAsDict
from sweeper.dbos.source import Source
from sweeper.dbos.source_season_map import Source_Season_Map
from sweeper.dbos.source_league_map import Source_League_Map
from sweeper.dbos.source_team_map import Source_Team_Map
from sweeper.dbos.match import Match
from sweeper.dbos.team import Team

def getBestOdds(log, row):
    '''
    From the row provided get the best home, draw and away odds

    :param log: a logging object
    :param row: a row from a Football-Data historical match csv file in 
                the form of a dictionary
    :returns: a tuple of best home, draw and away odds
    '''
    date = row['Date']
    ht = row['HomeTeam']
    at = row['AwayTeam']

    bestH = 0
    bestD = 0
    bestA = 0
    try:
        b365H = float(row['B365H'])
        b365D = float(row['B365D'])
        b365A = float(row['B365A'])
        if b365H > bestH: 
            bestH = b365H
        if b365D > bestD: 
            bestD = b365D
        if b365A > bestA: 
            bestA = b365A
    except BaseException:
        log.debug('No B365 data - skipping : {} {} {}'.format(date, ht, at))
    try:
        bwH = float(row['BWH'])
        bwD = float(row['BWD'])
        bwA = float(row['BWA'])
        if bwH > bestH: 
            bestH = bwH
        if bwD > bestD: 
            bestD = bwD
        if bwA > bestA: 
            bestA = bwA
    except BaseException:
        log.debug('No BW data - skipping : {} {} {}'.format(date, ht, at))
    try:
        iwH = float(row['IWH'])
        iwD = float(row['IWD'])
        iwA = float(row['IWA'])
        if iwH > bestH : 
            bestH = iwH
        if iwD > bestD: 
            bestD = iwD
        if iwA > bestA: 
            bestA = iwA
    except BaseException:
        log.debug('No IW data - skipping : {} {} {}'.format(date, ht, at))
    '''
    try:
        lbH = float(row['LBH'])
        lbD = float(row['LBD'])
        lbA = float(row['LBA'])
        if lbH > bestH : 
            bestH = lbH
        if lbD > bestD: 
            bestD = lbD
        if lbA > bestA: 
            bestA = lbA
    except BaseException:
        log.debug('No LB data - skipping : {} {} {}'.format(date, ht, at))
    '''
    try:
        whH = float(row['WHH'])
        whD = float(row['WHD'])
        whA = float(row['WHA'])
        if whH > bestH : 
            bestH = whH
        if whD > bestD: 
            bestD = whD
        if whA > bestA: 
            bestA = whA
    except BaseException:
        log.debug('No WH data - skipping : {} {} {}'.format(date, ht, at))
    try:
        vcH = float(row['VCH'])
        vcD = float(row['VCD'])
        vcA = float(row['VCA'])
        if vcH > bestH : 
            bestH = vcH
        if vcD > bestD: 
            bestD = vcD
        if vcA > bestA: 
            bestA = vcA
    except BaseException:
        log.debug('No VC data - skipping : {} {} {}'.format(date, ht, at))

    return (bestH, bestD, bestA)

def sourceData(log:Logger, target:str, currentSeason:bool):
    '''
    Obtain historical match data

    :param log: a logging object
    :param target: the name of match data source
    :param currentSeason: True if only interested in the current season's data
    '''
    log.info('Downloading data from source: {}'.format(target))

    config = getSweeperConfig()
    dbName = config['dbName']
    log.debug('Opening database: {}'.format(dbName))

    with Database(dbName, SQLite3Impl()) as db, db.transaction() as t:     
        keys = {'name' : target}
        source = db.select(Source.createAdhoc(keys))
        if source:
            source = source[0]
        else:
            sys.exit('{} source not in database'.format(target))
        log.debug('{}'.format(source))

        keys = {'source_id': source.getId(), 'active' : 1}
        if currentSeason:
            seasonMap = db.select(
                    Source_Season_Map.createAdhoc(keys, ('>season',)))[0:1]
        else:
            seasonMap = db.select(Source_Season_Map.createAdhoc(keys))
        log.debug('{}'.format(seasonMap))

        keys = {'source_id': source.getId()}
        leagueMap = db.select(Source_League_Map.createAdhoc(keys))
        log.debug('{}'.format(leagueMap))
        
        teams = db.select(Team())
        log.debug('{}'.format(teams))

        for l in leagueMap:
            for s in seasonMap:
                resultsURL = s.getData_Url().format(l.getLeague())
                log.info('Downloading...' + resultsURL)
    
                with readCSVFileAsDict(resultsURL) as resultsReader:
                    for row in resultsReader:
                        try:
                            dt = datetime.strptime(row['Date'], '%d/%m/%y')
                        except Exception:
                            continue

                        ht = row['HomeTeam']
                        keys = {'source_id' : source.getId(), 'moniker' : ht}
                        teamMap = db.select(Source_Team_Map.createAdhoc(keys))
                        if teamMap: ht = teamMap[0].getTeam()
                        db.upsert(Team(ht, l.getLeague()))

                        at = row['AwayTeam']
                        keys = {'source_id' : source.getId(), 'moniker' : at}
                        teamMap = db.select(Source_Team_Map.createAdhoc(keys))
                        if teamMap: at = teamMap[0].getTeam()
                        db.upsert(Team(at, l.getLeague()))
                    
                        bestH, bestD, bestA = getBestOdds(log, row)
                        match = Match(str(dt.date()), l.getLeague(), ht, at, \
                                row['FTR'], bestH, bestD, bestA, \
                                row['FTHG'], row['FTAG'])
                        log.debug(match)
                        db.upsert(match)
        
if __name__ == '__main__':
    from sweeper.utils import getSweeperOptions, SweeperOptions

    log = Logger()
    sopts = getSweeperOptions(log, sys.argv)
    target = 'Football-Data'
    sourceData(log, target, sopts.test(SweeperOptions.CURRENT_SEASON_ONLY))
