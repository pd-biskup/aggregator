from setuptools import setup, find_packages


with open('README.md') as file:
    description = file.read()


setup(
    name='aggregator',
    version='0.0.1.dev1',
    author='Paweł Dzięga',
    description='Pluggable content aggregator.',
    long_description=description,
    long_description_content_type='text/markdown',
    url='https://github.com/pd-biskup/aggregator',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: Linux'
    ]
)
