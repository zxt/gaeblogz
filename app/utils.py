import re
import unicodedata
from lib.markdown2 import markdown

## {{{ http://code.activestate.com/recipes/577257/ (r2)
_slugify_strip_re = re.compile(r'[^\w\s-]')
_slugify_hyphenate_re = re.compile(r'[-\s]+')
def _slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    
    From Django's "django/template/defaultfilters.py".
    """
    import unicodedata
    if not isinstance(value, unicode):
        value = unicode(value)
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = unicode(_slugify_strip_re.sub('', value).strip().lower())
    return _slugify_hyphenate_re.sub('-', value)
## end of http://code.activestate.com/recipes/577257/ }}}

def unique_slugify(value, existing_slugs):
    slug = _slugify(value)
    original_slug = slug
    append_num = 2
    while slug in existing_slugs:
        slug = original_slug
        end = "%s%s" % ('-', append_num)
        slug = "%s%s" % (slug, end)
        append_num += 1
    return slug

def md_to_html(text):
    if text:
        html_text = markdown(text, extras=['fenced-code-blocks',
                                           'code_friendly',
                                           'footnotes',
                                           'smarty-pants'])
        return html_text
    else:
        return ""
