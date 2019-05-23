import itertools
import sys
import smtplib
from datetime import datetime, timedelta
from shimbase.database import Database, AdhocKeys
from shimbase.sqlite3impl import SQLite3Impl

from genformtable import genFormTable
from sweeper.algos import AlgoFactory
from sweeper.logging import Logger
from sweeper.table import Table
from sweeper.utils import getSweeperConfig
from sweeper.dbos.algo import Algo
from sweeper.dbos.algo_config import Algo_Config
from sweeper.dbos.league import League
from sweeper.dbos.match import Match
from sweeper.dbos.rating import Rating
from sweeper.dbos.season import Season
from sweeper.dbos.statistics import Statistics
from sweeper.dbos.subscriber import Subscriber

def presentFixtures(log:Logger, algoId:int, league:str=None, show:bool=False, \
        mail:bool=False, backtest:bool=False, season:str=None):
    '''
    Present the latest set of fixtures with all the appropriate ratings.

    :param log: a logging object
    :param league: the subject league, None signifies all available leagues 
    :param show: displays any tables as HTML when True
    :param mail: send as email
    :param backtest: run in backtest mode
    :param season: season to run backtest for
    '''
    log.info('Presenting fixtures for algo <{}>, league <{}> and backtest ' \
            '<{}> for season <{}>'.format(algoId, league if league else 'ALL', \
            backtest, season))

    config = getSweeperConfig()
    dbName = config['dbName']
    log.debug('Opening database: {}'.format(dbName))

    with Database(dbName, SQLite3Impl()) as db, db.transaction() as t:     
        date = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
        try:
            algo = db.select(Algo(algoId))[0]
            algo = AlgoFactory.create(algo.getName())
        except Exception as e:
            log.critical('No algo matching the provided id exists')
            log.critical('Because...%s' % e)
            sys.exit(2)

        if backtest:
            # In backtest mode use the inverse algoId to retrieve config,
            # ratings and stats and process all matches irrespective of
            # existing results
            algoId = -algoId
            if season:
                try:
                    season = db.select(Season(season))[0]
                except Exception as e:
                    log.critical( \
                            'No season matching the provided season exists')
                    sys.exit(3)
            else:
                log.critical('Must specify season with backtest')
                sys.exit(4)
            keys = {'>date' : season.getL_Bnd_Date(), \
                    '<date' : season.getU_Bnd_Date()}
        else:
            keys = {'>date' : date, 'result' : ''}

        try:
            if league: keys.update({'league' : league})
            order = ['<league', '<date']
            fixtures = db.select(Match.createAdhoc(keys, order))
            if not fixtures: raise Exception('No fixtures')
        except Exception as e:
            log.critical("Couldn't find fixtures for league and date " \
                    "provided, run sourcedata?")
            log.critical('Because...{}'.format(e))
            sys.exit(5)

        try:
            if 'result' in keys: del keys['result']
            if '<date' in keys: keys.update({'<match_date' : keys.pop('<date')})
            del keys['>date']
            dt = datetime.strptime(min(f.getDate() for f in fixtures), \
                    '%Y-%m-%d') - timedelta(days=1)
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
            sys.exit(6)

        try:
            del keys['>match_date']
            if '<match_date' in keys: del keys['<match_date']
            keys.update({'>generation_date' : date})
            order = ['>generation_date']
            stats = db.select(Statistics.createAdhoc(keys, order))
            if not stats: raise Exception('No statistics')
            lastGenDate = stats[0].getGeneration_Date()
            stats = [s for s in stats if s.getGeneration_Date() == lastGenDate]
        except Exception as e:
            log.critical("Couldn't find algo statistics for league and date, " \
                    "run genstats?")
            log.critical('Because...{}'.format(e))
            sys.exit(7)

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
                [s.getMark() for s in stats if r.getLeague() == s.getLeague()],\
                ratings):
            stats.append(Statistics(r.getMatch_Date(), r.getAlgo_Id(), \
                    r.getLeague(), r.getMark(), 0, 0, 0, 0))
        analytics = map(lambda r : [(r, statsSummary(s)) for s in stats \
                if r.getMark() == s.getMark() \
                and r.getLeague() == s.getLeague()], ratings)
        presentation = zip(fixtures, analytics)
 
        tables = {}
        mailText = 'Visit the website for more details - http://www.sweeperfootball.com<br/><br/>The website is up to date again after a few weeks hiatus.<br/><br/>CAVEAT! Last week of the premier league season! Can\'t stand behind any of the algo predictions this week, only two teams have anything left to play for in the premiership and even that looks a foregone conclusion. There are two weeks left in the Bundesliga however. Next season the algo will be smarter and take this into account.<br/><br/>In the coming weeks Sweeper will provide an end of season summary...<br/><br/>'
        for i, (league, group) in enumerate(itertools.groupby(presentation, \
                lambda x : x[0].getLeague())):
            try:
                leagueDesc = db.select(League(league))[0].getDesc()
            except Exception as e:
                log.critical("Couldn't find league")
                log.critical('Because..{}'.format(e))
                sys.exit(5)
            try:
                keys = {'league' : league, 'algo_id' : algoId}
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
            t.setHighlights([[1, False] for f, [(r, a)] in presGrp \
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

            mask = log.getMask()
            log.setMask(mask & ~Logger.INFO)
            leagueTable, formTable = genFormTable(log, league, season, date)
            log.setMask(mask)
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
            server.sendmail(fromAddr, toAddrs, mailText)
            server.quit()
            log.info('email sent to: {!s}'.format(toAddrs))

        return tables

if __name__ == '__main__':
    from sweeper.utils import getSweeperOptions, SweeperOptions

    log = Logger()
    sopts = getSweeperOptions(log, sys.argv)
    if not (sopts.test(SweeperOptions.ALGO) or sopts.algoId < 0):
        print('ERROR: null/negative algo id provided, python presentfixtures ' \
                '-h for help')
        sys.exit(1)
    league = sopts.leagueMnemonic if sopts.test(SweeperOptions.LEAGUE) else None
    season = sopts.season if sopts.test(SweeperOptions.SEASON) else None
    presentFixtures(log, sopts.algoId, league, \
            sopts.test(SweeperOptions.SHOW), sopts.test(SweeperOptions.MAIL), \
            sopts.test(SweeperOptions.BACKTEST), season)
