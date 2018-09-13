# -*- coding: utf-8 -*-
import json
import logging
from collections import OrderedDict

from .context import OrderedDictFormatter, JSONFormatter

import unittest

try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO


log_buffer = StringIO()
stringio_handler = logging.StreamHandler(log_buffer)

logger = logging.getLogger('test')
logger.addHandler(stringio_handler)
logger.setLevel(logging.DEBUG)
logging.propagate = False


class LoggingBufferMixin(unittest.TestCase):

    def tearDown(self):
        log_buffer.seek(0)
        log_buffer.truncate()

class JSONFormatterTestSuite(LoggingBufferMixin):
    """Basic test cases."""

    def setUp(self):
        stringio_handler.setFormatter(JSONFormatter(include_hostname=False))

    def test_hostname_missing(self):
        logger.debug('Sign %s up', 'Bob')
        dict_record = json.loads(log_buffer.getvalue())
        self.assertTrue('hostname' not in dict_record.keys())

    def test_default_key_order(self):
        logger.info("Key Order Test %(name)s", {"name": "Foo Bar 2"})
        dict_record = json.loads(log_buffer.getvalue(), object_pairs_hook=OrderedDict)
        record_map = JSONFormatter(include_hostname=False).record_map
        for idx, (actual, key) in enumerate(record_map):
            self.assertTrue(key == list(dict_record.items())[idx][0])

    def test_core_values_exist(self):
        msg = 'Log Entry %s'
        args = 32
        logger.error(msg, args)
        dict_record = json.loads(log_buffer.getvalue(), object_pairs_hook=OrderedDict)
        for k, v in dict_record.items():
            print(k, v)
            if k in ['timestamp', 'level_name', 'name', 'module', 'function_name', 'msg', 'message',
                     'thread_name', 'process_name', 'filename', 'path']:
                self.assertTrue(isinstance(v, str))
            elif k in ['level_no', 'line_number', 'thread', 'process']:
                self.assertTrue(isinstance(v, int))
            elif k in ['args']:
                self.assertTrue(isinstance(v, list))
            elif k in ['exception_text', 'exception_info', 'stack_info']:
                self.assertTrue(isinstance(v, type(None)))
            elif k in ['relative_created', ]:
                self.assertTrue(isinstance(v, float))

            if k == 'level_name':
                self.assertEqual(v, 'ERROR')
            if k == 'name':
                self.assertEqual(v, 'test')
            if k == 'module':
                self.assertEqual(v, 'test_logging')
            if k == 'function_name':
                self.assertEqual(v, 'test_core_values_exist')
            if k == 'msg':
                self.assertEqual(v, msg)
            if k == 'message':
                self.assertEqual(v, msg % args)
            if k == 'args':
                self.assertEqual(v, [args])
            if k == 'filename':
                self.assertEqual(v, 'test_logging.py')
            if k == 'path':
                self.assertTrue(v.endswith('test_logging.py'))


if __name__ == '__main__':
    unittest.main()