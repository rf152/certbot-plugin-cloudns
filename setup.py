import sys

from setuptools import setup
from setuptools import find_packages


version = '0.0.1.alpha0'

setup(
    name='certbot-plugin-cloudns',
    version=version,
    description="ClouDNS plugin for Certbot",
    author="R Franks",
    author_email='git@rf152.co.uk',
    license='Apache License 2.0',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Plugins',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Security',
        'Topic :: System :: Installation/Setup',
        'Topic :: System :: Networking',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
    ],
    packages=['certbot_cloudns'],
    install_requires=['acme', 'certbot>=0.15', 'cloudnsapi'],
    entry_points={
        'certbot.plugins': [
            'dns-cloudns = certbot_cloudns.plugin:Authenticator',
        ],
    },
)