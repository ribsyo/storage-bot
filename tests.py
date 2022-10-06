from models import Quote
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





test_QuoteManager_add_quote()
test_QuoteManager_give_quote()
