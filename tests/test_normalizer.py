import pytest
from src.data_commands.normalizer import normalize_str

def test_normalize_str():
    text = " Ademco - hills,  Inc.  CO"
    expected = "ademco hills"
    result = normalize_str(text)
    assert result == expected