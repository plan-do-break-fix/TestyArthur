#!/usr/bin/python3

import hashlib
import json
from typing import List

VERSION = str(0.1)
BLANK = [0, ""]

class Author:

    def write_output(self, lines: List, outpath: str) -> bool:
        with open(f"{outpath}", "w") as _out:
            _out.writelines(lines)
        return True

    def author_import_lines(self, target) -> List[str]:
        lines = [[0, "import unittest"],]
        if len(target) == 1:
            lines.append([0, f"import {target[0]}"])
        elif len(target) == 2:
            lines.append([0, f"from {target[1]} import {target[0]}"])
        return lines

    def author_class_declaration_line(self, target) -> str:
        return f"class {target[0]}TestCase(unittest.TestCase):"

    def author_signature_lines(self) -> List[str]:
        return [[0, f"This file was authored by Testy Arthur v{VERSION}"],
                [0, "https://github.com/plan-do-break-fix/TestyArthur"]
                ]

    def author_setup_lines(self, instance_name: str, class_name: str) -> List[str]:
        return [[1, "def setUp(self):"],
                [2, f"self.{instance_name} = {class_name}()"]
               ]

    def author_teardown_lines(self, instance_name: str) -> bool:
        return [[1, "def tearDown(self):"],
                [2, f"self.{instance_name}.dispose()"]
               ]
    
    ## REFACTOR TESTDICT
    def author_test_definition(self, test: dict) -> str:
        md5hash = hashlib.md5()
        test_str = json.dumps(dict(method_name = test)).encode()
        md5hash.update(test_str)
        digest = md5hash.hexdigest()
        fingerprint = hex(int(digest[:16], 16) ^ int(digest[16:], 16))[2:]
        return f"def test_{test['method'][0]}_{fingerprint}(self):"

    def author_test_result(self, instance_name: str, method: List[str]) -> str:
        line = f"result = self.{instance_name}.{method[0]}("
        line += f"\"{method[1]}\""
        if len(method) > 1:
            for arg in method[2:]:
                line += f", \"{arg}\""
        line += ")"
        return line

    def author_test_assertion(self, assertion: List) -> str:
        line = f"self.assert{assertion[0]}(result"
        if len(assertion) > 1:
            line += f", \"{assertion[1]}\""
        line += ")"
        return line

    def author_python_lines(self, testdoc: dict) -> bool:
        target = testdoc["metadata"]["target"]
        alias = testdoc["metadata"]["alias"]
        lines = [[0, "#!/usr/bin/python3"],]
        lines += self.author_signature_lines()
        lines.append(BLANK)
        lines += self.author_import_lines(target)
        lines.append(BLANK)
        lines.append(self.author_class_declaration_line(target))
        lines.append(BLANK)
        if "setup" in testdoc["metadata"].keys():
            lines += self.author_setup_lines(alias, target[0])
            lines.append(BLANK)
        for testdict in testdoc["tests"]:
            method_name = testdict["method"][0]
            for test in testdoc["tests"][method_name]:
                lines += self.author_test(method_name,
                                          testdoc["metadata"]["alias"],
                                          test)
                lines.append(BLANK)
        if "teardown" in testdoc["metadata"].keys():
            lines += self.author_teardown_lines(alias)
            lines.append(BLANK)
        lines = [self.indent(_l[0], _l[1]) for _l in lines]
        return lines
        
    def author_test(self, instance_name: str, test: dict) -> List[str]:
        lines = []
        lines.append([1, self.author_test_definition(test)])
        lines.append([2, self.author_test_result(instance_name, test["method"])])
        lines.append([2, self.author_test_assertion(test["assertion"])])
        return lines

    
    def indent(self, level: int, line: str) -> str:
        return str(" "*level*4) + line
