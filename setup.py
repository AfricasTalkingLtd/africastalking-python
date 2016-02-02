from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

packages = [
    'africastalking'
]

with open('README.md', 'r', 'utf-8') as f:
    readme = f.read()

setup(
  name='africastalking',
  packages=['africastalking'], # this must be the same as the name above
  version='1.0',
  description='An Official Python library for communicating with the AfricasTalking REST API',
  long_description=readme + '\n\n',
  author='Ian Juma',
  author_email='ijuma@africastalking.com',
  url='https://github.com/AfricasTalkingLtd/africastalking-python',
  download_url='https://codeload.github.com/AfricasTalkingLtd/africastalking-python/tar.gz/1.0',
  keywords=['ussd', 'voice', 'sms' 'mpesa', 'payments', 'africastalking'],
  classifiers=[],
)