import itertools
import sys
import smtplib
from datetime import datetime, timedelta
from shimbase.database import Database, AdhocKeys
from shimbase.sqlite3impl import SQLite3Impl

from genformtable import genFormTable
from sweeper.logging import Logger
from sweeper.table import Table
from sweeper.utils import getSweeperConfig
from sweeper.dbos.algo_config import Algo_Config
from sweeper.dbos.league import League
from sweeper.dbos.match import Match
from sweeper.dbos.rating import Rating
from sweeper.dbos.season import Season
from sweeper.dbos.statistics import Statistics
from sweeper.dbos.subscriber import Subscriber

def presentFixtures(log:Logger, algoId:int, date:str, league:str=None, \
        show:bool=False, mail:bool=False):
    '''
    Present the latest set of fixtures with all the appropriate ratings.

    :param log: a logging object
    :param date: include all fixtures from this date and onward
    :param league: the subject league, None signifies all available leagues 
    :param show: displays any tables as HTML when True
    :param mail: send as email
    '''
    log.info('Presenting fixtures for algo <{}>, date <{}> and league <{}>\
            '.format(algoId, date, league if league else 'ALL'))

    config = getSweeperConfig()
    dbName = config['dbName']
    log.debug('Opening database: {}'.format(dbName))

    with Database(dbName, SQLite3Impl()) as db, db.transaction() as t:     
        dt = datetime.strptime(date, '%Y-%m-%d') - timedelta(days=1)
        try:
            keys = {'>date' : dt.strftime('%Y-%m-%d'), 'result' : ''}
            if league: keys.update({'league' : league})
            order = ['<league', '<date']
            fixtures = db.select(Match.createAdhoc(keys, order))
            if not fixtures: raise Exception('No fixtures')
        except Exception as e:
            log.critical("Couldn't find fixtures for league and date " \
                    "provided, run sourcedata?")
            log.critical('Because...{}'.format(e))
            sys.exit(2)

        try:
            del keys['result']
            del keys['>date']
            dt = datetime.strptime(fixtures[0].getDate(), '%Y-%m-%d') \
                    - timedelta(days=1)
            keys.update({'>match_date' : dt.strftime('%Y-%m-%d')})
            keys.update({'algo_id' : algoId})
            order = ['<league', '<match_date']
            ratings = db.select(Rating.createAdhoc(keys, order))
            log.debug('Num fixtures {}, ratings {}'.format(len(fixtures), \
                    len(ratings)))
            if len(fixtures) != len(ratings): 
                raise Exception('Mismatched ratings')
        except Exception as e:
            log.critical("Couldn't find algo ratings for all fixtures, " \
                    "run analysematches?")
            log.critical('Because...{}'.format(e))
            sys.exit(3)

        try:
            keys.update({'>generation_date' : keys.pop('>match_date')})
            order = ['>generation_date']
            stats = db.select(Statistics.createAdhoc(keys, order))
            if not stats: raise Exception('No statistics')
            lastGenDate = stats[0].getGeneration_Date()
            stats = [s for s in stats if s.getGeneration_Date() == lastGenDate]
        except Exception as e:
            log.critical("Couldn't find algo statistics for league and date, " \
                    "run genstats?")
            log.critical('Because...{}'.format(e))
            sys.exit(4)

        def statsSummary(s:Statistics):
            markF = s.getMark_Freq()
            homeF = s.getHome_Freq()
            homeP = (homeF / markF) * 100.0 if markF else 0.0
            homeO = 100.0 / homeP if homeP else 99.99 
            drawF = s.getDraw_Freq()
            drawP = (drawF / markF) * 100.0 if markF else 0.0
            drawO = 100.0 / drawP if drawP else 99.99
            awayF = s.getAway_Freq()
            awayP = (awayF / markF) * 100.0 if markF else 0.0
            awayO = 100.0 / awayP if awayP else 99.99
            return markF, homeF, homeP, homeO, drawF, drawP, drawO, awayF, \
                    awayP, awayO

        for r in itertools.filterfalse(lambda r : r.getMark() in \
                [s.getMark() for s in stats], ratings):
            stats.append(Statistics(r.getMatch_Date(), r.getAlgo_Id(), \
                    r.getLeague(), r.getMark(), 0, 0, 0, 0))
        analytics = map(lambda r : [(r, statsSummary(s)) for s in stats \
                if r.getMark() == s.getMark() \
                and r.getLeague() == s.getLeague()], ratings)
        presentation = zip(fixtures, analytics)
 
        tables = {}
        mailText = ''
        for i, (league, group) in enumerate(itertools.groupby(presentation, \
                lambda x : x[0].getLeague())):
            try:
                leagueDesc = db.select(League(league))[0].getDesc()
            except Exception as e:
                log.critical("Couldn't find league")
                log.critical('Because..{}'.format(e))
                sys.exit(5)
            try:
                keys = {'league' : league}
                order = ['>config_date']
                algoCfg = db.select(Algo_Config.createAdhoc(keys, order))[0]
            except Exception as e:
                log.critical("Couldn't find algo config for league")
                log.critical('Because...{}'.format(e))
                sys.exit(6)

            presGrp = list(group)
            headers = ['Date', 'Match', 'Mark', 'M#', \
                    'H#', 'H%', 'HO', 'D#', 'D%', 'DO', 'A#', 'A%', 'AO']
            schema = ['{:<12}', '{:<40}', '{:>4}', '{:>4}', \
                    '{:>4}', '{:>5.2f}', '{:>5.2f}', '{:>4}', '{:>5.2f}', \
                    '{:>5.2f}', '{:>4}', '{:>5.2f}', '{:>5.2f}']
            t = Table(headers=headers, schema=schema, \
                    title='{} Fixtures'.format(leagueDesc))
            t.append([[f.getDate(), '{} (vs) {}'.format(f.getHome_Team(), \
                    f.getAway_Team()), r.getMark(), *a] \
                    for f, [(r, a)] in presGrp])
            t.setHighlights([[f.getHome_Team(), False] \
                    for f, [(r, a)] in presGrp \
                    if r.getMark() > algoCfg.getL_Bnd_Mark() \
                    and r.getMark() < algoCfg.getU_Bnd_Mark()])
            t.htmlReplacements([['(vs)', '<br/>']])

            try:
                keys = {'>u_bnd_date' : date, '<l_bnd_date' : date}
                season = db.select(Season.createAdhoc(keys))[0].getName()
            except Exception as e:
                log.critical("Couldn't find season for date")
                log.critical('Because...{}'.format(e))
                sys.exit(6)

            log.toggleMask(Logger.INFO)
            leagueTable, formTable = genFormTable(log, league, season, date)
            log.toggleMask(Logger.INFO)
            log.info(t)
            log.info(formTable)

            tables[leagueDesc] = (t, leagueTable, formTable)

            if show: 
                t.asHTML(show)
                formTable.asHTML(show)

            if mail: 
                if not i:
                    mailText += t.asHTML().replace('</body>', '') + '<br/>'
                else:
                    mailText += t.asHTML(fullyFormed=False) + '<br/>'
                mailText += formTable.asHTML(fullyFormed=False) + '<br/>'

        if mail:
            mailText = 'MIME-Version: 1.0\nContent-type: text/html\nSubject: Sweeper Football Predictions\n\n{}</body>'.format(mailText)
            mailCfg = getSweeperConfig('mail.cfg')
            fromAddr = mailCfg['fromAddr']
            subs = db.select(Subscriber.createAdhoc({'include' : 1}))
            toAddrs = [s.getEmail() for s in subs]
            server = smtplib.SMTP(mailCfg['svr'], int(mailCfg['port']))
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(fromAddr, mailCfg['pwd'])
            server.quit()
            log.info('email sent to: {!s}'.format(toAddrs))

        return tables

if __name__ == '__main__':
    from sweeper.utils import getSweeperOptions, SweeperOptions

    log = Logger()
    sopts = getSweeperOptions(log, sys.argv)
    if not sopts.test(SweeperOptions.ALGO):
        print('ERROR: No algo id provided, python presentfixtures -h for help')
        sys.exit(1)
    league = sopts.leagueMnemonic if sopts.test(SweeperOptions.LEAGUE) else None
    date = sopts.date if sopts.test(SweeperOptions.DATE) else \
            datetime.today().strftime('%Y-%m-%d')
    presentFixtures(log, sopts.algoId, date, league, \
            sopts.test(SweeperOptions.SHOW), sopts.test(SweeperOptions.MAIL))
