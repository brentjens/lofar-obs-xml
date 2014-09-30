README
======

Synopsis
--------

The genvalobs program is a Python script that generates an XML file
containing MoM specifications for a set of system validation
observations for LOFAR. One can specify a target source (Cyg A, Vir A,
3C 196, Cas A), and a planned start date in UTC. The script will then
generate an XML file with observations for all desired observing
modes, using the specified target source and a given duration per
observation and interval between observations.

The Genvalobs is based on the momxml library (included in this
package), which can be used to write your own python scripts to
generate XML files that can be imported to LOFAR's MoM system.

Extensive documentation can be found in the doc/ directory. The
generated HTML documentation is found in ``doc/_build/html/``


Prerequisites
-------------

Python 2.6 or newer and pyephem (http://rhodesmill.org/pyephem/).

Installation
------------

user@localhost:~/genvalobs/ $ sudo python2 setup.py install



Usage
-----

usage: genvalobs [-h] [-o FILENAME] [-m CORRELATOR_MODE] [-d SECONDS]
                 [-g SECONDS] [-s STATION_SET] [-i STATION_NAMES]
                 [-e STATION_NAMES] [--min-alt DEGREES] [--max-alt DEGREES]
                 [-c CLOCK_MHZ] [-w SECONDS] [-t DATE_STRING] [-p MOM_NAME]
                 [-k STATIONS_TO_KEEP] [-f FILE_NAME] [-v]
                 [source]

The (optional) source name must be enclosed in single or double
quotes if it contains spaces. The following sources are recommended:

- "3C 48"  /  48: LST 22:30--04:30
- "3C 147" / 147: LST 02:30--08:30
- "3C 196" / 196: LST 05:00--11:00
- "3C 295" / 295: LST 11:00--17:00
- "Cyg A"  / cyg: LST 16:00--24:00

If no source is specified, the program chooses the source that is
closest to the meridian at the central LST of the observing
sequence. The program has separate calibrator lists for LBA
and HBA observations and pulsars.

Although genvalobs has its own default sequence of observations, it is
possible to read a custom set from an ASCII file with a fairly simple
format. The specification consists of newline-separated observations
where each observation is specified in a white-space separated line
with format:

    <ANTENNA_SET> <BAND> <SUBBANDS> <CLOCK> <BIT_MODE> <DATA_PRODUCTS>

    - ANTENNA_SET: one of LBA_INNER, LBA_OUTER, HBA_ZERO, HBA_ONE,
                    HBA_DUAL, HBA_JOINED, HBA_ZERO_INNER,
                    HBA_ONE_INNER, HBA_DUAL_INNER

    - FREQUENCY_BAND: LBA_LOW, LBA_HIGH, HBA_LOW, HBA_MID, HBA_HIGH

    - SUBBAND_LIST: comma-separated list of sub band ranges. Note: NO
                    SPACES ALLOWED! Examples:
                      - 12..499
                      - 12..22,112..122,212..222
    - CLOCK_MHZ: either 200 or 160

    - BIT_MODE: either 4, 8, or 16

    - DATA_PRODUCTS: white-space separated list of products. Allowed:
                     - XC (cross-correlation)
                     - FE (fly's eye)
                     - CS (coherent stokes)
                     - IS (incoherent stokes)
                     - TR (TAB rings)

    Empty lines are ignored, comments start with # end run until the
    end of the line.

    Example file:

        # Antennaset    Band      Subbands   Clock  Bits   Products
        LBA_OUTER       LBA_LOW   12..499    200     8     XC
        HBA_DUAL        HBA_LOW   12..499    200     8     XC
        LBA_INNER       LBA_HIGH  156..399   200    16     FE
        HBA_DUAL        HBA_LOW   77..320    200    16     IS
        HBA_DUAL        HBA_LOW   77..320    200    16     CS
        HBA_DUAL_INNER  HBA_MID   66..309    160    16     XC IS

Note that the custom sequence is subject to the same filtering by
options -m, -c, etc. as the default observing sequence. The last entry
is using the 160 MHz clock. It will only be used in the observation
sequence if the 160 MHz is selected using the -c / --clock option.

positional arguments:
  source                Force a source to be used for all observations,
                        bypassing genvalobs' own heuristics.

optional arguments:
  -h, --help            show this help message and exit
  -o FILENAME, --output FILENAME
                        Name of the output file [lofar-
                        validation-20140701-101048.xml].
  -m CORRELATOR_MODE, --mode CORRELATOR_MODE
                        Correlator modes to test. Choose one of XC
                        (crosscorrelation), FE (Fly's eye), IS (incoherent
                        stokes), or CS (coherent stokes). One can specify more
                        than one mode. If this argument is not spedified, all
                        modes will be tested [XC,FE,CS,IS,TR].
  -d SECONDS, --duration SECONDS
                        Duration of individual observations in seconds [120].
  -g SECONDS, --gap SECONDS
                        Gap between observations in seconds [60].
  -s STATION_SET, --stations STATION_SET
                        One of superterp, core, remote, nl, eu, all, or none.
                        EU stations that conflict with certain HBA1 core
                        fields are excluded from the HBA_ONE, HBA_ONE_INNER,
                        HBA_DUAL, and HBA_DUAL_INNER observations. They are
                        taken along in all other observations [nl].
  -i STATION_NAMES, --include STATION_NAMES
                        Comma separated list of station names to include. No
                        spaces allowed in the list. Example: -i
                        cs013,de601,rs106
  -e STATION_NAMES, --exclude STATION_NAMES
                        Comma separated list of station names to exclude. No
                        spaces allowed in the list. Example: -e
                        cs013,de601,rs106
  --min-alt DEGREES     Minimum elevation for target sources [40.00].
  --max-alt DEGREES     Maximum elevation for target sources [70.00].
  -c CLOCK_MHZ, --clocks CLOCK_MHZ
                        Allowed clock frequencies. Choose 160 or 200. Option
                        can be provided multiple times if more than one clock
                        frequency is required.
  -w SECONDS, --wait SECONDS
                        Number of seconds until the first observation [540].
  -t DATE_STRING, --start-date DATE_STRING
                        Specify an exact date and time to start the first
                        observation. Format: "yyyy/mm/dd hh:mm:ss.s"
  -p MOM_NAME, --project MOM_NAME
                        Name of the observations' MoM project
                        ['2014LOFAROBS'].
  -k STATIONS_TO_KEEP, --keep STATIONS_TO_KEEP
                        In case of HBA_DUAL or HBA_ONE network conflicts, keep
                        either "core", "eu" stations, or "all" of them.
                        ['core'].
  -f FILE_NAME, --from-file FILE_NAME
                        Read a custom observing sequence from FILE_NAME.
  -v, --version         Print version number and exit.



Brightest 3C sources
--------------------

Just for reference, sorted by brightness:

+-------+-------------+-------------+-------+---------+------------+-------+-----+-----------------+
|   3CR | RA B1950    | DEC B1950   |  Vmag |       z |  S 178 MHz | alpha |   b | Comments        |
+=======+=============+=============+=======+=========+============+=======+=====+=================+
| 405   | 19 57 44.43 | 40 35 45.2  | 16.22 |   0.056 | 8700.      |  0.74 |   6 | 108SP,CYGA,SE G |
+-------+-------------+-------------+-------+---------+------------+-------+-----+-----------------+
| 274   | 12 28 17.55 | 12 40 01.5  |  8.70 |   0.004 | 1050.      |  0.76 |  75 | M87,30SP,CL   G |
+-------+-------------+-------------+-------+---------+------------+-------+-----+-----------------+
| 348   | 16 48 39.98 | 05 04 35.0  | 16.90 |   0.154 | 351.0      |  1.00 |  29 | HER A,E,R174  G |
+-------+-------------+-------------+-------+---------+------------+-------+-----+-----------------+
| 353   | 17 17 53.29 | -00 55 49.5 | 15.36 |   0.030 | 236.0      |  0.71 |  20 | 75ID,E        G |
+-------+-------------+-------------+-------+---------+------------+-------+-----+-----------------+
| 123   | 04 33 55.21 | 29 34 12.6  |  21.7 |   0.218 | 189.0      |  0.70 | -12 | 18,12ID,E,CL  G |
+-------+-------------+-------------+-------+---------+------------+-------+-----+-----------------+
| 295   | 14 09 33.44 | 52 26 13.6  | 20.20 |   0.461 |  83.5      |  0.63 |  61 | E,CL,SE(3727) G |
+-------+-------------+-------------+-------+---------+------------+-------+-----+-----------------+
| 196   | 08 09 59.42 | 48 22 07.2  | 17.60 |   0.871 |  68.2      |  0.79 |  33 | Q               |
+-------+-------------+-------------+-------+---------+------------+-------+-----+-----------------+
| 111   | 04 15 01.   | 37 54 20.   |  18.0 |   0.048 |  64.6      |  0.73 |  -9 | SE,R=173      G |
+-------+-------------+-------------+-------+---------+------------+-------+-----+-----------------+
| 273   | 12 26 33.35 | 02 19 42.0  | 12.80 |   0.158 |  62.8      |  0.23 |  64 | 111SP         Q |
+-------+-------------+-------------+-------+---------+------------+-------+-----+-----------------+
|  84   | 03 16 29.55 | 41 19 51.9  | 11.85 |   0.017 |  61.3      |  0.78 | -13 | N1275,PERA,CL G |
+-------+-------------+-------------+-------+---------+------------+-------+-----+-----------------+
