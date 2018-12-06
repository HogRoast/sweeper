import sys
from datetime import datetime, timedelta
from shimbase.database import Database, AdhocKeys
from shimbase.sqlite3impl import SQLite3Impl

from sweeper.logging import Logger
from sweeper.utils import getSweeperConfig
from sweeper.dbos.league import League
from sweeper.dbos.match import Match
from sweeper.dbos.season import Season

def genForm(log:Logger, date:str, team:str):
    '''
    Generate form over the previous 6 matches for the team provided

    :param log: a logging object
    :param date: search date
    :param team: the subject team
    '''
    log.info('Generating form for date <{}> and team <{}>'.format(date, team))

    config = getSweeperConfig()
    dbName = config['dbName']
    log.debug('Opening database: {}'.format(dbName))

    with Database(dbName, SQLite3Impl()) as db, db.transaction() as t:     
        dt = datetime.strptime(date, '%Y-%m-%d') + timedelta(days=1)
        try:
            keys = {'<date' : dt.strftime('%Y-%m-%d'), 'home_team' : team, \
                    '!result' : ''}
            order = {'>date'}
            matches1 = [m for m in db.select(Match.createAdhoc(keys, order))]
            del keys['home_team']
            keys['away_team'] = team
            matches2 = [m for m in db.select(Match.createAdhoc(keys, order))]
        except:
            log.critical("Couldn't find matches for team and date provided")
            sys.exit(3)

        matches = sorted(matches1 + matches2, key=lambda m : m.getDate(), reverse=True)[0:6]
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
               return 'played {}, won {}, drawn {}, lost {}, for {}, ' \
                       'against {}, diff {}, points {}'.format( \
                       self.played, self.won, self.drawn, self.lost, \
                       self.glfor, self.glagn, self.gldif, self.points)
        form = Data()
        for m in matches:
            form.played += 1
            if m.getHome_Team() == team:
                form.glfor += m.getHome_Goals()
                form.glagn += m.getAway_Goals()
            else:
                form.glfor += m.getAway_Goals()
                form.glagn += m.getHome_Goals()
            form.gldif = form.glfor - form.glagn
            if m.getResult() == 'H':
                if m.getHome_Team() == team:
                    form.won += 1
                    form.points += 3
                else:
                    form.lost += 1
            elif m.getResult() == 'D':
                form.drawn += 1
                form.points += 1
            elif m.getResult() == 'A':
                if m.getAway_Team() == team:
                    form.won += 1
                    form.points += 3
                else:
                    form.lost += 1
            else:
                raise Exception("Wasn't expecting that!")

        log.info('{} Form: {}'.format(team, form))
        [log.info('{:<12} {:<16} ({:>2}) vs ({:>2}) {:>16}'.format( \
                m.getDate(), m.getHome_Team(), m.getHome_Goals(), \
                m.getAway_Goals(), m.getAway_Team())) for m in matches]
    
if __name__ == '__main__':
    from sweeper.utils import getSweeperOptions, SweeperOptions

    log = Logger()
    sopts = getSweeperOptions(log, sys.argv)
    if not sopts.test(SweeperOptions.DATE):
        print('ERROR: No match date provided, python genform -h for help')
        sys.exit(1)
    if not sopts.test(SweeperOptions.TEAM):
        print('ERROR: No team provided, python genform -h for help')
        sys.exit(2)

    genForm(log, sopts.date, sopts.team)
