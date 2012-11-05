r'''
Specification of target sources to use in Observation Beams.
'''

from momxml.angles import Angle
import urllib

class NoSimbadCoordinatesError(RuntimeError):
    r'''
    Raised if the Simbad response does not contain J2000 coordinates.
    '''

class SourceSpecificationError (ValueError):
    r'''
    Raised in case of badly specified TargetSource.
    '''


class TargetSource:
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

    **Raises**

    SourceSpecificationError
        In case of badly specified TargetSource.

    **Examples**

    >>> TargetSource('Cyg A', ra_angle = Angle(shms = ('+', 19, 59, 28.3565)), dec_angle = Angle(sdms = ('+', 40, 44, 2.099)) )
    TargetSource(name      = 'Cyg A',
                 ra_angle  = Angle(shms = ('+', 19, 59, 28.3565)),
                 dec_angle = Angle(sdms = ('+', 40, 44, 2.099)))


    '''
    
    def __init__(self, name = '', ra_angle = None, dec_angle = None):
        self.name      = name
        self.ra_angle  = ra_angle
        self.dec_angle = dec_angle
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

        >>> TargetSource('Cyg A', ra_angle = Angle(shms = ('+', 19, 59, 28.3565)), dec_angle = Angle(sdms = ('+', 40, 44, 2.099)) )
        TargetSource(name      = 'Cyg A',
                     ra_angle  = Angle(shms = ('+', 19, 59, 28.3565)),
                     dec_angle = Angle(sdms = ('+', 40, 44, 2.099)))
        >>> TargetSource(u'Cyg A', ra_angle = Angle(shms = ('+', 19, 59, 28.3565)), dec_angle = Angle(sdms = ('+', 40, 44, 2.099)) )
        Traceback (most recent call last):
        ...
        SourceSpecificationError: Source name may not be a unicode string.
        >>> TargetSource('Cyg A', ra_angle = 3.0, dec_angle = Angle(sdms = ('+', 40, 44, 2.099)) )
        Traceback (most recent call last):
        ...
        SourceSpecificationError: ra_angle must be a momxml.Angle, not 3.0

        >>> TargetSource('Cyg A', ra_angle = Angle(shms = ('+', 19, 59, 28.3565)), dec_angle = -2)
        Traceback (most recent call last):
        ...
        SourceSpecificationError: dec_angle must be a momxml.Angle, not -2

        '''
        if type(self.name) == type(u''):
            raise SourceSpecificationError(
                'Source name may not be a unicode string.')
        if type(self.name) != type(''):
            raise SourceSpecificationError(
                'Source name must be a string. You specified %s' % 
                (str(self.name),))
        if self.ra_angle.__class__.__name__ != 'Angle':
            raise SourceSpecificationError(
                'ra_angle must be a momxml.Angle, not %r' % self.ra_angle)

        if self.dec_angle.__class__.__name__ != 'Angle':
            raise SourceSpecificationError(
                'dec_angle must be a momxml.Angle, not %r' % self.dec_angle)

        return self



    def ra_deg(self):
        r'''
        Return right ascension in degrees

        **Returns**

        A float.

        **Examples**

        >>> TargetSource('Cyg A', ra_angle = Angle(deg = 299.868152), dec_angle = Angle(deg = 40.733916) ).ra_deg()
        299.868152

        '''
        return self.ra_angle.as_deg()


    def dec_deg(self):
        r'''
        Return declination in degrees

        **Returns**

        A float.

        **Examples**

        >>> TargetSource('Cyg A', ra_angle = Angle(deg = 299.868152), dec_angle = Angle(deg = 40.733916) ).dec_deg()
        40.733916

        '''
        return self.dec_angle.as_deg()

    
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

    >>> simbad_response = """C.D.S.  -  SIMBAD4 rel 1.201  -  2012.11.02CET07:49:05

NGC 891
-------

Object NGC 891  ---  GiG  ---  OID=@27433   (@@140880,0)  ---  coobox=2606

Coordinates(ICRS,ep=J2000,eq=2000): 02 22 32.907  +42 20 53.95 (IR  ) B [~ ~ ~] 2006AJ....131.1163S

Identifiers (22):
   NGC 891                         IRAS F02194+4207                IRAS 02193+4207               
   ISOSS J02225+4221               JCMTSE J022233.0+422050         JCMTSF J022233.0+422050       
   LEDA 9031                       2MASS J02223247+4220494         2MASX J02223290+4220539       
   MCG+07-05-046                   PSCz Q02193+4207                TC 454                        
   UGC 1831                        UZC J022233.4+422102            ZOAG G140.38-17.42            
   Z 538-52                        Z 0219.4+4207                   [BTW2003] J0222+4219          
   [CHM2007] LDC 160 J022232.90+4220539  [M98c] 021924.3+420710          [SLK2004] 299                 
   [VDD93] 15                                                                                    
================================================================================
"""
    >>> target_source_from_simbad_response('NGC 891', simbad_response)
    TargetSource(name      = 'NGC 891',
                 ra_angle  = Angle(shms = ('+', 2, 22, 32.907)),
                 dec_angle = Angle(sdms = ('+', 42, 20, 53.95)))

    >>> simbad_trifid = """C.D.S.  -  SIMBAD4 rel 1.201  -  2012.11.02CET13:53:30

Trifid Nebula
-------------

Object M 20  ---  HII  ---  OID=@2517890   (@@115109,0)  ---  coobox=18517

Coordinates(ICRS,ep=J2000,eq=2000): 18 02 42  -22 58.3 (Opt ) E [~ ~ ~] 2009MNRAS.399.2146W

Identifiers (20):
   M 20                            C 1759-230                      Cl Collinder 360              
   CSI-23-17593 1                  CTB 45                          GRS 007.00 -00.30             
   LBN 006.99-00.17                LBN 27                          LMH 12                        
   MM 11                           MSH 17-2-16                     NAME TRIFID NEBULA            
   NGC 6514                        NRL 10                          OCISM 2                       
   OCl 23.0                        [DGW65] 99                      [KPR2004b] 425                
   [SC95] M 208                    [SC95] M 215                                                  
================================================================================
"""
    >>> target_source_from_simbad_response('Trifid Nebula', simbad_trifid)
    '''
    coordinate_lines = [line for line in simbad_response.split('\n')
                         if 'Coordinates(ICRS,ep=J2000,eq=2000)' in line]
    if len(coordinate_lines) > 0:
        words    = coordinate_lines[0].split()
        ra_angle = Angle(shms =
                         ('+', int(words[1]), int(words[2]), float(words[3])))
        dec_angle = Angle(sdms =
                          (words[4][0], int(words[4][1:]), int(words[5]), float(words[6])))
        return TargetSource(name      = source_name,
                            ra_angle  = ra_angle,
                            dec_angle = dec_angle)
    else:
        raise NoSimbadCoordinatesError('No J2000 coordinates in %s' %
                                       simbad_response)



def simbad(source_name, debug = False):
    r'''
    '''
    query = '&'.join(['http://simbad.u-strasbg.fr/simbad/sim-id?output.format=ASCII',
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
    
    result = urllib.urlopen(query % urllib.quote(source_name),
                            proxies = {}).read()
    if debug:
        print(result)
        sys.stdout.flush()
    else:
        return target_source_from_simbad_response(source_name, result)

