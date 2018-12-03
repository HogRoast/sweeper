import csv, urllib.request, sys
from sweeper.logging import Logger
from configparser import ConfigParser

class SweeperArgsError(Exception):
    def __init__(self, msg):
        self.msg = msg

class SweeperOptions:
    DEBUG_LOGGING       = 0b00000001
    CURRENT_SEASON_ONLY = 0b00000010
    ALGO                = 0b00000100
    LEAGUE              = 0b00001000
    SEASON              = 0b00010000

    validOpts = [
            DEBUG_LOGGING,
            CURRENT_SEASON_ONLY,
            ALGO,
            LEAGUE,
            SEASON
            ]

    def __init__(self):
        self._mask = 0b0000000
        self.algoId = None
        self.leagueMnemonic = None

    def _set(self, opt):
        '''
        Set the identified option but iff it is a valid one

        :param opt: a valid Sweeper option
        '''
        if opt in self.validOpts:
            self._mask |= opt

    def test(self, opt):
        '''
        Is the supplied opt set?

        :param opt: a Sweeper option
        :returns: True if set false otherwise
        '''
        return self._mask & opt

def getSweeperOptions(log, opts):
    ''' 
    Setup the provided logger according to the given options list 

    :param log: the logger to be configured
    :param opts: a list of options
    :returns: a SweeperOptions object with the appropriate opts set
    '''
    def showHelpAndExit():
        print(  'Sweeper help...\n' \
                '\n' \
                '   general\n' \
                '         -d : enable debug logging\n' \
                '         -h : display help\n' \
                '   sourcedata\n' \
                '         -c : apply to current season only\n' \
                '   analysematches\n' \
                '       * -a <id>        : algo to apply\n' \
                '       * -l <mnemonic>  : league to analyse\n' \
                '       * -s <season>    : season to analyse\n' \
                '   generatestats\n' \
                '       * -a <id>        : algo to apply\n' \
                '       * -l <mnemonic>  : league to analyse\n' \
                '\n' \
                '   * indicates mandatory param')
        sys.exit(0)

    sopts = SweeperOptions()
    if len(opts) > 1:
        # -h first as the application will exit on help
        if '-h' in opts:
            showHelpAndExit()
        if '-d' in opts: 
            log.toggleMask(Logger.DEBUG | Logger.TIME | Logger.TYPE)
            sopts._set(SweeperOptions.DEBUG_LOGGING)
        if '-c' in opts:
            sopts._set(SweeperOptions.CURRENT_SEASON_ONLY)
        try:
            if '-a' in opts:
                idx = opts.index('-a')
                algoId = int(opts[idx + 1])
                sopts._set(SweeperOptions.ALGO)
                sopts.algoId = algoId
            if '-l' in opts:
                idx = opts.index('-l')
                mnemonic = opts[idx + 1]
                sopts._set(SweeperOptions.LEAGUE)
                sopts.leagueMnemonic = mnemonic
            if '-s' in opts:
                idx = opts.index('-s')
                season = opts[idx + 1]
                sopts._set(SweeperOptions.SEASON)
                sopts.season = season
        except:
            showHelpAndExit()

    return sopts

def getSweeperConfig():
    '''
    Get the Sweeper application's base configuration from the sweeper.ini file

    :returns: A dictionary representing the base configuration
    '''
    config = ConfigParser()
    # maintain case of ini file keys
    config.optionxform = lambda option: option
    config.read('./config/sweeper.ini')

    baseCfg = dict(zip(config.options('base.cfg'), \
            [config.get('base.cfg', o) for o in config.options('base.cfg')]))
    return baseCfg

class FileManipulator:
    '''
    FileManipulator context manager class
    '''
    def __init__(self, fileHandle, manipulator):
        self._fileHandle = fileHandle
        self._manipulator = manipulator

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if '__exit__' in dir(self._fileHandle):
            return self._fileHandle.__exit__(exc_type, exc_val, exc_tb)
        else:
            return False

class FileReader(FileManipulator):
    '''
    FileReader manipulator class - a mechanism for folding the file handle and
    it's associated reader into a single context manager object
    '''
    def __init__(self, fileHandle, reader):
        super().__init__(fileHandle, reader)

    def __iter__(self):
        return self._manipulator.__iter__()

class FileWriter(FileManipulator):
    '''
    FileWriter manipulator class - a mechanism for folding the file handle and
    it's associated writer into a single context manager object
    '''
    def __init__(self, fileHandle, writer):
        super().__init__(fileHandle, writer)

    def writerow(self, r):
        self._manipulator.writerow(r)

def newCSVFile(fileName, fieldNames):
    '''
    Open specified CSV file for writing and initialise with supplied list
    of fieldNames, return an object that aggregates the filehandle,
    so that it can be used as contextmanager, and the writer for output

    :param fileName: the name of the CSV file to open for writing
    :param fieldNames: a list of the header fields to be written to the file
    :returns: the writer object
    '''
    _file = open(fileName, 'w', newline='')
    _writer = csv.writer(_file)
    _writer.writerow(fieldNames)

    writer = FileWriter(_file, _writer)
    return writer

def readCSVFileAsDict(filename):
    '''
    Open specified CSV file for reading in a dictionary form
    If the file begins http then this is a URL, so open appropriately

    :param fileName: the name of the CSV file to open for reading
    :returns: the reader object
    '''
    _file = None
    if filename[:4] == 'http':
        httpResp = urllib.request.urlopen(filename)
        results = str(httpResp.read())
        _file = results.split('\\r\\n')
    else:
        _file = open(filename, 'r', newline='')
    _reader = csv.DictReader(_file, delimiter=',')

    return FileReader(_file, _reader)

#class NumberFountains:
#    _numberFountains = {}
#    _datedFountains = {}
#
#    @classmethod
#    def next(cls, f:str):
#        '''
#        Get the next number from the appropriate fountain
#
#        :param f: a fountain name string
#        :returns: the next integer from the fountain
#        '''
#        try:
#            n = cls._numberFountains[f]
#        except KeyError:
#            n = 0
#        n += 1
#        cls._numberFountains[f]
#        return n
#
#    @classmethod
#    def nextByDate(cls, dt:datetime.date, f:str):
#        '''
#        Get the next number from the appropriate dated fountain
#
#        :param dt: a date
#        :param f: a fountain name string
#        :returns: the next integer from the fountain at the given date
#        '''
#        n = 0
#        if dt not in cls._datedFountains:
#            cls._datedFountains[dt] = {f : n}
#        elif f not in cls._datedFountains[dt]:
#            cls._datedFountains[dt][f] = n
#        else:
#            n = cls._datedFountains[dt][f]
#
#        n += 1
#        cls._datedFountains[dt][f] = n
#        return n
