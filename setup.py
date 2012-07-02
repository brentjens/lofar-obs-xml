#!/usr/bin/env python

from distutils.core import setup

setup(name='genvalobs',
      version      = '0.9',
      description  = 'Generate XML file with LOFAR system validation observations',
      author       = 'Michiel Brentjens',
      author_email = 'brentjens@astron.nl',
      url          = '',
      packages     = ['momxml'],
      requires     = ['ephem'],
      scripts      = ['genvalobs'],
     )
