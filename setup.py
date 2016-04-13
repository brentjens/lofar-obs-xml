#!/usr/bin/env python

from distutils.core import setup
from momxml import __version__

setup(name='lofar-obs-xml',
      version      = __version__,
      description  = 'Generate XML file with LOFAR system validation observations',
      author       = 'Michiel Brentjens',
      author_email = 'brentjens@astron.nl',
      url          = 'http://www.lofar.org/operations/doku.php?id=operator:system_validation_observations',
      packages     = ['momxml', 'lofarobsxml'],
      requires     = ['ephem'],
      scripts      = ['genvalobs'],
     )
