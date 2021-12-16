#!/usr/bin/python3

import unittest


class NRequiredAssertValuesStringsTCTestCase(unittest.TestCase):

    def setUp(self):
        from src.Pal import Pal
        from tests.testclasses import StringTestClass
        self.pal = Pal()

    def test_n_required_assertion_values_missing_one(self):
        data = {"assertion": "assertEqual", "assertion_args": []}
        result = self.pal.n_required_assertion_values(data)
        self.assertEqual(result, 1)

    def test_n_required_assertion_values_missing_zero(self):
        data = {"assertion": "assertTrue", "assertion_args": []}
        result = self.pal.n_required_assertion_values(data)
        self.assertEqual(result, 0)


class NRequiredMethodValuesStringsTCTestCase(unittest.TestCase):

    def setUp(self):
        from src.Pal import Pal
        from tests.testclasses import StringTestClass
        self.pal = Pal()
        self.stc = StringTestClass.StringTestClass()
        self.pal.targets = self.pal.prepare_targets(self.stc)

    def test_n_required_method_values_contains_missing_two(self):
        data = {"target_method": "contains", "method_args": []}
        result = self.pal.n_required_method_values(data)
        self.assertEqual(result, 2)

    def test_n_required_method_values_contains_missing_one(self):
        data = {"target_method": "contains", "method_args": ["doug"]}
        result = self.pal.n_required_method_values(data)
        self.assertEqual(result, 1)

    def test_n_required_method_values_contains_missing_none(self):
        data = {"target_method": "contains", "method_args": ["doug", "ug"]}
        result = self.pal.n_required_method_values(data)
        self.assertEqual(result, 0)

    def test_n_required_method_values_zero_arg_method(self):
        data = {"target_method": "panic", "method_args": []}
        result = self.pal.n_required_method_values(data)
        self.assertEqual(result, 0)

    def test_n_required_method_values_drop_vowels_missing_one(self):
        data = {"target_method": "drop_vowels", "method_args": []}
        result = self.pal.n_required_method_values(data)
        self.assertEqual(result, 1)

    def test_n_required_method_values_drop_vowels_missing_none(self):
        data = {"target_method": "drop_vowels", "method_args": ["doug"]}
        result = self.pal.n_required_method_values(data)
        self.assertEqual(result, 0)

