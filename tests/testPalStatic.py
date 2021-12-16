#!/usr/bin/python3

import unittest


class TypesInListTestCase(unittest.TestCase):

    def setUp(self):
        from src.Pal import Pal
        self.pal = Pal()

    def test_mixed_list_all_types(self):
        data = ["", "", {}, [], {}, "", {}]
        result = self.pal.types_in_list(data)
        result.sort()
        expected = ["dict", "list", "str"]
        self.assertEqual(result, expected)

    def test_empty_list(self):
        data = []
        result = self.pal.types_in_list(data)
        expected = []
        self.assertEqual(result, expected)

    def test_list_of_strings(self):
        data = ["", ""]
        result = self.pal.types_in_list(data)
        expected = ["str"]
        self.assertEqual(result, expected)

    def test_list_of_lists(self):
        data = [[], [], []]
        result = self.pal.types_in_list(data)
        expected = ["list"]
        self.assertEqual(result, expected)

    def test_list_of_dicts(self):
        data = [{}, {}, {}]
        result = self.pal.types_in_list(data)
        expected = ["dict"]
        self.assertEqual(result, expected)


class ListMethodsTestCase(unittest.TestCase):

    def setUp(self):
        from src.Pal import Pal
        self.pal = Pal()

    def test_string_testclass(self):
        from tests.testclasses import StringTestClass
        stringy = StringTestClass.StringTestClass()
        result = self.pal.list_methods(stringy)
        expected = ["contains", "drop_vowels", "panic", "resub"]
        self.assertEqual(result, expected)

    def test_dummy_testclass(self):
        from tests.testclasses import DummyTestClass
        stringy = DummyTestClass.DummyTestClass()
        result = self.pal.list_methods(stringy)
        expected = ["default_none", "passthrough"]
        self.assertEqual(result, expected)


