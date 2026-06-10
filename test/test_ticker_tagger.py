from src.ticker_tagger import extract_ticker_tags

def test_keyword_match_nifty():
    result = extract_ticker_tags("Nifty at support 22200")
    assert "NIFTY" in result

def test_keyword_match_banknifty():
    result = extract_ticker_tags("BankNifty looking weak today")
    assert "BANKNIFTY" in result

def test_no_partial_match():
    # "itc" should not match inside "critical"
    result = extract_ticker_tags("This is critical support")
    assert "ITC" not in result

def test_itc_standalone():
    result = extract_ticker_tags("ITC breakout confirmed")
    assert "ITC" in result

def test_multiple_tickers():
    result = extract_ticker_tags("Nifty and Reliance both look good")
    assert "NIFTY" in result
    assert "RELIANCE" in result

def test_deduplication():
    # cashtag + keyword map both match NIFTY — should appear once
    result = extract_ticker_tags("Nifty at 22000. Nifty may open...")
    assert result.count("NIFTY") == 1

def test_empty_input():
    result = extract_ticker_tags("")
    assert result == []
