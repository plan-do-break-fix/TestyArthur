#!/usr/bin/python3

import unittest


class AssertionParsingTestCase(unittest.TestCase):

    def setUp(self):
        from src.Pal import Pal
        from unittest import TestCase
        self.pal = Pal()
        self.tc = TestCase()
  
  # Pal.n_required_args()
    def test_n_required_args_on_asserttrue(self):
        result = self.pal.n_required_args(self.tc, "assertTrue")
        self.assertEqual(result, 1)

    def test_n_required_args_on_assertfalse(self):
        result = self.pal.n_required_args(self.tc, "assertFalse")
        self.assertEqual(result, 1)

    def test_n_required_args_on_assertequal(self):
        result = self.pal.n_required_args(self.tc, "assertEqual")
        self.assertEqual(result, 2)

  # Pal.prepare_assertions()
    def test_prepare_assertions_returns_dict(self):
        result = self.pal.prepare_assertions()
        self.assertEqual(type(result), dict)

    def test_prepare_assertions_dict_has_int_values(self):
        result = self.pal.prepare_assertions()
        self.assertTrue(all([type(result[_k]) == int for _k in result]))

    def test_prepare_assertions_are_assertions(self):
        result = self.pal.prepare_assertions()
        self.assertTrue(all([_m.startswith("assert") for _m in result]))

  # Pal.normalize_assertion()
    def test_normalize_assertion_true(self):
        result = self.pal.normalize_assertion("true")
        self.assertEqual(result, "assertTrue")

    def test_normalize_assertion_TRUE(self):
        result = self.pal.normalize_assertion("TRUE")
        self.assertEqual(result, "assertTrue")

    def test_normalize_assertion_ASSERTequaL(self):
        result = self.pal.normalize_assertion("ASSERTequaL")
        self.assertEqual(result, "assertEqual")

    def test_normalize_assertion_bad_input(self):
        result = self.pal.normalize_assertion("worm gaming")
        self.assertFalse(result)
