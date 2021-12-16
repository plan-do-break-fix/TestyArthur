#!/usr/bin/python3

import unittest



class ParseStringTCTestCase(unittest.TestCase):

    def setUp(self):
        from src.Pal import Pal
        from tests.testclasses import StringTestClass
        self.pal = Pal()
        self.stc = StringTestClass.StringTestClass()
        self.pal.targets = self.pal.prepare_targets(self.stc)

  # StringTestCase.contains
    def test_parse_values_contains_last_value_assertion(self):
        data = ["assertTrue"]
        known = {"method": ["contains", "doug", "ug"],
                 "assertion": []}
        result = self.pal.parse_values(data, known)
        expected = {"method": ["contains", "doug", "ug"],
                 "assertion": ["assertTrue"]}
        self.assertEqual(result, expected)

    def test_parse_values_contains_last_value_method_arg(self):
        data = ["ug"]
        known = {"method": ["contains", "doug"],
                 "assertion": ["assertTrue"]}
        result = self.pal.parse_values(data, known)
        expected = {"method": ["contains", "doug", "ug"],
                 "assertion": ["assertTrue"]}
        self.assertEqual(result, expected)

    def test_parse_values_contains_all_method_args(self):
        data = ["contains", "doug", "ug"]
        known = {"method": [],
                 "assertion": ["assertTrue"]}
        result = self.pal.parse_values(data, known)
        expected = {"method": ["contains", "doug", "ug"],
                 "assertion": ["assertTrue"]}
        self.assertEqual(result, expected)
    
    def test_parse_values_contains_method_args(self):
        data = ["doug", "ug"]
        known = {"method": ["contains"],
                 "assertion": ["assertTrue"]}
        result = self.pal.parse_values(data, known)
        expected = {"method": ["contains", "doug", "ug"],
                 "assertion": ["assertTrue"]}
        self.assertEqual(result, expected)

    def test_parse_values_contains_all_in_list(self):
        known = {"method": [], "assertion": []}
        data = ["assertTrue", "contains", "doug", "ug"]
        result = self.pal.parse_values(data, known)
        expected = {"method": ["contains", "doug", "ug"],
                    "assertion": ["assertTrue"]}
        self.assertEqual(result, expected)

  # StringTestCase.drop_vowels()
    def test_parse_values_drop_vowels_last_value_assertion(self):
        data = ["dg"]
        known = {"method": ["drop_vowels", "doug"],
                 "assertion": ["assertEqual"]}
        result = self.pal.parse_values(data, known)
        expected = {"method": ["drop_vowels", "doug"],
                 "assertion": ["assertEqual", "dg"]}
        self.assertEqual(result, expected)

    def test_parse_values_drop_vowels_last_value_method_arg(self):
        data = ["doug"]
        known = {"method": ["drop_vowels"],
                 "assertion": ["assertEqual", "dg"]}
        result = self.pal.parse_values(data, known)
        expected = {"method": ["drop_vowels", "doug"],
                 "assertion": ["assertEqual", "dg"]}
        self.assertEqual(result, expected)

    def test_parse_values_drop_vowels_all_method_args(self):
        data = ["drop_vowels", "doug"]
        known = {"method": [],
                 "assertion": ["assertEqual", "dg"]}
        result = self.pal.parse_values(data, known)
        expected = {"method": ["drop_vowels", "doug"],
                 "assertion": ["assertEqual", "dg"]}
        self.assertEqual(result, expected)

    def test_parse_values_contains_all_in_list(self):
        known = {"method": [], "assertion": []}
        data = ["assertEqual", "drop_vowels", "doug", "dg"]
        result = self.pal.parse_values(data, known)
        expected = {"method": ["drop_vowels", "doug"],
                 "assertion": ["assertEqual", "dg"]}
        self.assertEqual(result, expected)
