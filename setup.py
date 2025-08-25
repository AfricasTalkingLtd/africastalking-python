#!/usr/bin/env python
from setuptools import setup
import sys
import os

version = "2.0"

long_description = open("README.md").read()

if sys.argv[-1] == "publish":
    os.system("python setup.py sdist upload")
    sys.exit()

setup(
    name="africastalking",
    version=version,
    packages=["africastalking"],
    description="Official Africa's Talking Python SDK",
    data_files=[("", ["README.md"])],
    license="MIT",
    author="Africa's Talking",
    install_requires=["requests>=v2.30.0", "schema>=0.6.7", "responses>=0.25.8"],
    python_requires=">=3.8",
    author_email="info@africastalking.com",
    url="https://github.com/AfricasTalkingLtd/africastalking-python",
    download_url="https://codeload.github.com/AfricasTalkingLtd/africastalking-python/tar.gz/"
    + version,
    keywords="ussd voice sms mpesa sender_id airtime africastalking mobile_data sim_swap whatsapp",
    classifiers=[],
    long_description=long_description,
    long_description_content_type="text/markdown",
)
