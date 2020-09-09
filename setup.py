
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='CDash API Tool',
    version='0.1.0',
    description='A CDash API tool that allows to programmatically manage stuff',
    long_description=readme,
    author='Adrian Castro',
    author_email='me@adct.it',
    url='https://github.com/BioDataAnalysis/cdash-tool',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
