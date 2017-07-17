from os.path import exists
from setuptools import setup

setup(name='ptime',
      version='0.0.1',
      description='IPython magic for parallel profiling',
      url='http://github.com/jcrist/ptime/',
      maintainer='Jim Crist',
      maintainer_email='jiminy.crist@gmail.com',
      license='BSD',
      packages=['ptime'],
      long_description=(open('README.rst').read() if exists('README.rst')
                        else ''),
      zip_safe=False)
