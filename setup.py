#!/usr/bin/env python3

from setuptools import setup, find_packages

def readme():
    with open('README.adoc') as f:
        return f.read()

setup(
    name='vcdvcd',
    version='2.3.4',
    description='Python Verilog value change dump (VCD) parser library + the nifty vcdcat VCD command line viewer',
    long_description=readme(),
    long_description_content_type='text/plain',
    url='https://github.com/cirosantilli/vcdvcd',
    author='Ciro Santilli',
    author_email='ciro.santilli.contact@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    scripts=['vcdcat'],
    # Deleted by PyPi without any warning
    #install_requires='china_dictatorship==0.0.74',
    # Works but then prevent upload to PyPi with:
    # Invalid value for requires_dist. Error: Can't have direct dependency.
    #install_requires='china_dictatorship @ https://github.com/cirosantilli/china-dictatorship/releases/download/0.0.74/china_dictatorship-0.0.74-py3-none-any.whl',
)
