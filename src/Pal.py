#!/usr/bin/python3

import importlib
from inspect import signature
from typing import List, Union
from unittest import Class, TestCase

class Pal:

    def __init__(self, testdoc: dict):

        self.candidates = []

        for _key in testdoc["metadata"]:
            self.__setattr__(self, _key, testdoc["metadata"][_key])

        self.assertions = {_m: self.arg_count(TestCase, _m) 
                           for _m in self.methods(TestCase)
                           if _m.startswith("assert")
                           and not _m.endswith("_")
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
        for _a in list(self.assertions.keys()):
            if assertion == _a[0].lower():
                return _a[0]
        return False

    def normalize_method(self, method_name: str) -> Union[str, bool]:
        for _m in list(self.methods.keys()):
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

    def extract_values(self, data: object, known: dict=None) -> None:
        known = {} if not known else known
        if type(data) == dict:
            # determine value type of key, add to known, recursive call on all values
            _keys = list(data.keys())
            for _k in _keys:
                _assertion = self.normalize_assertion(_k)
                if _assertion:
                    if not known["assertion"]:
                        known["assertion"] = [_assertion]
                    else:
                        # found duplicate assertions
                        raise RuntimeError
                else:
                    _method = self.normalize_method(_k)
                    if _method:
                        if not known["method"]:
                            known["method"] = _method
                        else:
                            # found two method names belonging to target
                            raise RuntimeError
                    else:
                        # assume it is first arg to pass to method being tested
                        if not known["args"]:
                            known["args"] = [_k]
                self.candidates.append(self.extract_values(data[_k], known))
        elif type(data) == str:
            self.candidates.append(self.extract_values([data], known))
        elif type(data) == list:
            if all([type(_i) in [list, dict] for _i in data]):
                # recursive call on all values
                for _i in data:
                    self.candidates.append(self.extract_values(_i, known))
            # determine if this is a terminal call
            if all([type(_i) == str for _i in data]):
                # terminal - process values, add to output
                for _i in data:
                    self.candidates.append(self.values_from_strings(_i, known))
            else:
                # add strings to known, recursive call on others
                strings = [_i for _i in data if type(_i) == str]
                others = [_i for _i in data if type(_i) != str]
                known = self.values_from_strings(strings, known)
                for _i in others:
                    self.candidates.append(self.extract_values(_i, known))
            
    def values_from_strings(self, values: List[str], known: dict) -> dict:
        added = []  # job finished if len(added) = len(values); used as filter on recursive calls
        if not known ["method"]:
            for _index, _value in enumerate(values):
                _method = self.normalize_method(_value)
                if _method:
                    known["method"] = [_method]
                    added.append(_method)
                    if self.methods[_method] > 1:
                        for _i in range(1, self.methods[_method]):
                            if not known["args"]:
                                known["args"] = []
                            known["args"].append(values[_index + _i])
                            added.append(values[_index + _i])
                            break
                    break
            if len(added) == len(values):
                return known
            else:
                self.values_from_strings([_v for _v in values if _v not in added])
        elif not known["assertion"]:
            for _index, _value in enumerate(values):
                _assertion = self.normalize_assertion(_value)
                if _assertion:
                    known["assertion"] = [_assertion]
                    added.append(_assertion)
                    if self.assertions[_assertion] > 1:
                        for _i in range(1, self.assertions[_assertion]):
                            known["assertion"].append(values[_index + _i])
                            added.append(values[_index + _i])
                            break
                    break
            if len(added) == len(values):
                return known
            else:
                self.values_from_strings([_v for _v in values if _v not in added])
        # check if all values are missing assertion arguments
        if  int(self.assertions[known["assertion"][0]]
                + 1
                - len(known["assertion"]))\
                == len(values):
                known["assertion"] += values
                return known
        # values must be arguments for method being tested
        if not known["args"]:
            known["args"] = []
        if  int(self.methods[known["method"]]
                + 1
                - len(known["args"]))\
                == len(values):
                known["args"] += values
                return known







