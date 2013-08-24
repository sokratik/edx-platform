__author__ = 'vulcan'

from unittest import TestCase
from theming_utils.template_customizer import enable_theme
from path import path


class TestThemeingCustomization(TestCase):
    MITX_FEATURES = {}
    PROJECT_ROOT = path(__file__).abspath().dirname().dirname()
    REPO_ROOT = PROJECT_ROOT.dirname()
    ENV_ROOT = REPO_ROOT.dirname()
    MAKO_TEMPLATES = {}
    MAKO_TEMPLATES['main'] = []
    TEMPLATE_DIRS = []
    STATICFILES_DIRS = []

    def test_theme(self):
        theme_name = "sokratik"
        enable_theme(theme_name, self)
        self.assertTrue(self.MITX_FEATURES['USE_CUSTOM_THEME'], "true is not true")
        self.assertIn(theme_name, str(self.MAKO_TEMPLATES['main'][0].relpath()), "theme name not affected")
        self.assertEqual(self.THEME_NAME, theme_name, "theme names do not match")
        self.assertEqual(self.FAVICON_PATH, 'themes/%s/images/favicon.ico' % theme_name, "favicon does not match")


if __name__ == '__main__':
    unittest.main()
