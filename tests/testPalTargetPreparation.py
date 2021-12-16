#!/usr/bin/python3

import unittest


class StringTCTargetsTestCase(unittest.TestCase):

    def setUp(self):
        from src.Pal import Pal
        from tests.testclasses import StringTestClass
        self.pal = Pal()
        self.stc = StringTestClass.StringTestClass()

  # Pal.prepare_targets()
    def test_prepare_targets(self):
        result = self.pal.prepare_targets(self.stc)
        expected = {'contains': 2, 'drop_vowels': 1, 'panic': 0, 'resub': 3}
        self.assertEqual(result, expected)

  # Pal.normalize_assertion()
    def test_normalize_method_Compare(self):
        self.pal.targets = self.pal.prepare_targets(self.stc)
        result = self.pal.normalize_method("Contains")
        self.assertEqual(result, "contains")
        
    def test_normalize_method_DROP_VOWELS(self):
        self.pal.targets = self.pal.prepare_targets(self.stc)
        result = self.pal.normalize_method("DROP_VOWELS")
        self.assertEqual(result, "drop_vowels")


class DummyTCTargetsTestCase(unittest.TestCase):

    def setUp(self):
        from src.Pal import Pal
        from tests.testclasses import DummyTestClass
        self.pal = Pal()
        self.dum = DummyTestClass.DummyTestClass()

  # Pal.prepare_targets()
    def test_prepare_targets(self):
        result = self.pal.prepare_targets(self.dum)
        expected = {'passthrough': 1, 'default_none': 1}
        self.assertEqual(result, expected)

  # Pal.normalize_assertion()
    def test_normalize_method_Compare(self):
        self.pal.targets = self.pal.prepare_targets(self.dum)
        result = self.pal.normalize_method("PASSthrough")
        self.assertEqual(result, "passthrough")
        
    def test_normalize_method_DROP_VOWELS(self):
        self.pal.targets = self.pal.prepare_targets(self.dum)
        result = self.pal.normalize_method("default_none")
        self.assertEqual(result, "default_none")