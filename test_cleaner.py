from pytask_pro.cleaner import TextCleaner
from pytask_pro.models import Record

def test_clean_text():
    assert TextCleaner.clean_text("  Hello\n\tWorld  ") == "Hello World"

def test_clean_records():
    result = TextCleaner().clean_records([Record("  A\nBook  ", "$10", " Three ", " In stock ")])
    assert result[0].title == "A Book"
    assert result[0].rating == "Three"
