#!/usr/bin/python3

import json
import unittest


class PalProcTestCase(unittest.TestCase):

    def setUp(self):
        from src.Pal import Pal
        self.pal = Pal()

    def test_proc_on_nothing(self):
        self.pal.proc(None)
        self.assertEqual(self.pal.tests, [])


class StringTCTestdictProcTestCase(unittest.TestCase):
    
    def setUp(self):
        from src.Pal import Pal
        from tests.testclasses import StringTestClass
        self.pal = Pal()
        self.stc = StringTestClass.StringTestClass()
        self.pal.targets = self.pal.prepare_targets(self.stc)
        with open("tests/testdocs/string_test_doc.json", "r") as _f:
            self.testdoc = json.load(_f)


    def test_proc_completed(self):
        data = []
        known = {"method": ["contains", "doug", "ug"],
                 "assertion": ["assertTrue"]}
        self.pal.proc(data, known)
        self.assertEqual(self.pal.tests[-1], known)

    def test_stringtc_testdoc_one(self):
        print(self.testdoc)
        data = self.testdoc["tests"][0]
        self.pal.proc(data)
        expected = {"method": ["drop_vowels", "you"],
                    "assertion": ["assertEqual", "y"]}
    
    #def test_proc_dute(self):
    #    from unittest import mock
    #    data = {"contains": ["doug", "ug"]}
    #    known = {"method": [],"assertion": ["assertTrue"]}
    #    with mock.patch.object(self.pal, "proc") as mock:
    #        self.pal.proc_dict(data, known)
    #    mock.assert_called_with({"_k": [5, 6]}, {})
