import pytest
from src.refresh.cleaner import extract_zip_code, clean_string


def test_string_cleaner():
    
    tests = {
        '06502': '06502', 
        '6502.0': '06502', 
        '06502-1111': '065021111', 
        '065021111': '065021111',
        '06502  1111': '065021111',
        '06502 1111': '065021111'
    }
    for test, expected in tests.items():
        cleaned = clean_string(test)
        assert cleaned == expected

def test_extract_zip_code():
    ca_tests = ['M5A1A1', 'M5A 1A1', 'M5A-1A1']
    us_tests = ['06502', '6502.0', '06502-1111','065021111', '06502 1111']
    for ca in ca_tests:
        assert extract_zip_code(clean_string(ca)) == 'M5A1A1'
    for us in us_tests:
        assert extract_zip_code(clean_string(us)) == '06502'
    assert extract_zip_code(clean_string('not a zip')) == ''