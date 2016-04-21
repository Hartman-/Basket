from setuptools import setup, find_packages
from codecs import open
import imp, os

version = imp.load_source(
    'version', os.path.join('basket', 'version.py'))

here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# get the dependencies and installs
with open(os.path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    all_reqs = f.read().split('\n')

install_requires = [x.strip() for x in all_reqs if 'git+' not in x]
dependency_links = [x.strip().replace('git+', '') for x in all_reqs if 'git+' not in x]

setup(
    name='Basket',
    version=version.VERSION_STRING,
    description='The base setup for BasketApp',
    long_description=long_description,
    url='https://github.com/Hartman-/basket',
    download_url='https://github.com/Hartman-/basket/tarball/' + version.VERSION_STRING,
    license='BSD',
    classifiers=[
      'Development Status :: 3 - Alpha',
      'Intended Audience :: Developers',
      'Programming Language :: Python :: 2.7.11',
    ],
    keywords='',
    packages=find_packages(exclude=['docs', 'tests*']),
    include_package_data=True,
    author='Ian Hartman',
    install_requires=install_requires,
    dependency_links=dependency_links,
    author_email='imh29@drexel.edu'
)
