# Testy Arthur <img src="https://i.etsystatic.com/21347555/r/il/46f2ba/2750468715/il_fullxfull.2750468715_e06r.jpg" width="64" />

A tool for easy authoring of Python3 unit tests

---

## Quick Start

## Components

### Author

The Author class turns simplified JSON documents, referred to as "testdocs," into Python3 unittest files. Author provides the core functionality of Test Arthur.

## Testdoc Schema

### Document Format

```
{
    "metadata": {target, alias, ..},
    "tests": [{td1}, {td2}, ...]
}
```

### Metadata Format

```
"metadata": {
    "target":["_className_", "_moduleName_"],
    "alias": "_instanceName_",
    "setup": Bool,
    "teardown": Bool
}
```

### Testdict List Format

```
{
  "_methodName_": [
      {
          "args": ["", ... ],
          "assertion": ["", ... ]
      },
      ...
  ]
}
```

## Notes

### Lines

#### Authored vs Written

Authored lines are actually a two-member array in the form `[int, str]`. The integer represents the relative indent level of the lines. Immediately before writing the line to the output file, this integer is multiplied by four and the line is padded with the resultant number of spaces.

### Test method fingerprinting

To ensure the Author writes unique method definitions in the Test Case, each `test_methodName()` is appended with a hexademical fingerprint to `test_methodName_FINGERPRINT()`. The generate the fingerprint value, the MD5 hash digest of the dictionary `methodName: {"args":[], "assertion": []}` is first computed. The fingerprint is the result of taking the XOR of the first sixteen digits of the hash digest with the second sixteen digits. This reduces the length of the test method fingerprint with a smaller increase in collision frequency than simple truncation would result in.

### Test Arguments

Values in `methodName["assertion"]` are passed to the test method definition.

### Test Assertions

Each test dictionary under a method must have at least one assertion value. The value of `methodName["assertion"][0]` is expected to be a `unittest.TestCase.assert` method. No additional values are necessary in `methodName["assertion"]` for assertions such as `assertIsTrue` while other assertions will require additional values in the `methodName["assertion"]` list.

#### Examples

`"methodName": {"assertion": ["False"]}` becomes:

```py
self.assertIsFalse(result)
```

`"methodName": {"assertion": ["Equal", expectedValue]}` becomes:

```py
self.assertIsEqual(result, expectedValue)
```

## Q&A
