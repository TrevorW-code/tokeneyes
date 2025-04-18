from IPython.display import HTML, display
from transformers import AutoTokenizer
from tokeneyes.colors import get_index_colors
from tokeneyes.core import get_model_name_from_tokenizer
from tokeneyes.web import CSS, make_token_span, make_info_line
from typing import Callable, Any
import functools as ft

def make_colored_tokens_html(tokens, token_colors):
    colored_text = ""
    for token in tokens:
        color = token_colors[token]
        span = make_token_span(
            color = color,
            hover = token,
            content = token
        )
        colored_text += span
    return colored_text

@ft.singledispatch
def input_vis(inp: Any, tokz: AutoTokenizer, dark_mode: bool, color_by: Callable):
    raise ValueError(f'No Visualization for Input Type: {type(inp)}')

@input_vis.register
def _(inp: str, tokz: AutoTokenizer, dark_mode: bool, color_by: Callable):
    """
    Visualizes how input text is parsed, rather than displaying the encoded actual string
    """
    
    encoding = tokz(inp, return_offsets_mapping=True)
    tokens = tokz.tokenize(inp)
    index_tuples, ids = encoding['offset_mapping'], encoding['input_ids']
    index_colors = get_index_colors(index_tuples, dark_mode)
    id2token = {id: tokz.convert_ids_to_tokens(id) for id in encoding['input_ids']}
    
    # write spans
    spans = ""
    for idx, tup in enumerate(index_tuples):
        start,end = tup
        if end - start > 0:
            current_id = ids[idx]
            spans += make_token_span(
                color = index_colors[tup],
                hover = f'id: {current_id}\nraw: {id2token[current_id]}',
                content = inp[start:end]
            )
    return spans, tokens

def show_tokens(text: str, tokenizer: AutoTokenizer | str, dark_mode: bool = False, color_by = get_index_colors):
    # get tokenizer
    if isinstance(tokenizer, str):
        model = tokenizer
        tokz = AutoTokenizer.from_pretrained(tokenizer)
    else:
        model = get_model_name_from_tokenizer(tokenizer)
        tokz = tokenizer
    
    # visualize tokens
    tokens_vis, tokens = input_vis(text, tokz, dark_mode=dark_mode, color_by = color_by)
    num_tokens, num_chars = len(tokens), len(text)
    
    # make info
    model = "<p>" + make_info_line("model", model) + "</p>"
    token_info = make_info_line("tokens", num_tokens)
    char_info = make_info_line("chars", num_chars)
    counts = "<p>" + token_info + ", " + char_info + "</p>"
    display(HTML(CSS + model + tokens_vis + counts))