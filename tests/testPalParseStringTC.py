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
        known = {"target_method": "contains", 
                 "method_args": ["doug", "ug"],
                 "assertion": "",
                 "assertion_args": []}
        result = self.pal.parse_values(data, known)
        expected = {"target_method": "contains", 
                    "method_args": ["doug", "ug"],
                    "assertion": "assertTrue",
                    "assertion_args": []}
        self.assertEqual(result, expected)

    def test_parse_values_contains_last_value_method_arg(self):
        data = ["ug"]
        known = {"target_method": "contains", 
                 "method_args": ["doug"],
                 "assertion": "assertTrue",
                 "assertion_args": []}
        result = self.pal.parse_values(data, known)
        expected = {"target_method": "contains", 
                    "method_args": ["doug", "ug"],
                    "assertion": "assertTrue",
                    "assertion_args": []}
        self.assertEqual(result, expected)

    def test_parse_values_contains_all_method_args(self):
        data = ["contains", "doug", "ug"]
        known = {"target_method": "", 
                 "method_args": [],
                 "assertion": "assertTrue",
                 "assertion_args": []}
        result = self.pal.parse_values(data, known)
        expected = {"target_method": "contains", 
                    "method_args": ["doug", "ug"],
                    "assertion": "assertTrue",
                    "assertion_args": []}
        self.assertEqual(result, expected)
    
    def test_parse_values_contains_method_args(self):
        data = ["doug", "ug"]
        known = {"target_method": "contains", 
                 "method_args": [],
                 "assertion": "assertTrue",
                 "assertion_args": []}
        result = self.pal.parse_values(data, known)
        expected = {"target_method": "contains", 
                    "method_args": ["doug", "ug"],
                    "assertion": "assertTrue",
                    "assertion_args": []}
        self.assertEqual(result, expected)

    def test_parse_values_contains_all_in_list(self):
        data = ["assertTrue", "contains", "doug", "ug"]
        known = {"target_method": "", 
                 "method_args": [],
                 "assertion": "",
                 "assertion_args": []}
        result = self.pal.parse_values(data, known)
        expected = {"target_method": "contains", 
                    "method_args": ["doug", "ug"],
                    "assertion": "assertTrue",
                    "assertion_args": []}
        self.assertEqual(result, expected)

  # StringTestCase.drop_vowels()
    def test_parse_values_drop_vowels_last_value_assertion(self):
        data = ["dg"]
        known = {"target_method": "drop_vowels",
                 "method_args": ["doug"],
                 "assertion": "assertEqual",
                 "assertion_args": []}
        result = self.pal.parse_values(data, known)
        expected = {"target_method": "drop_vowels",
                 "method_args": ["doug"],
                 "assertion": "assertEqual",
                 "assertion_args": ["dg"]}
        self.assertEqual(result, expected)

    def test_parse_values_drop_vowels_last_value_method_arg(self):
        data = ["doug"]
        known = {"target_method": "drop_vowels",
                 "method_args": [],
                 "assertion": "assertEqual",
                 "assertion_args": ["dg"]}
        result = self.pal.parse_values(data, known)
        expected = {"target_method": "drop_vowels",
                    "method_args": ["doug"],
                    "assertion": "assertEqual",
                    "assertion_args": ["dg"]}
        self.assertEqual(result, expected)

    def test_parse_values_drop_vowels_all_method_args(self):
        data = ["drop_vowels", "doug"]
        known = {"target_method": "",
                 "method_args": [],
                 "assertion": "assertEqual",
                 "assertion_args": ["dg"]}
        result = self.pal.parse_values(data, known)
        expected = {"target_method": "drop_vowels",
                    "method_args": ["doug"],
                    "assertion": "assertEqual",
                    "assertion_args": ["dg"]}
        self.assertEqual(result, expected)

    def test_parse_values_contains_all_in_list(self):
        data = ["assertEqual", "drop_vowels", "doug", "dg"]
        known = {"target_method": "",
                 "method_args": [],
                 "assertion": "",
                 "assertion_args": []}
        result = self.pal.parse_values(data, known)
        expected = {"target_method": "drop_vowels",
                    "method_args": ["doug"],
                    "assertion": "assertEqual",
                    "assertion_args": ["dg"]}
        self.assertEqual(result, expected)
