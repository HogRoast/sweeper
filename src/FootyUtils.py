import csv
from Logging import Logger
from configparser import ConfigParser

class FootyArgsError(Exception):
    def __init__(self, msg):
        self.msg = msg

def getFootyOptions(log, opts):
    ''' Setup the provided logger according to the given options list
        and return values for indicated options '''
    sendMail = False
    rangeMap = None
    if len(opts) > 1:
        if '-d' in opts: log.toggleMask(Logger.DEBUG | Logger.TIME | Logger.TYPE)
        if '-s' in opts: sendMail = True
        if '-r' in opts:
            i = opts.index('-r')
            rmErr = True
            if i+1 < len(opts):
                try:
                    rangeMap = eval(opts[i+1])
                    log.debug(rangeMap)
                    if isinstance(rangeMap, dict):
                        rmErr = False
                except BaseException:
                    msg = 'Failed to evaluate rangeMap arg - ' + opts[i+1]
                    log.debug(msg)
                    raise FootyArgsError(msg)
            if rmErr:
                msg = '-r option must be followed by dictionary type representing a rangeMap'
                log.critical(msg)
                raise FootyArgsError(msg)

    return (sendMail, rangeMap)

def getFootyConfig():
    config = ConfigParser()
    config.read('../config/footy.ini')

    algoCfg = dict(zip(config.options('algo.cfg'), [config.get('algo.cfg', o) for o in config.options('algo.cfg')]))
    algoCfg['rangeMap'] = eval(config.get('algo.cfg', 'rangeMap'))
    algoCfg['seasons'] = eval(config.get('algo.cfg', 'seasons'))
    
    mailCfg = dict(zip(config.options('mail.cfg'), [config.get('mail.cfg', o) for o in config.options('mail.cfg')]))
    mailCfg['toAddrs'] = eval(config.get('mail.cfg', 'toAddrs'))
   
    return (algoCfg, mailCfg)

class FileManipulator:
    def __init__(self, fileHandle, manipulator):
        self._fileHandle = fileHandle
        self._manipulator = manipulator

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self._fileHandle.__exit__(exc_type, exc_val, exc_tb)

class FileReader(FileManipulator):
    def __init__(self, fileHandle, reader):
        super().__init__(fileHandle, reader)

    def __iter__(self):
        return self._manipulator.__iter__()

class FileWriter(FileManipulator):
    def __init__(self, fileHandle, writer):
        super().__init__(fileHandle, writer)

    def writerow(self, r):
        self._manipulator.writerow(r)

def newCSVFile(fileName, fieldNames):
    '''
    Open specified CSV file for writing and initialise with supplied list
    of fieldNames, return an object that aggregates the filehandle,
    so that it can be used as contextmanager, and the writer for output
    '''
    _file = open(fileName, 'w', newline='')
    _writer = csv.writer(_file)
    _writer.writerow(fieldNames)

    writer = FileWriter(_file, _writer)
    return writer

def readCSVFileAsDict(filename):
    '''
    Open specified CSV file for reading in a dictionary form
    '''
    _file = open(filename, 'r', newline='')
    _reader = csv.DictReader(_file, delimiter=',')
    
    reader = FileReader(_file, _reader)
    return reader


