import pytest
import json
import os
from unittest.mock import mock_open
from src.utils import load_transactions

def test_load_valid_file(tmp_path):
    data = [{"id": 1}, {"id": 2}]
    file = tmp_path / "test.json"
    file.write_text(json.dumps(data))
    assert load_transactions(file) == data

def test_load_empty_file(tmp_path):
    file = tmp_path / "empty.json"
    file.write_text('')
    assert load_transactions(file) == []

def test_load_invalid_file(tmp_path):
    file = tmp_path / "invalid.json"
    file.write_text('{invalid}')
    assert load_transactions(file) == []

def test_file_not_exists():
    assert load_transactions("nonexistent.json") == []