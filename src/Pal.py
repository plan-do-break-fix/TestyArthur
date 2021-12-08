#!/usr/bin/python3

import importlib
from inspect import signature
from typing import List, Union
from unittest import TestCase

ASSERTIONS = [_i for _i in dir(TestCase)     ## method -> [method, n_args]
              if _i.startswith("assert")
              and not _i.endswith("_")
              ]


def normalize_assertion(assertion: str) -> Union[str, bool]:
    """Attempts to match user input to a TextCase assertion.
    Args:
        assertion (str): User-submitted string
    Returns:
        Union[str, bool]: The name of a unittest.TestCase method name or False
    """
    if not assertion.startswith("assert"):
        assertion = f"assert{assertion.lower()}"
    else:
        assertion = assertion.lower()
    for _a in ASSERTIONS:
        if assertion == _a.lower():
            return _a
    return False

def normalize_method(method: str, METHODS: List[str]) -> Union[str, bool]:
    for _m in METHODS:
        if method.lower() == _m.lower():
            return _m
    return False

def target_as_object(target: List[str]) -> object:
    _c = importlib.import_module(f"{target[1]}.{target[0]}")
    return _c.__getattribute__(target[0])

def methods(target: List[str]) -> List[str]:
    _c = target_as_object(target)
    return [_m for _m in dir(_c) if not _m.startswith("_")]

def arg_count(target: List[str], methodName: str) -> int:
    _c = target_as_object(target)
    sig = signature(_c.__getattribute__(methodName))
    return len([_i.strip() for _i
                in str(sig)[1:-1].split(",")
                if _i.strip() != "self"])

## This one is making wanting a class for TARGET_METHODS
def extract_values(data: object, known: dict=None) -> dict:
    known = {} if not known else known
    if type(data) == dict:
        pass
    elif type(data) == list:
        pass

    
def assertion_values_from_list(data: list):
    pass
