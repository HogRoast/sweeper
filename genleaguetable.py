import sys
from datetime import datetime
from shimbase.database import Database, AdhocKeys
from shimbase.sqlite3impl import SQLite3Impl
from operator import attrgetter, itemgetter

from sweeper.logging import Logger
from sweeper.utils import getSweeperConfig
from sweeper.dbos.league import League
from sweeper.dbos.match import Match
from sweeper.dbos.season import Season

def genLeagueTable(log:Logger, league:str, season:str, date:str=None):
    '''
    Generate a league table for the subject league and season

    :param log: a logging object
    :param league: the subject league
    :param season: the subject season
    :param date: the date string up to which to generate the league YYYY-MM-DD
    '''
    log.info('Generating league table for ' \
            'league <{}> and season <{}>'.format(league, season))

    config = getSweeperConfig()
    dbName = config['dbName']
    log.debug('Opening database: {}'.format(dbName))

    with Database(dbName, SQLite3Impl()) as db, db.transaction() as t:     
        try:
            league = db.select(League(league))[0]
        except:
            log.critical('No league matching the provided mnemonic exists')
            sys.exit(3)
        try:
            season = db.select(Season(season))[0]
        except:
            log.critical('No season matching the provided string exists')
            sys.exit(4)

        ubnd =  date if date is not None else season.getU_Bnd_Date()
        keys = {'league' : league.getMnemonic(), '!result' : '', '>date' : \
                season.getL_Bnd_Date(), '<date' : ubnd} 
        matches = [m for m in db.select(Match.createAdhoc(keys))]
        log.info('{} {} matches found'.format(len(matches), \
                league.getMnemonic()))

        teams = set([m.getHome_Team() for m in matches] + \
                [m.getAway_Team() for m in matches])

        class Data:
            played = 0
            won = 0
            drawn = 0
            lost = 0
            glfor = 0
            glagn = 0
            gldif = 0
            points = 0
            
            def __repr__(self):
                return 'played {:>2}, won {:>2}, drawn {:>2}, lost {:>2}, ' \
                        'for {:>3}, against {:>3}, diff {:>4}, points {:>3}' \
                        .format(self.played, self.won, self.drawn, self.lost, \
                       self.glfor, self.glagn, self.gldif, self.points)
            
        table = {} 
        for m in matches:
            table[m.getHome_Team()] = h = table.get(m.getHome_Team(), Data())
            table[m.getAway_Team()] = a = table.get(m.getAway_Team(), Data())
            h.played += 1
            a.played += 1
            h.glfor += m.getHome_Goals()
            h.glagn += m.getAway_Goals()
            h.gldif = h.glfor - h.glagn
            a.glfor += m.getAway_Goals()
            a.glagn += m.getHome_Goals()
            a.gldif = a.glfor - a.glagn
            if m.getResult() == 'H':
                h.won += 1
                h.points += 3
            elif m.getResult() == 'D':
                h.drawn += 1
                h.points += 1
                h.drawn += 1
                a.points += 1
            elif m.getResult() == 'A':
                a.won += 1
                a.points += 3
            else:
                raise Exception("Empty result, wasn't expecting that")

        [log.info('{:<16} {}'.format(row[0], row[1])) for row in \
                sorted(sorted(table.items(), key=itemgetter(0)), \
                key=lambda x : (x[1].points, x[1].gldif, x[1].glfor), \
                reverse=True)]

if __name__ == '__main__':
    from sweeper.utils import getSweeperOptions, SweeperOptions

    log = Logger()
    sopts = getSweeperOptions(log, sys.argv)
    if not sopts.test(SweeperOptions.LEAGUE):
        print('ERROR: No league provided, python genleaguetable -h for help')
        sys.exit(1)
    if not sopts.test(SweeperOptions.SEASON):
        print('ERROR: No season provided, python genleaguetable -h for help')
        sys.exit(2)

    date = sopts.date if sopts.test(SweeperOptions.DATE) else None
    genLeagueTable(log, sopts.leagueMnemonic, sopts.season, date)
