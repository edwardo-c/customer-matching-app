import pytest
from src.customer_resolution.normalizer import normalize_str

def test_normalize_str():
    text = " Ademco,  Inc.  CO"
    expected = "ademco"
    result = normalize_str(text)
    assert result == expected