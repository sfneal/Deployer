from setuptools import setup, find_packages

setup(
    name='PyPi',
    version='0.2.0',
    packages=find_packages(),
    install_requires=[
        'twine>=1.12.1',
    ],
    url='https://github.com/mrstephenneal/PyPiDistributor',
    license='',
    author='Stephen Neal',
    author_email='stephen@stephenneal.net',
    description='Utility for distributing packages to PyPi'
)
