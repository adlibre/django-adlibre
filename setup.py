#!/usr/bin/env python

from distutils.core import setup

setup(name='django-adlibre',
      version='1.0',
      description='Miscellaneous Django apps and helpers',
      author='Adlibre Pty Ltd',
      author_email='code@adlibre.com.au',
      url='https://github.com/adlibre/django-adlibre',
      install_requires = ["xhtml2pdf",],
     )
