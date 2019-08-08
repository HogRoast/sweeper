import itertools
import sys
import io
import smtplib

from datetime import datetime, timedelta
from shimbase.database import Database, AdhocKeys
from shimbase.sqlite3impl import SQLite3Impl

from runsweeper import runSweeper
from sweeper.logging import Logger
from sweeper.table import Table
from sweeper.utils import getSweeperConfig
from sweeper.dbos.subscriber import Subscriber

#log = logging.getLogger(__name__)

class Mail():
    '''
    Send emails!
    '''
    def __init__(self, log:Logger, subject:str=None, content:list=None):
        '''
        Initialise the Mail class with content; all parameters are optional
        and can be added instead via the Mail interface.

        :param log: a logging object
        :param subject: the subject line of the email
        :param content: a list of strs, files or Tables containing content
        '''
        self._container = 'MIME-Version: 1.0\nContent-type: text/html\n' \
                'Subject:{subject}\n\n{body}</body>'
        self._firstTable = True
        self._subject = ''
        self._body = ''
        self._stdRecipients = True

        self.addSubject(subject)
        self.addContent(content)

        config = getSweeperConfig()
        log.debug('Opening database: {}'.format(config['dbName']))
        with Database(config['dbName'], SQLite3Impl()) as db:
            subs = db.select(Subscriber.createAdhoc({'include' : 1}))

        mailCfg = getSweeperConfig('mail.cfg')
        self._sender = mailCfg['fromAddr']
        self._recipients = [s.getEmail() for s in subs]
        self._server = smtplib.SMTP(mailCfg['svr'], int(mailCfg['port']))
        self._server.ehlo()
        self._server.starttls()
        self._server.ehlo()
        self._server.login(self._sender, mailCfg['pwd'])
        
    def addSubject(self, subject:str):
        if isinstance(subject, str):
            self._subject = subject

    def addContent(self, content):
        if content:
            if isinstance(content, str):
                self._addTextContent(content)
            elif isinstance(content, io.TextIOBase):
                self._addFileContent(content)
            elif isinstance(content, Table):
                self._addTableContent(content)

    def addRecipients(self, recipients:list):
        for r in recipients:
            self.addRecipient(r)

    def addRecipient(self, recipient):
        if self._stdRecipients:
            self._stdRecipients = False
            self._recipients = []

        if all([x in recipient for x in ('@', '.')]):
            self._recipients.append(recipient)

    def _addTextContent(self, content):
        self._body += '{}<br/><br/>'.format(content) 

    def _addFileContent(self, content):
        self._addTextContent(content.read())

    def _addTableContent(self, content):
        if self._firstTable:
            self._addTextContent(content.asHTML().replace('</body>', ''))
            self._firstTable = False
        else:
            self._addTextContent(content.asHTML(fullyFormed=False))

    def send(self):
       self._server.sendmail(*self._repr()) 
       log.info('email sent to: {!s}'.format(self._recipients))
 
    def __str__(self):
        return self._container.format(subject=self._subject, body=self._body)

    def __repr__(self):
        return str(self._repr())
    
    def _repr(self):
        return (self._sender, self._recipients, str(self))

if __name__ == '__main__':
    log = Logger()
    mail = Mail(log)
    mail.addSubject('Sweeper 18/19 summary and 19/20 kick off')
    #mail.addContent('This a test email to see if the new class works')

    #t = Table(headers=['1st', '2nd', '3rd'], schema=['{:>4}', '{:>5.3f}', '{:>3}'], title='Test')
    #t.append([[1, 2.454, 3], [4, 5, 6]])
    #t.append([[7, 8, 'dfd']])
    #t.setHighlights([[1]])
    #t.setHighlights([[2, 'dfd', True, False, Table.Palette.GREEN]])
    #t.append([[75,3, 3]])
    #t.addHighlight('3rd', 3, False, False, Table.Palette.RED)

    #mail.addContent(t)
    #mail.addContent('Just some more text to see what it looks like!')
    #mail.addContent(t)

    #log.info(repr(mail))
    f = open('mailtext/1819wrapup.txt', 'r')
    mail.addContent(f)
    f.close()
    mail.addContent(runSweeper(\
            log=log, algoId=1, league='E0', season='1819', backtest=True))
    mail.addContent(runSweeper(\
            log=log, algoId=1, league='D1', season='1819', backtest=True))
    mail.send()
