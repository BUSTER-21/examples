project = 'Falkonry APIs'
copyright = '2012-22, Falkonry, Inc'
author = 'Falkonry'

release = '1.0'
version = '1.0.0'

master_doc = 'index'

# -- General configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinxcontrib.httpdomain',
    'sphinx_tabs.tabs',
    'sphinx-prompt',
    'notfound.extension',
    'sphinx_search.extension',
    'sphinxemoji.sphinxemoji',
    'sphinx_tabs.tabs',
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

templates_path = ['_templates']

html_theme = 'sphinx_rtd_theme'
html_logo = 'img/favicon.ico'
html_theme_options = {
    'logo_only': True,
    'display_version': False,
    'prev_next_buttons_location': None,
}

epub_show_urls = 'footnote'

html_show_sourcelink = False

language = 'en'

hoverxref_auto_ref = True

notfound_context = {
    'title': 'Page Not Found',
    'body': '''
<h1>Page Not Found</h1>
<p>Sorry, we couldn't find that page.</p>
<p>Try using the search box or go to the homepage.</p>
''',
}