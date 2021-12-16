# <img src="https://i.etsystatic.com/21347555/r/il/46f2ba/2750468715/il_fullxfull.2750468715_e06r.jpg" width="48" /> Testy Arthur 

A tool for easy authoring of Python3 unit tests

---

## Quick Start
Consider an example class:
```py
class Parser:

    def first_word(self, text: str) -> str:
        return text.split(" ")[0]

    def is_question(self, text: str) -> bool:
        return text.endswith("?")

    def contains_substring(self, text: str, substring: str) -> bool:
        return substring in text
```

The following are examples of JSON test declarations using simple, homogenous data structures.

\- 1 -

```JSON
{
    "first_word": {
        "equal": {
            ["the other day", "the"],
            ["two is too few", "two"],
            ["how now brown cow?", "how"]
        }
    }
}
```

```PY
def test_first_word_ABCDEF0123456789(self):
    expected = "the"
    result = self.parser.first_word("the other day")
    self.assertEqual(result, expected)

def test_first_word_BCDEF0123456789A(self):
    expected = "two"
    result = self.parser.first_word("two is too few")
    self.assertEqual(result, expected)
    
def test_first_word_CDEF0123456789AB(self):
    expected = "how"
    result = self.parser.first_word("how now brown cow?")
    self.assertEqual(result, expected)
    
```

\- 2 -

```JSON
{
    "is_question": {
        "true": [
            "This one?",
            "At what time?"
        ],
        "false": [
            "No, the other one!",
            "Around noon."
        ]
    }
}
```

```PY
def test_is_question_ABCDEF0123456789(self):
    result = self.parser.is_question("This one?")
    self.assertTrue(result)

def test_is_question_ABCDEF0123456789(self):
    result = self.parser.is_question("At what time?")
    self.assertTrue(result)

def test_is_question_ABCDEF0123456789(self):
    result = self.parser.is_question("No, the other one!")
    self.assertFalse(result)

def test_is_question_ABCDEF0123456789(self):
    result = self.parser.is_question("Around noon.")
    self.assertFalse(result)

```

Pal is capable of interpreting nested, heterogenous data structures.

```JSON
{
    "How now, brown cow?": [
        ["first_word", "equal", "How"],
        ["is_question", "true"],
        {
            "contains_substring": {
                "true": [
                    "How no",
                    "brown"
                ],
                "false": [
                    "English",
                    "Spanish"
                ]
        }   }
    ]
}
```

Pal is highly flexible. The `contains_substring` dictionary in the previous example could alternatively be written as follows:

```JSON
"contains_substring": [
    ["How no", "assertTrue"],
    ["true", "brown"],
    {"false": ["English", "Spanish"]}
]
```

### Assumptions/Rules

* Tests elements are as follows:
  * The method to test
  * A unittest.TestCase assertion
  * Zero or more arguments to pass to the method being tested
  * The result (return value) of the method to test, to be passed to the TestCase assertion
  * Zero or more arguments to pass to the TestCase assertion in addition to the result

* Each test definition has exactly one TestCase assertion.
* Arguments for the method being tested take precedence over additional arguments for the TestCase assertion.
* When providing arguments for `method(a, b)`, `a` takes precedence over `b`.

### Liberties

* So long as the values are provided in a logical structure, Pal should be able to handle it. Do what seems best.
* TestCase assertion declarations are case insensitive and the inclusion of the word "assert" is optional.




###

## Components

### Author

The Author class turns simplified JSON documents, referred to as "testdocs," into Python3 unittest files. Author provides the core functionality of Test Arthur but is fairly useless when used directly.

### Pal

Pal allows unit tests to be authored in JSON without enforcing a specific schema. Pal 

Pal is designed to be flexible, but it also naive. "Tricking" Pal is a trivial task.  

## Author TestDict Notes

### Document Format

```
{
    "metadata": {},
    "tests": []
}
```

### Metadata Format

```
"metadata": {
    "outpath": "",
    "target":["_className_", "_moduleName_"],
    "alias": "_instanceName_",
    "setup": Bool,
    "teardown": Bool
}
```

### Testdict List Format

```
{
    "method": "",
    "args": ["", ... ],
    "assertion": ["", ... ]
}
```

### Lines

#### Authored vs Written

Authored lines are actually a two-member array in the form `[int, str]`. The integer represents the relative indent level of the lines. Immediately before writing the line to the output file, this integer is multiplied by four and the line is padded with the resultant number of spaces.

### Test method fingerprinting

<<<<<<< HEAD
To ensure the Author writes unique method definitions in the Test Case, each `test_methodName()` is appended with a hexademical fingerprint to `test_methodName_FINGERPRINT()`. The generate the fingerprint value, the MD5 hash digest of the test dictionary `{"method": "", "args":[], "assertion": []}` is first computed. The fingerprint is the result of taking the XOR of the first sixteen digits of the hash digest with the second sixteen digits. This reduces the length of the test method fingerprint with a smaller increase in collision frequency than simple truncation would result in.

### Test Arguments

Values in `testdict["args"]` are passed to the method being tested.
=======
To ensure the Author writes unique method definitions in the Test Case, each `test_methodName()` is appended with a hexademical fingerprint to `test_methodName_FINGERPRINT()`. The generate the fingerprint value, the MD5 hash digest of the test dictionary `"method": "", "args":[], "assertion": []}` is first computed. The fingerprint is the result of taking the XOR of the first sixteen digits of the hash digest with the second sixteen digits. This reduces the length of the test method fingerprint with a smaller increase in collision frequency than simple truncation would result in.

### Test Arguments

Values in `testdict["assertion"]` are passed to the test method definition.
>>>>>>> master

### Test Assertions

Each test dictionary under a method must have at least one assertion value. The value of `testdict["assertion"][0]` is expected to be a `unittest.TestCase.assert` method. No additional values are necessary in `testdict["assertion"]` for assertions such as `assertIsTrue` while other assertions will require additional values in the `testdict["assertion"]` list.

#### Examples

`"assertion": ["False"]` becomes:

```py
self.assertIsFalse(result)
```

`"assertion": ["Equal", expectedValue]` becomes:

```py
self.assertIsEqual(result, expectedValue)
```

## Q&A
