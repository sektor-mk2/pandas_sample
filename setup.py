from setuptools import setup, find_packages

setup(
    name='pandas_sample',
    version='0.1.0',
    packages=find_packages(include=['pandas_sample']),
    install_requires=[
            'pandas==2.0.1',
        ]
)
