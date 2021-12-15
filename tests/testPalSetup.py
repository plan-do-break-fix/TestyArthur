#!/usr/bin/python3

import unittest


class SetupPalTestCase(unittest.TestCase):

    def test_pal_import(self):
        from src.Pal import Pal
        self.assertTrue(Pal)

    def test_pal_init(self):
        from src.Pal import Pal
        pal = Pal()
        self.assertTrue(pal)


class SetupStringTCTestCase(unittest.TestCase):

    def test_string_testclass_import(self):
        from tests.testclasses import StringTestClass
        self.assertTrue(StringTestClass)
    
    def test_string_testclass_init(self):
        from tests.testclasses import StringTestClass
        self.strings = StringTestClass.StringTestClass()
        self.assertTrue(self.strings)


class SetupDummyTCTestCase(unittest.TestCase):

    def test_dummy_testclass_import(self):
        from tests.testclasses import DummyTestClass
        self.assertTrue(DummyTestClass)
    
    def test_dummy_testclass_init(self):
        from tests.testclasses import DummyTestClass
        self.dummy = DummyTestClass.DummyTestClass()
        self.assertTrue(self.dummy)
