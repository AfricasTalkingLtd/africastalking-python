#!/usr/bin/env python
from distutils.core import setup
import sys
import os

version = '1.0.0'

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

setup(
    name='africastalking',
    version=version,
    packages=['africastalking'],
    description='Africa\'s Talking Python SDK',
    author='Africa\'s Talking',
    install_requires=[
        'requests>=v2.18.4',
        'schema>=0.6.7'
    ],
    author_email='info@africastalking.com',
    url='https://github.com/AfricasTalkingLtd/africastalking-python',
    download_url='https://codeload.github.com/AfricasTalkingLtd/africastalking-python/tar.gz/' + version,
    keywords=['ussd', 'voice', 'sms', 'mpesa', 'payments', 'airtime', 'africastalking'],
    classifiers=[],
)
