#!/usr/bin/env python

from distutils.core import setup

# http://wiki.python.org/moin/Distutils/Cookbook/AutoPackageDiscovery
import os

def is_package(path):
    return (
        os.path.isdir(path) and
        os.path.isfile(os.path.join(path, '__init__.py'))
        )

def find_packages(path, base="" ):
    """ Find all packages in path """
    packages = {}
    for item in os.listdir(path):
        dir = os.path.join(path, item)
        if is_package( dir ):
            if base:
                module_name = "%(base)s.%(item)s" % vars()
            else:
                module_name = item
            packages[module_name] = dir
            packages.update(find_packages(dir, module_name))
    return packages


setup(name='django-adlibre',
      version='0.1.1',
      description='Miscellaneous Django apps and helpers',
      long_description=open('README.md').read(),
      author='Adlibre Pty Ltd',
      author_email='code@adlibre.com.au',
      url='https://github.com/adlibre/django-adlibre',
      packages=find_packages('.'),
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Framework :: Django',
      ],
      install_requires=["xhtml2pdf",],
     )
