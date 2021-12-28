# stutility
A package for commonly used utility functions.

This is based on the steven_utils package, providing pretty much the same set of functions. I want to take this chance to practise PEP8 recommended coding styles and organizing the export functions better via `__init__.py`.

## Excel Module
The excel module works with both xls and xlsx types of Excel workbooks, by providing two sets of functions. Under the cover it uses openpyxl to handle xlsx files and xlrd for xls files.

## Unit Test
See "test_stutility.py".