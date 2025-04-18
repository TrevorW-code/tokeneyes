CSS = """
<style>
.token-hover {
    transition: background-color 0.3s ease;
}
.token-hover:hover {
    filter: brightness(1.5);
}
</style>
"""

def make_token_span(color,hover,content):
    return f'<span class="token-hover" style="background-color: {color};" title="{hover}">{content}</span>'

def make_info_line(title: str,info: str):
    return f"{title}: <b>{info}</b>"