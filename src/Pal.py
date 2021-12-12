#!/usr/bin/python3

import importlib
from inspect import signature
from typing import Dict, List, Tuple, Union
from unittest import Class, TestCase

class Pal:

    def __init__(self, testdoc: Dict):

        _meta, _keys = testdoc["metadata"], list(testdoc["metadata"].keys())
        self.outpath = self.parse_outpath(_meta["outpath"])
        self.target = _meta["target"]
        self.alias = _meta["alias"] if "alias" in _keys else _meta["target"].lower()
        self.setup = True if "setup" in _keys else False
        self.teardown = True if "teardown" in _keys else False

        self.tests = []

        self.assertions = {_m: self.arg_count(TestCase, _m) 
                           for _m in self.methods(TestCase)
                           if _m.startswith("assert")
                           and not _m.endswith("_")  # ignore TestCase.assert_()
                           }

        _class = self.class_by_name(self.target[0], self.target[1])
        self.methods = {_m: self.arg_count(_class, _m)
                        for _m in self.methods(_class)
                        }

    def normalize_assertion(self, assertion: str) -> Union[str, bool]:
        if not assertion.startswith("assert"):
            assertion = f"assert{assertion.lower()}"
        else:
            assertion = assertion.lower()
        for _a in list(self.assertions):
            if assertion == _a[0].lower():
                return _a[0]
        return False

    def normalize_method(self, method_name: str) -> Union[str, bool]:
        for _m in list(self.methods):
            if method_name.lower() == _m.lower():
                return _m
        return False

    def class_by_name(self, class_name: str, class_path: str=None) -> Class:
        if class_path:
            _c = importlib.import_module(f"{class_path}.{class_name}")
        else:
            _c = importlib.import_module(class_name)
        return _c.__getattribute__(class_name)

    def methods(self, _class: Class) -> List[str]:
        return [_m for _m in dir(_class) if not _m.startswith("_")]

    def arg_count(self, _class: Class, method_name: str) -> int:
        sig = signature(_class.__getattribute__(method_name))
        return len([_i.strip() for _i
                    in str(sig)[1:-1].split(",")
                    if _i.strip() != "self"])

###
# From Visio file 

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
        return 2 + self.assertions[assertion] + self.methods["method_name"] 

    def proc(self, data: Dict, known: Dict=None):
        if not data:
            if self.validate(known):
                self.tests.append(known)
        known = {} if not known else known
        if type(data) == dict:
            self.proc_dict(data, known)
        elif type(data) == list:
            self.proc_list(data, known)
        elif type(data) == str:
            self.proc([data,], known)

    def proc_dict(self, data: Dict, known: Dict) -> None:
        if len(data.keys()) > 1:
        # split up job if multiple keys
            for _k in data.keys():
                self.proc(dict(_k = data[_k]), known)
        elif len(data.keys()) == 1:
            known = self.parse_values(list(data)[0], known)
            self.proc(data[list(data)[0]], known)

    def proc_list(self, data: List, known: Dict) -> None:
        _types = self.types_in_list(data)
        if "str" not in _types:
            for _d in data:
                self.proc(_d, known)
        if len(_types) > 1 and "str" in _types:
            values = [_d for _d in data if type(_d) == str]
            data = [_d for _d in data if type(_d) != str]
            known = self.parse_values(values, known)
            self.proc(data, known)

    def parse_values(self, values: List[str], known: Dict) -> Dict:
        """Adds all values to known and returns.
           * len(values) expected to equal n_required_values(known)"""
        if not known["method"]:
            for _i, _v in enumerate(values):
                if self.normalize_method(_v):
                    known["method"] = [self.normalize_method(_v),]
                    return self.parse_values(values, known)
        if not known["assertion"]:
            for _i, _v in enumerate(values):
                if self.normalize_assertion(_v):
                    known["assertion"] = [self.normalize_assertion(_v),]
                    return self.parse_values(values, known)
        method_values_needed = (self.methods[known["method"][0]] + 1 - len(known["method"]))
        if method_values_needed:
            known["method"] += values[:method_values_needed]
            if values[method_values_needed:] == []:
                return known
            return self.parse_values(values[method_values_needed:], known)
        assert_values_needed = (self.assertions[known["assertion"][0]] + 1 - len(known["assertion"]))
        if assert_values_needed:
            known["assertion"] += values[:assert_values_needed]
            if values[assert_values_needed:] == []:
                return known
            return self.parse_values(values[assert_values_needed:], known)

        


    def split_values(self, values: List[str], sublen: int) -> List[List[str]]:
        """Return len(values)/n lists of every n strings in values.
           * len(values) expected to be a multiple of n_required_values(known)"""
        pass  # TODO
                    #values = values[:_i][_i+1:]
            
