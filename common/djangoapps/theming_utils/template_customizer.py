__author__ = 'himangshu'
"""
This file contains utilities to customize templates.moves the template customization logic from lms to common
"""


def enable_theme(theme_name, container):
    """
    Enable the settings for a custom theme, whose files should be stored
    in ENV_ROOT/themes/THEME_NAME (e.g., edx_all/themes/stanford).

    The THEME_NAME setting should be configured separately since it can't
    be set here (this function closes too early). An idiom for doing this
    is:

    THEME_NAME = "stanford"
    enable_theme(THEME_NAME)
    """
    container["THEME_NAME"] = theme_name
    container['MITX_FEATURES']['USE_CUSTOM_THEME'] = True
    # Calculate the location of the theme's files
    theme_root = container['ENV_ROOT'] / "themes" / theme_name
    # Include the theme's templates in the template search paths
    container['TEMPLATE_DIRS'].append(theme_root / 'templates')
    container['MAKO_TEMPLATES']['main'].append(theme_root / 'templates')
    # Namespace the theme's static files to 'themes/<theme_name>' to
    # avoid collisions with default edX static files
    container['STATICFILES_DIRS'].append((u'themes/%s' % theme_name,
                                       theme_root / 'static'))
    container['FAVICON_PATH'] = 'themes/%s/images/favicon.ico' % theme_name





