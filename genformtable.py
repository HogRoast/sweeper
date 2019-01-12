import sys
from datetime import datetime
from shimbase.database import Database, AdhocKeys
from shimbase.sqlite3impl import SQLite3Impl
from operator import attrgetter, itemgetter

from genleaguetable import genLeagueTable
from genform import genForm
from sweeper.form import Form
from sweeper.logging import Logger
from sweeper.table import Table
from sweeper.utils import getSweeperConfig
from sweeper.dbos.league import League
from sweeper.dbos.match import Match
from sweeper.dbos.season import Season
from sweeper.dbos.team import Team

def genFormTable(log:Logger, league:str, season:str, date:str=None, \
        show:bool=False):
    '''
    Generate a form table for the subject league and season

    :param log: a logging object
    :param league: the subject league
    :param season: the subject season
    :param date: the date string up to which to generate the league YYYY-MM-DD
    :param show: displays any tables as HTML when True

    :returns: the league and form tables
    '''
    log.info('Generating form table for ' \
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
            sys.exit(5)

        headers = ['Team', 'P', 'W', 'D', 'L', 'F', 'A', 'GD', 'PTS']
        schema = ['{:<20}', '{:>3}', '{:>3}', '{:>3}', '{:>3}', '{:>3}', \
                '{:>3}', '{:>4}', '{:>4}']
        formTable = Table(headers=headers, schema=schema, \
                title='{} Form Table'.format(league.getDesc()))
        leagueTable = genLeagueTable(log, league.getMnemonic(), \
                season.getName(), date, show)
        for team in leagueTable.getColumns()[0]:
            form, results = genForm(log, team, date)
            formTable.append(form.getRows())
        formTable.setRows([row for row in  \
                sorted(sorted(formTable.getRows(), key=itemgetter(0)), \
                key=lambda x : (x[8], x[7], x[5]), reverse=True)])
        log.info(formTable)

        if show: formTable.asHTML(show)

        return leagueTable, formTable 

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
    genFormTable(log, sopts.leagueMnemonic, sopts.season, date, \
            sopts.test(SweeperOptions.SHOW))
