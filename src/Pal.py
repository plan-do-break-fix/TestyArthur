#!/usr/bin/python3

#import importlib
from inspect import signature
from typing import Dict, List, Tuple, Union
import unittest

class Pal:

    def __init__(self):
        self.tests = []
        self.assertions = self.prepare_assertions()
        self.targets = {}

    #    _meta, _keys = testdoc["metadata"], list(testdoc["metadata"].keys())
    #    self.outpath = self.parse_outpath(_meta["outpath"])
    #    self.target = _meta["target"]
    #    self.alias = _meta["alias"] if "alias" in _keys else _meta["target"].lower()
    #    self.setup = True if "setup" in _keys else False
    #    self.teardown = True if "teardown" in _keys else False

    def prepare_assertions(self) -> Dict:
        _tc = unittest.TestCase()
        assertion_names = [_m for _m in self.list_methods(_tc)
                           if _m.startswith("assert")
                           and not _m.endswith("_")]
        return {_m: self.n_required_args(_tc, _m) for _m in assertion_names}

    def normalize_assertion(self, assertion: str) -> Union[str, bool]:
        if not assertion.lower().startswith("assert"):
            assertion = f"assert{assertion.lower()}"
        else:
            assertion = assertion.lower()
        for _a in list(self.assertions.keys()):
            if assertion == _a.lower():
                return _a
        return False

    def prepare_targets(self, _instance: object) -> Dict:
        targets = self.list_methods(_instance)
        return {_m: self.n_required_args(_instance, _m) for _m in targets}


    def normalize_method(self, method_name: str) -> Union[str, bool]:
        for _m in list(self.targets.keys()):
            if method_name.lower() == _m.lower():
                return _m
        return False

    def list_methods(self, _class: object) -> List[str]:
        return [_m for _m in dir(_class) if not _m.startswith("_")]

    def n_required_args(self, _class: object, method_name: str) -> int:
        sig = signature(_class.__getattribute__(method_name))
        if str(sig) == "()":
            return 0
        return len([_i.strip() for _i
                    in str(sig)[1:-1].split(",")
                    if _i.strip() != "self"
                      and "=" not in _i
                    ])

    def types_in_list(self, _list: List[object]) -> List[str]:
        """Returns a list of distinct object types contained in _list."""
        types = [str(type(_i)).split("'")[1] for _i in _list]
        if len(types) > 1:
            types = list(set(types))
        return types

    def n_known_values(self, known:dict) -> int:
        """Returns the number of values in a known values dictionary."""
        _n = 1 if known["method"] else 0
        return _n + len(known["args"]) + len(known["assertion"])

    def n_required_values(self, method_name: str, assertion: str) -> int:
        """Returns number of values required to complete a known values dict for
           a given normalized method, normalized assertion pair."""
        # The method to test and the assertion itself make two
        return 2 + self.assertions[assertion] + self.list_methods["method_name"] 

    def n_required_assertion_values(self, assertion_array: List) -> int:
        n_current = len(assertion_array)
        min_required = self.assertions[str(assertion_array[0])]
        return int(min_required - n_current) # +1 for assertion itself, -1 for implied result

    def n_required_method_values(self, method_array: List) -> int:
        """Returns minimum number of missing values in known['method'].
           * method_array[0] expected to contain method name."""
        n_current = len(method_array)
        min_required = self.targets[str(method_array[0])]
        return int(min_required + 1 - n_current)  #  +1 for method itself in [0]

    def proc(self, data: Dict, known: Dict=None):
        if not data and known:
            if self.validate(known):
                self.tests.append(known)
        known = {"method": [], "assertion": []} if not known else known
        if type(data) == dict:
            self.proc_dict(data, known)
        elif type(data) == list:
            self.proc_list(data, known)
        elif type(data) == str:
            self.proc([data,], known)

    def proc_dict(self, data: Dict, known: Dict) -> None:
        if len(data.keys()) > 1:
        # split up job if multiple keys
            for _k in list(data):
                self.proc(dict(_k = data[_k]), known)
        elif len(data.keys()) == 1:
            known = self.parse_values(list(data)[0], known, judge=False)
            self.proc(data[list(data)[0]], known)

    def proc_list(self, data: List, known: Dict) -> None:
        _types = self.types_in_list(data)
        if "str" not in _types:
            for _d in data:
                self.proc(_d, known)
        if len(_types) > 1 and "str" in _types:
            values = [_d for _d in data if type(_d) == str]
            data = [_d for _d in data if type(_d) != str]
            known = self.parse_values(values, known, judge=False)
            self.proc(data, known)

    def parse_values(self, values: List[str], known: Dict, judge=True) -> Union[Dict, bool]:
        """Adds all values to known and returns.
    #NO       * len(values) expected to equal n_required_values(known)  # This is declared with judge instead
           * judge is used to catch invalid testdicts
               - should be True when all remaining values are in values list
               - should be False otherwise (values taken from lists of heterogenous types)
        """
        if not known["method"]:
            _m, values = self.extract_method(values)
            if judge and not _m:
                return False
            known["method"] = [_m,] if _m else []
        if not known["assertion"]:
            _a, values = self.extract_assertion(values)
            if judge and not _a:
                return False
            known["assertion"] = [_a,] if _a else []
        method_values_needed = self.n_required_method_values(known["method"])
        if method_values_needed:
            known["method"] += values[:method_values_needed]
            values = values[method_values_needed:]
        assert_values_needed = self.n_required_assertion_values(known["assertion"])
        if assert_values_needed:
            known["assertion"] += values[:assert_values_needed]
            values = values[assert_values_needed:]
        if not values:
            return known
        return self.parse_values(values, known)

    def extract_assertion(self, values: List[str]) -> Tuple[str, List[str]]:
        for _i, _v in enumerate(values):
            if self.normalize_assertion(_v):
                return (self.normalize_assertion(_v), values[:_i] + values[_i+1:])
        return ("", values)

    def extract_method(self, values: List[str]) -> Tuple[str, List[str]]:
        for _i, _v in enumerate(values):
            if self.normalize_method(_v):
                return (self.normalize_method(_v), values[:_i] + values[_i+1:])
        return ("", values)


    def validate(self, known: dict):
        return True if ("method" in known.keys()
                        and "assertion" in known.keys()
                        and known["method"]
                        and known["assertion"]
                        ) else False


    def split_values(self, values: List[str], sublen: int) -> List[List[str]]:
        """Return len(values)/n lists of every n strings in values.
           * len(values) expected to be a multiple of n_required_values(known)"""
        pass  # TODO
                    #values = values[:_i][_i+1:]

    def parse_outpath(self, outpath: str):
        return outpath  # TODO
            
