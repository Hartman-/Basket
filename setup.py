from setuptools import setup
import py2exe

setup(name='basket',
      version='0.1.0',
      description='Fruit Basket Pipeline',
      url='https://github.com/Hartman-/Basket',
      author='Hartman-',
      author_email='imh29@drexel.edu',
      license='MIT',
      packages=['basket', 'basket.gui', 'basket.utils'],
      zip_safe=False,
      options={
            'py2exe': {
                'includes': ['basket'],
                'dll_excludes': ['MSVCP90.dll']
            }
      },
      windows=['basket/BasketLauncher.py'])
