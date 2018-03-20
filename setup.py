#!/usr/bin/env python
from distutils.core import setup
import sys
import os

version = '1.1.0'

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md').read()

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

setup(
    name='africastalking',
    version=version,
    packages=['africastalking'],
    description='Official Africa\'s Talking Python SDK',
    long_description=long_description,
    data_files=[('', ['README.md'])],
    license='MIT',
    author='Africa\'s Talking',
    install_requires=[
        'requests>=v2.18.4',
        'schema>=0.6.7'
    ],
    python_requires=">=2.7.10",
    author_email='info@africastalking.com',
    url='https://github.com/AfricasTalkingLtd/africastalking-python',
    download_url='https://codeload.github.com/AfricasTalkingLtd/africastalking-python/tar.gz/' + version,
    keywords='ussd voice sms mpesa card bank b2b b2c sender_id payments airtime africastalking',
    classifiers=[],
)
