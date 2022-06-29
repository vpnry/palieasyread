import os
from setuptools import setup, find_packages

# User-friendly description from README.md
cwd = os.path.dirname(os.path.abspath(__file__))
try:
    with open(os.path.join(cwd, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
except Exception:
    long_description = ''

setup(
    # Name of the package
    name='palieasyread',
    # Packages to include into the distribution
    packages=find_packages('.'),
    # Start with a small number and increase it with
    # every change you make https://semver.org
    version='0.0.2',
    # Short description of your library
    description='Split Roman pali words into smaller syllables',
    # Long description of your library
    long_description=long_description,
    long_description_content_type='text/markdown',
    # Your name
    author='Cuong DANG',
    # Your email

    author_email='https://github.com/vpnry/palieasyread/issues/new',
    # Either the link to your github or to your website
    url='https://github.com/vpnry/palieasyread',
    # Link from which the project can be downloaded
    download_url='',
    # package_data={
    #         'palieasyread': [
    #             'templates/*.*',
    #             'static/js/*.*',
    #             'static/css/*.*']},
    # List of keywords
    keywords=['pali syllables', 'split', 'roman pali'],
    # List of packages to install with this one
    # python_requires='>=3.6.0',
    install_requires=[],
    # https://pypi.org/classifiers/
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers'
    ]
)
