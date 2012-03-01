r'''
Specification of target sources to use in Observation Beams.
'''

from momxml.angles import Angle

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
