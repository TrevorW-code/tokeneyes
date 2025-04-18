import pytest
from transformers import AutoTokenizer
from tokeneyes.core import get_model_name_from_tokenizer

def make_name_obj_tuple(name: str):
    return (AutoTokenizer.from_pretrained(name), name)

def test_get_name_from_tokenizer():
    test, output = make_name_obj_tuple('answerdotai/ModernBERT-base')
    assert output == get_model_name_from_tokenizer(test)
