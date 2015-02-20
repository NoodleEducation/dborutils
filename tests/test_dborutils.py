#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_dborutils
----------------------------------

Tests for `dborutils` module.
"""

import unittest

from dborutils import dborutils
from dborutils.mongo_client import NoodleMongoClient


class TestDborutils(unittest.TestCase):

    def setUp(self):
        pass

    def test_parse_argstring_without_user_pass(self):
        mongo_spec = '127.0.0.1:development:categories'
        mongo_connection_tuple = NoodleMongoClient.parse_argstring(mongo_spec)

        self.assertEqual(list(mongo_connection_tuple),
                         ['mongodb://127.0.0.1:27017/development', 27017,
                          'development', 'categories'])

    def test_parse_argstring_with_user_pass(self):
        mongo_spec = 'noodle:pass@127.0.0.1:development:categories'
        mongo_connection_tuple = NoodleMongoClient.parse_argstring(mongo_spec)

        self.assertEqual(list(mongo_connection_tuple),
                         ['mongodb://noodle:pass@127.0.0.1:27017/development', 27017,
                          'development', 'categories'])

    def test_parse_db_argstring_without_user_pass(self):
        mongo_spec = '127.0.0.1:development'
        mongo_connection_tuple = NoodleMongoClient.parse_db_argstring(mongo_spec)

        self.assertEqual(list(mongo_connection_tuple),
                         ['mongodb://127.0.0.1:27017/development', 27017,
                          'development'])

    def test_parse_db_argstring_with_user_pass(self):
        mongo_spec = 'noodle:pass@127.0.0.1:development'
        mongo_connection_tuple = NoodleMongoClient.parse_db_argstring(mongo_spec)

        self.assertEqual(list(mongo_connection_tuple),
                         ['mongodb://noodle:pass@127.0.0.1:27017/development', 27017,
                          'development'])

    def test_parse_db_argstring_with_user_pass_localhost(self):
        mongo_spec = 'noodle:pass@localhost:development'
        mongo_connection_tuple = NoodleMongoClient.parse_db_argstring(mongo_spec)

        self.assertEqual(list(mongo_connection_tuple),
                         ['mongodb://noodle:pass@localhost:27017/development', 27017,
                          'development'])

    def test_parse_db_argstring_with_user_pass_localhost_with_port(self):
        mongo_spec = 'noodle:pass@localhost:27017:development'
        mongo_connection_tuple = NoodleMongoClient.parse_db_argstring(mongo_spec)

        self.assertEqual(list(mongo_connection_tuple),
                         ['mongodb://noodle:pass@localhost:27017/development', 27017,
                          'development'])

    def test_parse_db_argstring_with_user_pass_no_host(self):
        mongo_spec = 'noodle:pass@development'

        with self.assertRaises(Exception):
            NoodleMongoClient.parse_db_argstring(mongo_spec)

    def test_parse_db_argstring_without_user_pass_no_host(self):
        mongo_spec = 'development'

        with self.assertRaises(Exception):
            NoodleMongoClient.parse_db_argstring(mongo_spec)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()