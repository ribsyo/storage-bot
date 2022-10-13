from models import Quote, File
from classes import FileManager, QuoteManager
import unittest
import requests



def test_QuoteManager_add_quote():
    test_command = Quote(
        quote = "test"
    )
    quoteManager = QuoteManager([])
    quoteManager.add_quote_suggestion(test_command)
    assert test_command.quote == quoteManager.quoteSuggestions[0]

def test_QuoteManager_give_quote():
    test_path = "test.txt"
    test_command = Quote(
        quote = "test"
    )
    with open(test_path, 'w') as f:
        f.write(test_command.quote)
        f.close()
    with open(test_path, 'r') as f:
        quoteManager = QuoteManager(f.read().splitlines())
        f.close()
    assert quoteManager.give_quote() == test_command


def test_FileManager_set_file():
    fileManager = FileManager("test.txt")
    testPath = "pathTest.txt"
    fileManager.set_file(testPath)
    assert testPath == getattr(fileManager, 'path')
    assert open(testPath, "a+").read().splitlines() == getattr(fileManager, 'fileContent')

def test_FileManager_get_all_lines():
    fileManager = FileManager("test.txt")
    with open("test.txt", "a+") as f:
        content = f.read().splitlines()
    result = fileManager.get_all_lines()
    x = 0
    for line in content:
        assert result[x] == content[x]
        x += 1

def test_FileManager_get_line():
    content = "hello"
    with open("test.txt", "w") as f:
        f.write(content)
        f.close()
    fileManager = FileManager("test.txt")
    assert content == fileManager.get_line(len(getattr(fileManager, 'fileContent')) - 1)
