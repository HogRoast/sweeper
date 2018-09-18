# coding: utf-8

from datetime import datetime
from unittest import TestCase
from src.Logging import Logger

class TestLogging(TestCase):
    """Logging test stubs"""
    def setUp(self):
        self.mockLog = []

    def log(self, s):
        self.mockLog.append(s)

    def test_init(self):
        """Test case for initialisation
        
        """
        l = Logger()
        self.assertIs(l.log, print)
        self.assertEqual(l.mask, 0x1110100)

    def test_setGetLogger(self):
        """Test case for setting/getting a logging object
        
        """
        l = Logger()
        # Yes this is nasty in real life, but it proves the point
        l.setLogger(l)
        self.assertIs(l.getLogger(), l)

    def test_setGetMask(self):
        """Test case for setting/getting a mask
        
        """
        l = Logger()
        l.setMask(Logger.DEBUG)
        self.assertEqual(l.getMask(), 0x0001000)

    def test_toggleMask(self):
        """Test case for toggling a mask
        
        """
        l = Logger()
        l.setMask(Logger.DEBUG)
        l.toggleMask(Logger.DEBUG)
        self.assertEqual(l.getMask(), 0x0000000)
        l.toggleMask(Logger.INFO)
        self.assertEqual(l.getMask(), 0x0000100)

    def test_info(self):
        """Test cases for info logging
        
        """
        l = Logger()
        l.setLogger(self.log)
        l.info('test_info_0')

        l.toggleMask(Logger.TYPE)
        l.info('test_info_1')

        l.toggleMask(Logger.TYPE | Logger.TIME)
        dt = datetime.now()
        l.info('test_info_2')

        l.toggleMask(Logger.TYPE)
        dt = datetime.now()
        l.info('test_info_3')

        l.toggleMask(Logger.INFO)
        dt = datetime.now()
        # this won't get logged
        l.info('test_info_4')

        self.assertEqual(self.mockLog[0], 'test_info_0')
        self.assertEqual(self.mockLog[1], 'INFO     : test_info_1')
        self.assertEqual(self.mockLog[2], '{!s} : test_info_2'.format(dt))
        self.assertEqual(self.mockLog[3], '{!s} : INFO     : test_info_3'.format(dt))
        # length 4 only as last not logged
        self.assertEqual(len(self.mockLog), 4) 

    def test_debug(self):
        """Test cases for debug logging
        
        """
        l = Logger()
        l.setLogger(self.log)
        l.toggleMask(Logger.DEBUG)
        l.debug('test_debug_0')

        l.toggleMask(Logger.TYPE)
        l.debug('test_debug_1')

        l.toggleMask(Logger.TYPE | Logger.TIME)
        dt = datetime.now()
        l.debug('test_debug_2')

        l.toggleMask(Logger.TYPE)
        dt = datetime.now()
        l.debug('test_debug_3')

        l.toggleMask(Logger.DEBUG)
        dt = datetime.now()
        # this won't get logged
        l.debug('test_debug_4')

        self.assertEqual(self.mockLog[0], 'test_debug_0')
        self.assertEqual(self.mockLog[1], 'DEBUG    : test_debug_1')
        self.assertEqual(self.mockLog[2], '{!s} : test_debug_2'.format(dt))
        self.assertEqual(self.mockLog[3], '{!s} : DEBUG    : test_debug_3'.format(dt))
        # length 4 only as last not logged
        self.assertEqual(len(self.mockLog), 4) 

    def test_warning(self):
        """Test cases for warning logging
        
        """
        l = Logger()
        l.setLogger(self.log)
        l.warning('test_warn_0')

        l.toggleMask(Logger.TYPE)
        l.warning('test_warn_1')

        l.toggleMask(Logger.TYPE | Logger.TIME)
        dt = datetime.now()
        l.warning('test_warn_2')

        l.toggleMask(Logger.TYPE)
        dt = datetime.now()
        l.warning('test_warn_3')

        l.toggleMask(Logger.WARNING)
        dt = datetime.now()
        # this won't get logged
        l.warning('test_warn_4')

        self.assertEqual(self.mockLog[0], 'test_warn_0')
        self.assertEqual(self.mockLog[1], 'WARNING  : test_warn_1')
        self.assertEqual(self.mockLog[2], '{!s} : test_warn_2'.format(dt))
        self.assertEqual(self.mockLog[3], '{!s} : WARNING  : test_warn_3'.format(dt))
        # length 4 only as last not logged
        self.assertEqual(len(self.mockLog), 4) 

    def test_error(self):
        """Test cases for error logging
        
        """
        l = Logger()
        l.setLogger(self.log)
        l.error('test_error_0')

        l.toggleMask(Logger.TYPE)
        l.error('test_error_1')

        l.toggleMask(Logger.TYPE | Logger.TIME)
        dt = datetime.now()
        l.error('test_error_2')

        l.toggleMask(Logger.TYPE)
        dt = datetime.now()
        l.error('test_error_3')

        l.toggleMask(Logger.ERROR)
        dt = datetime.now()
        # this won't get logged
        l.error('test_error_4')

        self.assertEqual(self.mockLog[0], 'test_error_0')
        self.assertEqual(self.mockLog[1], 'ERROR    : test_error_1')
        self.assertEqual(self.mockLog[2], '{!s} : test_error_2'.format(dt))
        self.assertEqual(self.mockLog[3], '{!s} : ERROR    : test_error_3'.format(dt))
        # length 4 only as last not logged
        self.assertEqual(len(self.mockLog), 4) 

    def test_critical(self):
        """Test cases for critical logging
        
        """
        l = Logger()
        l.setLogger(self.log)
        l.critical('test_crit_0')

        l.toggleMask(Logger.TYPE)
        l.critical('test_crit_1')

        l.toggleMask(Logger.TYPE | Logger.TIME)
        dt = datetime.now()
        l.critical('test_crit_2')

        l.toggleMask(Logger.TYPE)
        dt = datetime.now()
        l.critical('test_crit_3')

        l.toggleMask(Logger.CRITICAL)
        dt = datetime.now()
        # this won't get logged
        l.critical('test_crit_4')

        self.assertEqual(self.mockLog[0], 'test_crit_0')
        self.assertEqual(self.mockLog[1], 'CRITICAL : test_crit_1')
        self.assertEqual(self.mockLog[2], '{!s} : test_crit_2'.format(dt))
        self.assertEqual(self.mockLog[3], '{!s} : CRITICAL : test_crit_3'.format(dt))
        # length 4 only as last not logged
        self.assertEqual(len(self.mockLog), 4) 

if __name__ == '__main__':
    import unittest
    unittest.main()
