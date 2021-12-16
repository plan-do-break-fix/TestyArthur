#!/usr/bin/python3

import re

class DummyTestClass:

    def passthrough(self, a):
        return a

    def default_none(self, a, b=None):
        return b if b else a

    def __ignore__(self):
        return None