from datetime import datetime, timedelta
import os
import sys
import tempfile
import webbrowser

from presentfixtures import presentFixtures
from sweeper.logging import Logger
from sweeper.table import Table
from sweeper.website import HTML_HEAD, HTML_BODY, COLLAPSIBLE_GROUP

def modTable(html):
    return html.replace('<table>', '').replace('</table>', '').replace('<td ', '<td class="m"')

def addPriorities(html):
    thead = html.split('thead')
    hdrs = thead[1].split('<th>')
    for i, h in enumerate(hdrs):
        if 'Date' in h:
            hdrs[i] = '<th data-priority="2">' + h
        elif 'Match' in h:
            hdrs[i] = '<th>' + h
        elif 'Mark' in h:
            hdrs[i] = '<th>' + h
        elif 'M#' in h:
            hdrs[i] = '<th data-priority="3">' + h
        elif 'H#' in h:
            hdrs[i] = '<th data-priority="1">' + h
        elif 'H%' in h:
            hdrs[i] = '<th data-priority="1">' + h
        elif 'HO' in h:
            hdrs[i] = '<th>' + h
        elif 'D#' in h:
            hdrs[i] = '<th data-priority="1">' + h
        elif 'D%' in h:
            hdrs[i] = '<th data-priority="1">' + h
        elif 'DO' in h:
            hdrs[i] = '<th>' + h
        elif 'A#' in h:
            hdrs[i] = '<th data-priority="1">' + h
        elif 'A%' in h:
            hdrs[i] = '<th data-priority="1">' + h
        elif 'AO' in h:
            hdrs[i] = '<th>' + h
    thead[1] = ''.join(hdrs)
    html = 'thead'.join(thead)
    return html

def createWebPage(log:Logger, algoId:int, date:str, league:str=None, \
        show:bool=False):
    '''
    Create a web page for the algo, league and date provided

    :param log: a logging object
    :param date: include all fixtures from this date and onward
    :param league: the subject league, None signifies all available leagues 
    :param show: displays any tables as HTML when True
    '''
    log.info('Creating web page for algo <{}>, date <{}> and league <{}>\
            '.format(algoId, date, league if league else 'ALL'))

    tables = presentFixtures(log, algoId, date, league)
    groups = ''
    for groupId, (name, (fixturesTable, leagueTable, formTable)) \
            in enumerate(sorted(tables.items(), key=lambda x : x[0])):
        collapsibleTheme = 'c' if fixturesTable.getHighlights() else 'b'
        groups += COLLAPSIBLE_GROUP.format(groupName=name, fixturesTable= \
                addPriorities(modTable(fixturesTable.asHTML(fullyFormed=False))), \
                formTable=modTable(formTable.asHTML(fullyFormed=False)), \
                leagueTable=modTable(leagueTable.asHTML(fullyFormed=False)),
                groupId=groupId, collapsibleTheme=collapsibleTheme)
    html = HTML_HEAD + HTML_BODY.format(groups=groups)

    log.info(html)
    with open('web/index.html', 'w') as f:
        f.write(html)
    if show:
        webbrowser.open(os.getcwd() + '/web/index.html')


if __name__ == '__main__':
    from sweeper.utils import getSweeperOptions, SweeperOptions

    log = Logger()
    sopts = getSweeperOptions(log, sys.argv)
    if not sopts.test(SweeperOptions.ALGO):
        print('ERROR: No algo id provided, python createwebpage -h for help')
        sys.exit(1)
    league = sopts.leagueMnemonic if sopts.test(SweeperOptions.LEAGUE) else None
    date = sopts.date if sopts.test(SweeperOptions.DATE) else \
            datetime.today().strftime('%Y-%m-%d')
    createWebPage(log, sopts.algoId, date, league, \
            sopts.test(SweeperOptions.SHOW))

