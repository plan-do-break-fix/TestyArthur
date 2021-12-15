#!/usr/bin/python3

import unittest



class ParseStringTCTestCase(unittest.TestCase):

    def setUp(self):
        from src.Pal import Pal
        from tests.testclasses import StringTestClass
        self.pal = Pal()
        self.stc = StringTestClass.StringTestClass()
        self.pal.targets = self.pal.prepare_targets(self.stc)

    def test_parse_values_last_value_assertion(self):
        data = ["assertTrue"]
        known = {"method": ["contains", "doug", "ug"],
                 "assertion": []}
        result = self.pal.parse_values(data, known)
        self.assertEqual(result["assertion"][0], "assertTrue")

    def test_parse_values_last_value_method_arg(self):
        data = ["ug"]
        known = {"method": ["contains", "doug"],
                 "assertion": ["assertTrue"]}
        result = self.pal.parse_values(data, known)
        self.assertEqual(len(result["method"]), 3)

    def test_parse_values_all_method_args(self):
        data = ["contains", "doug", "ug"]
        known = {"method": [],
                 "assertion": ["assertTrue"]}
        result = self.pal.parse_values(data, known)
        self.assertEqual(result["method"], ["contains", "doug", "ug"])
    
    def test_parse_values_method_args(self):
        data = ["doug", "ug"]
        known = {"method": ["contains"],
                 "assertion": ["assertTrue"]}
        result = self.pal.parse_values(data, known)
        self.assertEqual(len(result["method"]), 3)

    def test_parse_values_all_in_list(self):
        known = {"method": [], "assertion": []}
        data = ["assertTrue", "contains", "doug", "ug"]
        result = self.pal.parse_values(data, known)
        expected = {"method": ["contains", "doug", "ug"],
                    "assertion": ["assertTrue"]}
        self.assertEqual(result, expected)
