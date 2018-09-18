from datetime import datetime

class Logger:
    TYPE     = 0x0000001
    TIME     = 0x0000010
    INFO     = 0x0000100
    DEBUG    = 0x0001000
    WARNING  = 0x0010000 
    ERROR    = 0x0100000 
    CRITICAL = 0x1000000

    def __init__(self):
        self.mask = self.INFO | self.WARNING | self.ERROR | self.CRITICAL
        self.log = print

    def setLogger(self, l):
        self.log = l

    def getLogger(self):
        return self.log

    def setMask(self, m):
        self.mask = m

    def toggleMask(self, m):
        self.mask ^= m

    def getMask(self):
        return self.mask
    
    def _baselog(self, s):
        ll = ''
        if self.mask & self.TIME: ll += '{!s} : '.format(datetime.now())
        if self.mask & self.TYPE: ll += '{:<8s} : '.format(s)
        return ll
        
    def info(self, s):
        if self.mask & self.INFO: self.log('{}{}'.format(self._baselog('INFO'), s))
        
    def debug(self, s):
        if self.mask & self.DEBUG: self.log('{}{}'.format(self._baselog('DEBUG'), s))

    def warning(self, s):
        if self.mask & self.WARNING: self.log('{}{}'.format(self._baselog('WARNING'), s))

    def error(self, s):
        if self.mask & self.ERROR: self.log('{}{}'.format(self._baselog('ERROR'), s))

    def critical(self, s):
        if self.mask & self.CRITICAL: self.log('{}{}'.format(self._baselog('CRITICAL'), s))
