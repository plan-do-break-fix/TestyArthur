#!/usr/bin/python3

import unittest

class PalValidateTestCase(unittest.TestCase):

    def setUp(self):
        from src.Pal import Pal
        from tests.testclasses import StringTestClass
        self.pal = Pal()
        self.stc = StringTestClass.StringTestClass()
        self.pal.targets = self.pal.prepare_targets(self.stc)

    def test_contains_valid_doug(self):
        known = {"target_method": "contains",
                 "method_args": ["doug", "ug"],
                 "assertion": "assertTrue",
                 "assertion_args": []}
        result = self.pal.validate(known)
        self.assertTrue(result)

    def test_contains_invalid_doug_missing_method(self):
        known = {"target_method": "",
                 "method_args": ["doug", "ug"],
                 "assertion": "assertTrue",
                 "assertion_args": []}
        result = self.pal.validate(known)
        self.assertFalse(result)

    def test_drop_vowels_invalid_doug_missing_method(self):
        known = {"target_method": "",
                 "method_args": ["doug"],
                 "assertion": "assertEqual",
                 "assertion_args": ["dg"]}
        result = self.pal.validate(known)
        self.assertFalse(result)
