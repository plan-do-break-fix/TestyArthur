#!/usr/bin/python3

import unittest

class SetupPalTestCase(unittest.TestCase):

    def test_string_testclass_import(self):
        from tests import StringTestClass
        self.strings = StringTestClass.StringTestClass()
        self.assertTrue(self.strings)

    def test_pal_import(self):
        from src.Pal import Pal
        self.assertTrue(Pal)

    def test_pal_init(self):
        from src.Pal import Pal
        pal = Pal()
        self.assertTrue(pal)


class AssertionsPalTestCase(unittest.TestCase):

    def setUp(self):
        from src.Pal import Pal
        self.pal = Pal()
        self.tc = unittest.TestCase()

  # Pal.types_in_list()
    def test_types_in_list_everything(self):
        data = ["", "", {}, [], {}, "", {}]
        result = self.pal.types_in_list(data)
        result.sort()
        expected = ["dict", "list", "str"]
        self.assertEqual(result, expected)

    def test_types_in_list_empty(self):
        data = []
        result = self.pal.types_in_list(data)
        expected = []
        self.assertEqual(result, expected)

    def test_types_in_list_strings(self):
        data = ["", ""]
        result = self.pal.types_in_list(data)
        expected = ["str"]
        self.assertEqual(result, expected)

    def test_types_in_list_lists(self):
        data = [[], [], []]
        result = self.pal.types_in_list(data)
        expected = ["list"]
        self.assertEqual(result, expected)

  # pal.list_methods()
    def test_methods_on_testcase_returns_list(self):
        result = self.pal.list_methods(self.tc)
        self.assertEqual(type(result), list)

    def test_methods_on_testcase_list_length(self):
        result = self.pal.list_methods(self.tc)
        self.assertEqual(len(result), 69)

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


class StringTCPalTestCase(unittest.TestCase):

    def setUp(self):
        from src.Pal import Pal
        from tests import StringTestClass
        self.pal = Pal()
        self.stc = StringTestClass.StringTestClass()

  # Pal.list_methods()
    def test_methods_on_json_returns_list(self):
        result = self.pal.list_methods(self.stc)
        self.assertEqual(type(result), list)

    def test_methods_on_json_list_length(self):
        result = self.pal.list_methods(self.stc)
        self.assertEqual(len(result), 4)

  # Pal.prepare_targets()
    def test_prepare_targets_returns_dict(self):
        result = self.pal.prepare_targets(self.stc)
        self.assertEqual(type(result), dict)

    def test_prepare_targets_dict_has_int_values(self):
        result = self.pal.prepare_targets(self.stc)
        self.assertTrue(all([type(result[_k]) == int for _k in result]))

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

  # Pal.validate()
    def test_validate_empty(self):
        result = self.pal.validate({})
        self.assertFalse(result)

  # Pal.proc methods
    def test_proc_on_nothing(self):
        self.pal.proc(None)
        self.assertEqual(self.pal.tests, [])


    #def test_proc_dict_alpha(self):
    #    data = {"assertTrue": []}

class ParseStringTCPalTestCase(unittest.TestCase):

    def setUp(self):
        from src.Pal import Pal
        from tests import StringTestClass
        self.pal = Pal()
        self.stc = StringTestClass.StringTestClass()
        self.pal.targets = self.pal.prepare_targets(self.stc)
        print(self.pal.targets)

  # Pal.n_required_method_values()
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

  # Pal.n_requires_assertion_values()
    def test_n_required_assertion_values_missing_one(self):
        data = ["assertEqual"]
        result = self.pal.n_required_assertion_values(data)
        self.assertEqual(result, 1)

    def test_n_required_assertion_values_missing_zero(self):
        data = ["assertTrue"]
        result = self.pal.n_required_assertion_values(data)
        self.assertEqual(result, 0)

  # Pal.parse_values()
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

class ProcStringTCPalTestCase(unittest.TestCase):

    def setUp(self):

        from src.Pal import Pal
        from tests import StringTestClass
        self.pal = Pal()
        self.stc = StringTestClass.StringTestClass()
        self.pal.targets = self.pal.prepare_targets(self.stc)

    #def test_proc_completed_known(self):
    #    data = []
    #    known = {"method": ["contains", "doug", "ug"],
    #             "assertion": ["assertTrue"]}
    #    self.pal.proc(data, known)
    #    self.assertEqual(self.pal.tests[-1], known)

    
    #def test_proc_dict_multiple_keys(self):
    #    from unittest import mock
    #    data = {"one": [1,2], "two": [3,4], "three": [5,6]}
    #    with mock.patch.object(self.pal, "proc") as mock:
    #        self.pal.proc_dict(data, {})
    #    mock.assert_called_with({"_k": [5, 6]}, {})

    #def test_proc_dute(self):
    #    from unittest import mock
    #    data = {"contains": ["doug", "ug"]}
    #    known = {"method": [],"assertion": ["assertTrue"]}
    #    with mock.patch.object(self.pal, "proc") as mock:
    #        self.pal.proc_dict(data, known)
    #    mock.assert_called_with({"_k": [5, 6]}, {})