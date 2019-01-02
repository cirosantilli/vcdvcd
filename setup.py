#!/usr/bin/env python

from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='vcdvcd',
    version='1.0.2',
    description='Python Verilog value change dump (VCD) parser library',
    long_description=readme(),
    url='https://github.com/cirosantilli/vcdvcd',
    author='Ciro Santilli',
    author_email='ciro.santilli.contact@gmail.com',
    packages=find_packages(),
    scripts=['vcdvcd/vcdcat'],
)
