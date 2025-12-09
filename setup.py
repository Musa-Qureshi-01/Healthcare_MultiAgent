
from setuptools import setup, find_packages

setup(
    name='ey_provider_agent',
    version='1.0.0',
    packages=find_packages(include=['agents', 'pipeline', 'utils', 'tools']),
)
