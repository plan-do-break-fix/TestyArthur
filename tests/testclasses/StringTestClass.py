#!/usr/bin/python3

import re

class StringTestClass:

    def drop_vowels(self, a):
        """For testing single argument method."""
        return ''.join([_c for _c in a if _c not in ['a', 'e', 'i', 'o', 'u']])

    def contains(self, a, b):
        """For testing two argument method."""
        return b in a

    def resub(self, a, b, c):
        """For testing multi-argument method using additional imported module."""
        return re.sub(a, b, c)
    
    def panic(self):
        return str(42)