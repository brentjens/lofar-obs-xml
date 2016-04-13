r'''
Specification of target sources to use in Observation Beams.
'''

from lofarobsxml.angles import Angle
import sys
import urllib
if sys.version_info[0] > 2:
    import urllib.request as request

class NoSimbadCoordinatesError(RuntimeError):
    r'''
    Raised if the Simbad response does not contain J2000 coordinates.
    '''

class SourceSpecificationError (ValueError):
    r'''
    Raised in case of badly specified TargetSource.
    '''


class TargetSource(object):
    r'''
    A target source to be used when specifying a Beam within an
    Observation.

    **Parameters**

    name : non-unicode string
        Contains the name of the source.

    ra_angle : None or an Angle
        J2000 right ascension.

    dec_angle : None or an Angle
        J2000 declination.

    reference_frame : string
        Reference frame for the longitudinal (ra/az/lon) and
        latitudinal (dec/el/lat) coordinates. Examples: 'J2000',
        'B1950', 'AZELGEO', 'AZEL', 'GALACTIC', 'JMEAN', JTRUE',
        etc... Basically anything supported by Casacore.
        Default: 'J2000'

    **Raises**

    SourceSpecificationError
        In case of badly specified TargetSource.

    **Examples**

    >>> TargetSource('Cyg A',
    ...              ra_angle  = Angle(shms = ('+', 19, 59, 28.3565)),
    ...              dec_angle = Angle(sdms = ('+', 40, 44, 2.099)) )
    TargetSource(name      = 'Cyg A',
                 ra_angle  = Angle(shms = ('+', 19, 59, 28.3565)),
                 dec_angle = Angle(sdms = ('+', 40, 44, 2.099)))


    '''

    def __init__(self, name = '', ra_angle = None, dec_angle = None,
                 reference_frame='J2000'):
        self.name      = name
        self.ra_angle  = ra_angle
        self.dec_angle = dec_angle
        self.reference_frame = reference_frame
        self.validate_and_normalize()


    def validate_and_normalize(self):
        r'''
        Validates type and contents of data members. This method is
        called by the constructor.

        **Returns**

        A reference to ``self``.

        **Raises**

        SourceSpecificationError
            In case of a badly specified target source.

        **Examples**

        >>> TargetSource('Cyg A',
        ...              ra_angle = Angle(shms = ('+', 19, 59, 28.3565)),
        ...              dec_angle = Angle(sdms = ('+', 40, 44, 2.099)) )
        TargetSource(name      = 'Cyg A',
                     ra_angle  = Angle(shms = ('+', 19, 59, 28.3565)),
                     dec_angle = Angle(sdms = ('+', 40, 44, 2.099)))

        # >>> TargetSource(u'Cyg A',
        # ...              ra_angle = Angle(shms = ('+', 19, 59, 28.3565)),
        # ...              dec_angle = Angle(sdms = ('+', 40, 44, 2.099)) )
        # Traceback (most recent call last):
        # ...
        # lofarobsxml.targetsource.SourceSpecificationError: Source name may not be a unicode string.
        >>> TargetSource('Cyg A',
        ...              ra_angle = 3.0,
        ...              dec_angle = Angle(sdms = ('+', 40, 44, 2.099)) )
        Traceback (most recent call last):
        ...
        lofarobsxml.targetsource.SourceSpecificationError: ra_angle must be a lofarobsxml.Angle, not 3.0

        >>> TargetSource('Cyg A',
        ...              ra_angle = Angle(shms = ('+', 19, 59, 28.3565)),
        ...              dec_angle = -2)
        Traceback (most recent call last):
        ...
        lofarobsxml.targetsource.SourceSpecificationError: dec_angle must be a lofarobsxml.Angle, not -2

        '''
        # Named tuple was introduced in Python 2.7
        # In python 2.7 use sys.version_info.major 
        if sys.version_info[0] == 2:
            if type(self.name) == type(u''):
                raise SourceSpecificationError(
                    'Source name may not be a unicode string.')
        if type(self.name) != type(''):
            raise SourceSpecificationError(
                'Source name must be a string. You specified %s' %
                (str(self.name),))
        if self.ra_angle.__class__.__name__ != 'Angle':
            raise SourceSpecificationError(
                'ra_angle must be a lofarobsxml.Angle, not %r' % self.ra_angle)

        if self.dec_angle.__class__.__name__ != 'Angle':
            raise SourceSpecificationError(
                'dec_angle must be a lofarobsxml.Angle, not %r' % self.dec_angle)

        return self



    def ra_deg(self):
        r'''
        Return right ascension in degrees

        **Returns**

        A float.

        **Examples**

        >>> TargetSource('Cyg A',
        ...              ra_angle = Angle(deg = 299.868152),
        ...              dec_angle = Angle(deg = 40.733916) ).ra_deg()
        299.868152

        '''
        return self.ra_angle.as_deg()


    def dec_deg(self):
        r'''
        Return declination in degrees

        **Returns**

        A float.

        **Examples**

        >>> TargetSource('Cyg A',
        ...              ra_angle = Angle(deg = 299.868152),
        ...              dec_angle = Angle(deg = 40.733916) ).dec_deg()
        40.733916

        '''
        return self.dec_angle.as_deg()


    def ra_dec_rad(self):
        r'''
        Returns coordinates as an (ra_rad, dec_rad) pair of floats.

        **Examples**

        >>> '(%.6f, %.6f)' % TargetSource('Cyg A',
        ...                               ra_angle = Angle(deg = 299.868152),
        ...                               dec_angle = Angle(deg = 40.733916) ).ra_dec_rad()
        '(5.233687, 0.710941)'
        '''
        return (self.ra_angle.as_rad(), self.dec_angle.as_rad())


    def __repr__(self):
        return ('''TargetSource(name      = %r,
             ra_angle  = Angle(shms = %r),
             dec_angle = Angle(sdms = %r))''' %
             (self.name,
              self.ra_angle.as_shms()[0:3]  +
              (float('%7.4f' % self.ra_angle.as_shms()[-1]),),
              self.dec_angle.as_sdms()[0:3] +
              (float('%7.4f' % self.dec_angle.as_sdms()[-1]),)))




def target_source_from_simbad_response(source_name, simbad_response):
    r'''

    **Examples**

    >>> simbad_response = open('examples/simbad-ngc891.txt').read()
    >>> target_source_from_simbad_response('NGC 891', simbad_response)
    TargetSource(name      = 'NGC 891',
                 ra_angle  = Angle(shms = ('+', 2, 22, 32.907)),
                 dec_angle = Angle(sdms = ('+', 42, 20, 53.95)))

    >>> simbad_trifid = open('examples/simbad-trifid.txt').read()
    >>> target_source_from_simbad_response('Trifid Nebula', simbad_trifid)
    TargetSource(name      = 'Trifid Nebula',
                 ra_angle  = Angle(shms = ('+', 18, 2, 42.0)),
                 dec_angle = Angle(sdms = ('-', 22, 58, 18.0)))

    >>> simbad_ncp = open('examples/simbad-ncp.txt').read()
    >>> target_source_from_simbad_response('NCP', simbad_ncp)
    TargetSource(name      = 'NCP',
                 ra_angle  = Angle(shms = ('+', 0, 0, 0.0)),
                 dec_angle = Angle(sdms = ('+', 90, 0, 0.0)))

    '''
    coordinate_lines = [line for line in simbad_response.split('\n')
                         if 'Coordinates(ICRS,ep=J2000,eq=2000)' in line]
    if len(coordinate_lines) > 0:
        words    = coordinate_lines[0].split()
        ra_hms   = [float(number) for number in words[1:4]]
        ra_angle = Angle(hms = ra_hms)

        if words[6][0] in '0123456789':
            dec_sdms = (words[4][0],
                        float(words[4][1:]), float(words[5]), float(words[6]))
        else:
            dec_sdms = (words[4][0],
                        float(words[4][1:]), float(words[5]), 0.0)
        dec_angle = Angle(sdms = dec_sdms)
        return TargetSource(name      = source_name,
                            ra_angle  = ra_angle,
                            dec_angle = dec_angle)
    else:
        raise NoSimbadCoordinatesError('No J2000 coordinates in %s' %
                                       simbad_response)



def simbad(source_name, debug = False):
    r'''
    Lookup ``source_name`` on simbad and return a TargetSource instance.

    **Examples**

    >>> simbad('3C 196')
    TargetSource(name      = '3C 196',
                 ra_angle  = Angle(shms = ('+', 8, 13, 36.0561)),
                 dec_angle = Angle(sdms = ('+', 48, 13, 2.636)))
    '''
    query = '&'.join([
        'http://simbad.u-strasbg.fr/simbad/sim-id?output.format=ASCII',
        'obj.coo1=on',
        'obj.coo2=off',
        'obj.coo3=off',
        'obj.coo4=off',
        'frame1=ICRS',
        'epoch1=J2000',
        'equi1=2000',
        'obj.pmsel=off',
        'obj.plxsel=off',
        'obj.rvsel=off',
        'obj.spsel=off',
        'obj.mtsel=off',
        'obj.sizesel=off',
        'obj.fluxsel=off',
        'obj.bibsel=off',
        'obj.messel=off',
        'obj.notesel=off',
        'Ident=%s'])

    if sys.version_info[0] == 2:
        result = urllib.urlopen(query % urllib.quote(source_name),
                                proxies = {}).read()
    else:
        result = request.urlopen(query % urllib.parse.quote(source_name)).read().decode('utf8')
    if debug:
        print(result)
        sys.stdout.flush()
    else:
        return target_source_from_simbad_response(source_name, result)

