#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_dborutils
----------------------------------

Tests for `dborutils` module.
"""

import unittest

from dborutils.mongo_client import NoodleMongoClient


class TestDborutils(unittest.TestCase):

    def setUp(self):
        pass

    def test_parse_argstring_without_user_pass(self):
        mongo_spec = '127.0.0.1:local:categories'
        mongo_connection_tuple = NoodleMongoClient.parse_argstring(mongo_spec)

        self.assertEqual(list(mongo_connection_tuple),
                         ['mongodb://127.0.0.1:27017/local', 27017,
                          'local', 'categories'])

    def test_parse_argstring_with_user_pass(self):
        mongo_spec = 'noodle:pass@127.0.0.1:local:categories'
        mongo_connection_tuple = NoodleMongoClient.parse_argstring(mongo_spec)

        self.assertEqual(list(mongo_connection_tuple),
                         ['mongodb://noodle:pass@127.0.0.1:27017/local', 27017,
                          'local', 'categories'])

    def test_parse_db_argstring_without_user_pass(self):
        mongo_spec = '127.0.0.1:local'
        mongo_connection_tuple = NoodleMongoClient.parse_db_argstring(mongo_spec)

        self.assertEqual(list(mongo_connection_tuple),
                         ['mongodb://127.0.0.1:27017/local', 27017,
                          'local'])

    def test_parse_db_argstring_with_user_pass(self):
        mongo_spec = 'noodle:pass@127.0.0.1:local'
        mongo_connection_tuple = NoodleMongoClient.parse_db_argstring(mongo_spec)

        self.assertEqual(list(mongo_connection_tuple),
                         ['mongodb://noodle:pass@127.0.0.1:27017/local', 27017,
                          'local'])

    def test_parse_db_argstring_with_user_pass_localhost(self):
        mongo_spec = 'noodle:pass@localhost:local'
        mongo_connection_tuple = NoodleMongoClient.parse_db_argstring(mongo_spec)

        self.assertEqual(list(mongo_connection_tuple),
                         ['mongodb://noodle:pass@localhost:27017/local', 27017,
                          'local'])

    def test_parse_db_argstring_with_user_pass_localhost_with_port(self):
        mongo_spec = 'noodle:pass@localhost:27017:local'
        mongo_connection_tuple = NoodleMongoClient.parse_db_argstring(mongo_spec)

        self.assertEqual(list(mongo_connection_tuple),
                         ['mongodb://noodle:pass@localhost:27017/local', 27017,
                          'local'])

    def test_parse_db_argstring_with_user_pass_no_host(self):
        mongo_spec = 'noodle:pass@local'

        with self.assertRaises(Exception):
            NoodleMongoClient.parse_db_argstring(mongo_spec)

    def test_parse_db_argstring_without_user_pass_no_host(self):
        mongo_spec = 'local'

        with self.assertRaises(Exception):
            NoodleMongoClient.parse_db_argstring(mongo_spec)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
