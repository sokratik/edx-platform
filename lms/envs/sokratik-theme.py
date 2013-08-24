__author__ = 'vulcan'
from sokratik import *
from theming_utils.template_customizer import enable_theme
THEME_NAME = "stanford"
THEME_SASS_DIRECTORY = ENV_ROOT / "themes/stanford/static/sass/"
print(THEME_SASS_DIRECTORY)
PIPELINE = False
MKTG_URL_LINK_MAP = {
    'ABOUT': 'about_edx',
    'TOS': 'tos',
    'FAQ': 'help_edx',
}

MITX_FEATURES['USE_DJANGO_PIPELINE'] = False
PIPELINE = False
DEBUG = True
TEMPLATE_DEBUG = True
enable_theme(THEME_NAME, locals())
