"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='circuitpython-ncd-pr33-15',

    use_scm_version=True,
    setup_requires=['setuptools_scm'],

    description='Driver for the ncd.io PR33-15 4-20ma receiver',
    long_description=long_description,
    long_description_content_type='text/x-rst',

    # The project's main homepage.
    url='https://github.com/schlafsack/CircuitPython_NCD_PR33_15',

    # Author details
    author='Tom Greasley',
    author_email='tom@greasley.com.com',

    install_requires=[
        'adafruit-circuitpython-busdevice',
    ],

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Topic :: System :: Hardware',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    # What does your project relate to?
    keywords='adafruit circuitpython micropython device ncd_pr33_15 NCD ncd.io PR33-15 MCP3428 4-20ma',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=['ncd_pr33_15'],
)
