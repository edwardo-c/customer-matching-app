import pytest
from src.customer_matching.normalizer import normalize_str

def test_normalize_str():
    text = " Ademco hills,  Inc.  CO hills"
    expected = "ademco hills"
    result = normalize_str(text)
    assert result == expected