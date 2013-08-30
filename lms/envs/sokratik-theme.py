__author__ = 'vulcan'
from sokratik import *
from theming_utils.template_customizer import enable_theme
THEME_NAME = "stanford"
THEME_SASS_DIRECTORY = ENV_ROOT / "themes/stanford/static/sass/"
PIPELINE = False
MITX_FEATURES['USE_DJANGO_PIPELINE'] = False
DEBUG = True
TEMPLATE_DEBUG = True
enable_theme(THEME_NAME, locals())
