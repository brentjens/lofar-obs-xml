.. Genvalobs / momxml documentation master file, created by
   sphinx-quickstart2 on Tue Oct 22 13:35:17 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Genvalobs / momxml's documentation!
==============================================

The genvalobs program is a Python script that generates an XML file
containing MoM specifications for a set of system validation
observations for LOFAR. One can specify a target source (Cyg A, Vir A,
3C 196, Cas A), and a planned start date in UTC. The script will then
generate an XML file with observations for all desired observing
modes, using the specified target source and a given duration per
observation and interval between observations.

Genvalobs is based on the ``momxml`` library (included in this
package), which can be used to write your own python scripts to
generate XML files that can be imported to LOFAR's MoM system.

Extensive documentation can be found in the doc/ directory. The
generated HTML documentation is found in ``doc/_build/html/``

Contents
========

.. toctree::
   :maxdepth: 2

   readme
   momxml

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

