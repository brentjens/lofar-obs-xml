Synopsis
--------

The genvalobs program is a Python script that generates an XML file
containing MoM specifications for a set of system validation
observations for LOFAR. One can specify a target source (Cyg A, Vir A,
3C 196, Cas A), and a planned start date in UTC. The script will then
generate an XML file with observations for all desired observing
modes, using the specified target source and a given duration per
observation and interval between observations.


Prerequisites
-------------

Python 2.6 or newer


Installation
------------

user@localhost:~/genvalobs/ $ sudo python setup.py install


Brightest 3C sources
--------------------

|-------+-------------+-------------+-------+---------+-------+-------+-----+-----------------|
|   3CR | RA B1950    | DEC B1950   |  Vmag |       z |  S178 | alpha |   b | Comments        |
|-------+-------------+-------------+-------+---------+-------+-------+-----+-----------------|
|  84.0 | 03 16 29.55 | 41 19 51.9  | 11.85 |   0.017 |  61.3 |  0.78 | -13 | N1275,PERA,CL G |
| 273.0 | 12 26 33.35 | 02 19 42.0  | 12.80 | * 0.158 |  62.8 |  0.23 |  64 | 111SP         Q |
| 111.0 | 04 15 01.   | 37 54 20.   |  18.0 |   0.048 |  64.6 |  0.73 |  -9 | SE,R=173      G |
| 196.0 | 08 09 59.42 | 48 22 07.2  | 17.60 | * 0.871 |  68.2 |  0.79 |  33 | Q               |
| 295.0 | 14 09 33.44 | 52 26 13.6  | 20.20 |   0.461 |  83.5 |  0.63 |  61 | E,CL,SE(3727) G |
| 123.0 | 04 33 55.21 | 29 34 12.6  |  21.7 |   0.218 | 189.0 |  0.70 | -12 | 18,12ID,E,CL  G |
| 353.0 | 17 17 53.29 | -00 55 49.5 | 15.36 |   0.030 | 236.0 |  0.71 |  20 | 75ID,E        G |
| 348.0 | 16 48 39.98 | 05 04 35.0  | 16.90 |   0.154 | 351.0 |  1.00 |  29 | HER A,E,R174  G |
| 274.0 | 12 28 17.55 | 12 40 01.5  |  8.70 |   0.004 | 1050. |  0.76 |  75 | M87,30SP,CL   G |
| 405.0 | 19 57 44.43 | 40 35 45.2  | 16.22 |   0.056 | 8700. |  0.74 |   6 | 108SP,CYGA,SE G |
|-------+-------------+-------------+-------+---------+-------+-------+-----+-----------------|


Usage
-----

usage: genvalobs [options] "source name"

The source name must be enclosed in single or double quotes if it
contains spaces. The following sources are supported:

- "Cas A"  / cas: LST 21:00--03:00
- "3C 123" / 123: LST 01:30--07:30
- "3C 196" / 196: LST 05:00--11:00
- "Vir A"  / vir: LST 09:30--15:30
- "Her A"  / her: LST 14:00--20:00
- "Cyg A"  / cyg: LST 16:00--24:00

Options:
-o / --output    Specify output directory. Default is the current
                 directory.

-d / --duration  Duration of individual observations in
                 seconds. Default is 300.

-i / --interval  Interval between observations in seconds. Default
                 is 90.
