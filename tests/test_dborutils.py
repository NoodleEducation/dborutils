# -*- coding: utf-8 -*-

"""
Tests for the dborutils repo.
"""

import re
from mock import patch
from unittest import TestCase
import unittest

from dborutils.mongo_client import NoodleMongoClient
from dborutils.key_service import NoodleKeyService


class TestDborutils(TestCase):

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

    def fake_is_unique(self, candidate_nice_key):
        return True

    @patch('dborutils.key_service.NoodleKeyService._is_nice_key_unique')
    def test_key_service(self, fake_is_unique):
        nks = NoodleKeyService()
        test_key = nks.generate_nice_key(prefix="yz")
        self.assertTrue(re.match("yz\w\w\w\w\w\w\w\w\w\w", test_key))

if __name__ == '__main__':
    unittest.main()
