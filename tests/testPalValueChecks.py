#!/usr/bin/python3

import unittest


class NRequiredAssertValuesStringsTCTestCase(unittest.TestCase):

    def setUp(self):
        from src.Pal import Pal
        from tests.testclasses import StringTestClass
        self.pal = Pal()

    def test_n_required_assertion_values_missing_one(self):
        data = ["assertEqual"]
        result = self.pal.n_required_assertion_values(data)
        self.assertEqual(result, 1)

    def test_n_required_assertion_values_missing_zero(self):
        data = ["assertTrue"]
        result = self.pal.n_required_assertion_values(data)
        self.assertEqual(result, 0)


class NRequiredMethodValuesStringsTCTestCase(unittest.TestCase):

    def setUp(self):
        from src.Pal import Pal
        from tests.testclasses import StringTestClass
        self.pal = Pal()
        self.stc = StringTestClass.StringTestClass()
        self.pal.targets = self.pal.prepare_targets(self.stc)

    def test_n_required_method_values_contains_all_but_one(self):
        data = ["contains", "doug"]
        result = self.pal.n_required_method_values(data)
        self.assertEqual(result, 1)

    def test_n_required_method_values_contains_all_but_two(self):
        data = ["contains"]
        result = self.pal.n_required_method_values(data)
        self.assertEqual(result, 2)

    def test_n_required_method_values_zero_arg_method(self):
        data = ["panic"]
        result = self.pal.n_required_method_values(data)
        self.assertEqual(result, 0)

    def test_n_required_method_values_drop_vowels_with_none(self):
        data = ["drop_vowels"]
        result = self.pal.n_required_method_values(data)
        self.assertEqual(result, 1)

    def test_n_required_method_values_drop_vowels_with_one(self):
        data = ["drop_vowels", "doug"]
        result = self.pal.n_required_method_values(data)
        self.assertEqual(result, 0)

