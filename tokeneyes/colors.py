from transformers import AutoTokenizer
GOLDEN_RATIO_CONJUGATE = 0.618033988749895
A = 1664525
C = 1013904223
M = 2**32

def number_to_color(number: int, dark_mode=False, config = dict):
    pseudorandom = (A * number + C) % M
    hue = ((pseudorandom * GOLDEN_RATIO_CONJUGATE) % 1) * 360
    
    if dark_mode:
        # Dark mode adjustments
        saturation = 50 + (pseudorandom % 20)  # Slightly lower saturation
        lightness = 20 + (pseudorandom % 20)  # Much lower lightness (20-40%)
    else:
        saturation = 60 + (pseudorandom % 21)  # Saturation between 60-80%
        lightness = 70 + (pseudorandom % 21)  # Lightness between 70-90%

    return f"hsl({hue}, {saturation}%, {lightness}%)"

def get_token_colors(text: str, tokenizer: AutoTokenizer, color_func = number_to_color):
    tokens = tokenizer.tokenize(text)
    unique_tokens = list(set(tokens))
    token_colors = {token: color_func(index, dark_mode=True) for index, token in enumerate(unique_tokens)}
    return token_colors

def get_index_colors(index_tuples, dark_mode, color_func = number_to_color):
    token_colors = {tup: color_func(index, dark_mode) for index, tup in enumerate(index_tuples)}
    return token_colors