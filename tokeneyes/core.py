from transformers import AutoTokenizer

def get_model_name_from_tokenizer(tokenizer: AutoTokenizer):
    if hasattr(tokenizer, "name_or_path"):
        return tokenizer.name_or_path
    elif hasattr(tokenizer, "init_kwargs") and "name_or_path" in tokenizer.init_kwargs:
        return tokenizer.init_kwargs["name_or_path"]
    else:
        return tokenizer.__class__.__name__