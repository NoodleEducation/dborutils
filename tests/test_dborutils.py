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

    def test_create_from_mongo_spec_without_user_pass(self):
        mongo_spec = '127.0.0.1:development:categories'
        mongo_result = NoodleMongoClient.create_from_mongo_spec(mongo_spec)

        self.assertIsNotNone(mongo_result)

    def test_parse_argstring_with_user_pass(self):
        mongo_spec = 'noodle:pass@127.0.0.1:development:categories'
        mongo_connection_tuple = NoodleMongoClient.parse_argstring(mongo_spec)

        self.assertEqual(list(mongo_connection_tuple), ['noodle:pass@127.0.0.1', 27017,
                                                        'development', 'categories'])

    # def test_create_from_mongo_spec_with_user_pass(self):
    #     mongo_spec = 'noodle:pass@127.0.0.1:development:categories'
    #     mongo_result = NoodleMongoClient.create_from_mongo_spec(mongo_spec)
    #
    #     self.assertIsNotNone(mongo_result)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()