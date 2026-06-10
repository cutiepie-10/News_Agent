from src.categoriser import categorise

def test_keyword_match_macro():
    result = categorise('The RBI has changed...')
    assert 'macro' in result

def test_keyword_match_ipo():
    result =categorise('Initial public offering of this company')
    assert 'ipo' in result
def test_no_match():
    result= categorise('There is not category.')
    assert 'other' in result

def test_multiple_category():
    result = categorise('IPO was listed. Now it shows a net loss')
    assert 'ipo' in result
    assert 'results' in result

def test_deduplicate():
    result = categorise('The quarterly result of ... . It has performed good and there is a net profit ')
    assert  'results' in result

