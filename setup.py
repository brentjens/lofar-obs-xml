#!/usr/bin/env python

from distutils.core import setup
from momxml import __version__

setup(name='genvalobs',
      version      = __version__,
      description  = 'Generate XML file with LOFAR system validation observations',
      author       = 'Michiel Brentjens',
      author_email = 'brentjens@astron.nl',
      url          = '',
      packages     = ['momxml'],
      requires     = ['ephem'],
      scripts      = ['genvalobs'],
     )
