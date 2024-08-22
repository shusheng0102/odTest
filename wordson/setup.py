# from distutils.core import setup
from setuptools import setup
import os

from wordson.version import VERSION as __version__

setup(
    name="wordson",
    packages=["wordson"],
    package_data={
        '': [
            'wordson/config.json',
            'wordson/img',
            'wordson/words',
            'wordson/i18n',
            'README.md',
            'LICENSE',
        ],
    },
    version=__version__,
    install_requires=[
        'pygame',
        'requests',
        'bs4',
        'html5lib',
    ],
    entry_points={
        'console_scripts': [
            'wordson = wordson.__main__:main'
        ]
    },
    author="TylerTemp",
    author_email="tylertempdev@gmail.com",
    # url="http://docpie.comes.today/",
    # download_url="https://github.com/TylerTemp/docpie/tarball/%s/" % __version__,
    license='MIT',
    # description=("An easy and Pythonic way to create "
    #              "your POSIX command line interface"),
    # keywords='option arguments parsing optparse argparse getopt docopt',
    long_description=open(
        os.path.join(os.path.dirname(__file__), 'README.md')).read(),
    long_description_content_type='text/markdown',
    platforms='any',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Topic :: Education',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
)
