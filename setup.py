#!/usr/bin/env python

from setuptools import setup, find_packages

def readme():
    with open('README.adoc') as f:
        return f.read()

setup(
    name='vcdvcd',
    version='2.1.0',
    description='Python Verilog value change dump (VCD) parser library + the nifty vcdcat VCD command line viewer',
    long_description=readme(),
    long_description_content_type='text/plain',
    url='https://github.com/cirosantilli/vcdvcd',
    author='Ciro Santilli',
    author_email='ciro.santilli.contact@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    scripts=['vcdcat'],
)
