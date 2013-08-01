from setuptools import setup, find_packages

setup(
        name="edX docs",
        version="0.1",
        install_requires=['distribute']
        packages=['docs', 'docs.shared']
        )
