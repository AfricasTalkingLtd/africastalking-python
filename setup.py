from distutils.core import setup
import sys, os

from codecs import open

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

packages = [
    'africastalking'
]

setup(
    name='africastalking',
    packages=['africastalking'],  # this must be the same as the name above
    version='1.1',
    description='An Official Python library for communicating with the AfricasTalking REST API',
    author='Ian Juma',
    author_email='ijuma@africastalking.com',
    url='https://github.com/AfricasTalkingLtd/africastalking-python',
    download_url='https://codeload.github.com/AfricasTalkingLtd/africastalking-python/tar.gz/1.1',
    keywords=['ussd', 'voice', 'sms', 'mpesa', 'payments', 'africastalking'],
    classifiers=[],
)
