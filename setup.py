from setuptools import setup
from scratch import __version__

setup(name='scratchpy',
      version=__version__,
      description='A Python interface to Scratch',
      keywords=['Scratch'],
      url='http://github.com/pilliq/scratchpy',
      author='Phillip Quiza',
      author_email='pquiza@gmail.com',
      license='MIT',
      packages=['scratch'],
      test_suite='tests.all_tests',
      zip_safe=False)
