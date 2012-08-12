from lib.markdown2 import markdown

def md_to_html(text):
    if text:
        html_text = markdown(text, extras=['fenced-code-blocks',
                                           'code_friendly',
                                           'footnotes',
                                           'smarty-pants'])
        return html_text
    else:
        return ""
