from distutils.core import setup
import sys
import os

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

setup(
    name='africastalking',
    version='2.0.0',
    packages=['africastalking'],
    description='Africa\'s Talking Python SDK',
    author='Africa\'s Talking',
    install_requires=[
        'requests>=v2.18.4',
        'schema>=0.6.7'
    ],
    author_email='info@africastalking.com',
    url='https://github.com/AfricasTalkingLtd/africastalking-python',
    download_url='https://codeload.github.com/AfricasTalkingLtd/africastalking-python/tar.gz/2.0.0',
    keywords=['ussd', 'voice', 'sms', 'mpesa', 'payments', 'airtime', 'africastalking'],
    classifiers=[],
)
