
import os.path

from setuptools import setup, find_packages

__version__ = 'devel'

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()

requires = [
    'PyGithub',
]

dev_extras = [
    'emulambda',
]

setup(
    name='skill-for-github',
    version=__version__,
    description='Alexa skill for GitHub',
    long_description=README,
    classifiers=[
        "Programming Language :: Python",
    ],
    author='David Kavanagh',
    author_email='dkavanagh@gmail.com',
    url='',
    keywords='',
    packages=find_packages(),
    test_suite='tests'
)
