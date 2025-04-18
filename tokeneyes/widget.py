from IPython.display import HTML, display
from transformers import AutoTokenizer
from tokeneyes.colors import get_index_colors
from tokeneyes.web import CSS, make_token_span, make_info_line

# def raw_token_visualization(text: str, tokz: AutoTokenizer):
#     tokens = tokz.tokenize(text)
#     token_colors = get_token_colors(text, tokz)
#     tokens_vis = make_colored_tokens_html(tokens, token_colors)
#     return tokens_vis, tokens

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

def parsed_text_visualization(text: str, tokz: AutoTokenizer, dark_mode: bool):
    """
    Visualizes how input text is parsed, rather than displaying the encoded actual string
    """
    encoding = tokz(text, return_offsets_mapping=True)
    tokens = tokz.tokenize(text)
    index_tuples, ids = encoding['offset_mapping'], encoding['input_ids']
    index_colors = get_index_colors(index_tuples, dark_mode)
    
    spans = ""
    for idx, tup in enumerate(index_tuples):
        s,e = tup
        if e - s > 0:
            spans += make_token_span(
                color = index_colors[tup],
                hover = ids[idx],
                content = text[s:e]
            )

    return spans, tokens

def show_tokens(text: str, model_str: str, dark_mode: bool = False):
    tokz = AutoTokenizer.from_pretrained(model_str)
    model = "<p>" + make_info_line("model", model_str) + "</p>"
    tokens_vis, tokens = parsed_text_visualization(text,tokz, dark_mode=dark_mode)
    # tokens_vis, tokens = raw_token_visualization(text, tokz)
    num_tokens, num_chars = len(tokens), len(text)
    token_info = make_info_line("tokens", num_tokens)
    char_info = make_info_line("chars", num_chars)
    counts = "<p>" + token_info + ", " + char_info + "</p>"
    display(HTML(CSS + model + tokens_vis + counts))