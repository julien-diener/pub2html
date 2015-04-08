import os
from setuptools import setup, find_packages


def read(fname):
    """ Utility function to read the README file (used for the long_description) """
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="pub2html",
    version="0.1",
    author="Julien Diener",
    description=("Search publication DB and generate html content ", "using templates."),
    long_description=read('README.md'),
    license="BSD",
    keywords="publication html generator template",
    # url = "http://packages.python.org/....",

    package_dir = {'': 'src'}, # See packages below
    packages = find_packages("src", exclude="test"),

    requires=['jinja2']
)