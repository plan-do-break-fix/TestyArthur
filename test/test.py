#!/usr/bin/python3

import json
import unittest

from src import Author

class GenericTestCase(unittest.TestCase):

    def setUp(self):
        self.author = Author.Author()

    def test_author_signature_lines(self):
        result = self.author.author_signature_lines()
        expected = [[0, "This file was authored by Testy Arthur v0.1"],
                    [0, "https://github.com/plan-do-break-fix/TestyArthur"]]
        self.assertEqual(result, expected)

    def test_indent_blank_line(self):
        result = self.author.indent(0, "")
        expected = ""
        self.assertEqual(result, expected)

    def test_indent_line_level_zero(self):
        result = self.author.indent(0, "Gde moi yablaka?")
        expected = "Gde moi yablaka?"
        self.assertEqual(result, expected)

    def test_indent_line_level_two(self):
        result = self.author.indent(2, "Gde moi yablaka?")
        expected = "        Gde moi yablaka?"
        self.assertEqual(result, expected)

class MathsTestCase(unittest.TestCase):

    def setUp(self):
        self.author = Author.Author()
        with open('./test/testdocs/maths_test_doc.json') as _f:
            self.testdoc = json.load(_f)

    def test_author_import_lines(self):
        result = self.author.author_import_lines(self.testdoc["metadata"]["target"])
        expected = [[0, "import unittest"], 
                    [0, "from test.TestClasses import MathsTestClass"]
                    ]
        self.assertEqual(result, expected)

    def test_author_class_declaration_line(self):
        result = self.author.author_class_declaration_line(self.testdoc["metadata"]["target"])
        expected = "class MathsTestClassTestCase(unittest.TestCase):"   
        self.assertEqual(result, expected)

    def test_author_setup_lines(self):
        result = self.author.author_setup_lines(self.testdoc["metadata"]["alias"],
                                         self.testdoc["metadata"]["target"][0])
        expected = [[1, "def setUp(self):"],
                    [2, "self.maths = MathsTestClass()"]
                    ]
        self.assertEqual(result, expected)

    def test_author_teardown_lines(self):
        result = self.author.author_teardown_lines(self.testdoc["metadata"]["alias"])
        expected = [[1, "def tearDown(self):"],
                    [2, "self.maths.dispose()"]
                    ]
        self.assertEqual(result, expected)

    def test_author_test_definition(self):
        result = self.author.author_test_definition("add", self.testdoc["tests"]["add"][0])
        expected = "def test_add_ef0858aaa92f5454(self):"
        self.assertEqual(result, expected)

    def test_author_test_result(self):
        result = self.author.author_test_result(self.testdoc["metadata"]["alias"],
                                                "add",
                                                self.testdoc["tests"]["add"][0]["args"])
        expected = "result = self.maths.add(2, 3)"
        self.assertEqual(result, expected)

    def test_author_test_assertion(self):
        result = self.author.author_test_assertion(self.testdoc["tests"]["add"][0]["assertion"])
        expected = "self.assertEqual(result, 5)"
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
        