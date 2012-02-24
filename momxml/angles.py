r'''
Uniform handling of angles.
'''

from math import floor, pi

def signum(number):
    r'''
    Returns the sign of ``number``.

    **Parameters**

    number : number
        The number for which to calculate the sign.

    **Returns**

    Integer +1 if `number`` >= 0.0, -1 if ``number`` < 0.0

    **Examples**

    >>> signum(3)
    1
    >>> signum(0.0)
    1
    >>> signum(0)
    1
    >>> signum(-1e-30)
    -1
    >>> signum(-0)
    1
    '''
    if number < 0.0:
        return -1
    else:
        return +1


def sign_char(number):
    r'''
    Returns the sign of ``number``.

    **Parameters**

    number : number
        The number for which to calculate the sign.

    **Returns**

    String '+' if number >= 0.0, '-' if number < 0.0

    **Examples**

    >>> sign_char(3)
    '+'
    >>> sign_char(0.0)
    '+'
    >>> sign_char(0)
    '+'
    >>> sign_char(-1e-30)
    '-'
    >>> sign_char(-0)
    '+'
    '''
    return ['-', None, '+'][1+signum(number)]


def int_from_sign_char(char):
    r'''
    Returns -1 if ``char`` == '-', +1 if ``char`` == '+'

    **Parameters**

    char: a one-character string
        Either '+' or '-'.

    **Returns**

    The integer -1 or +1, depending on the value of ``char``.

    **Raises**

    ValueError
        If ``char`` is something other than '+' or '-'.

    **Examples**

    >>> int_from_sign_char('+')
    1
    >>> int_from_sign_char('-')
    -1
    >>> int_from_sign_char('f')
    Traceback (most recent call last):
    ...
    ValueError: char must be either '+' or '-', not 'f'
    
    '''
    if char == '+':
        return +1
    elif char == '-':
        return -1
    else:
        raise ValueError('char must be either \'+\' or \'-\', not %r' % char)
    



class Angle(object):
    r'''
    A simple container for angles. It can be created from various
    units of angles. Specify exactly one of ``shms``, ``sdms``,
    ``rad``, or ``deg``.

    **Parameters**

    shms : None or tuple
        An angle in hours, minutes, and seconds, e.g. ('+', 13, 59,
        12.4). The sign is required.
    
    sdms : None or tuple
        An angle in degrees, minutes, and seconds, e.g. ('-', 359, 59,
        12.4). The sign is required.

    rad : None or float
        An angle in radians.

    deg : None or float
        An angle in degrees.

    **Raises**

    ValueError
        In case of problems with the provided arguments.

    **Examples**

    Direct values:

    >>> Angle(deg = 360.0)
    Angle(rad = 6.28318530718)
    >>> Angle(rad = pi)
    Angle(rad = 3.14159265359)

    Hours:

    >>> Angle(shms = ('+', 3, 15, 30.2))
    Angle(rad = 0.853044216323)
    >>> Angle(shms = ('-', 3, 15, 30.2))
    Angle(rad = -0.853044216323)

    Degrees:

    >>> Angle(sdms = ('+', 3, 15, 30.2))
    Angle(rad = 0.0568696144215)
    >>> Angle(sdms = ('-', 3, 15, 30.2))
    Angle(rad = -0.0568696144215)
    
    '''
    def __init__(self, shms = None, sdms = None, rad = None, deg = None):
        none_count = [shms, sdms, rad, deg].count(None)
        if none_count != 3:
            raise ValueError('Specify exactly none of shms, sdms, rad, or deg.')
        self.rad = 0.0
        
        if shms is not None:
            self.set_shms(*shms)
        if sdms is not None:
            self.set_sdms(*sdms)
        if rad is not None:
            self.set_rad(rad)
        if deg is not None:
            self.set_deg(deg)

    def __repr__(self):
        return 'Angle(rad = %s)' % str(self.rad)
        
    def set_shms(self, sign, hours, minutes, seconds):
        sgn      = int_from_sign_char(sign) 
        self.rad = sgn*pi*(hours + minutes/60.0 + seconds/3600.0)/12.0
        return self.rad

    
    def set_sdms(self, sign, degrees, minutes, seconds):
        sgn      = int_from_sign_char(sign) 
        self.rad = sgn*pi*(degrees + minutes/60.0 + seconds/3600.0)/180.0
        return self.rad

    
    def set_deg(self, deg):
        self.rad = deg*pi/180.0
        return self.rad

    
    def set_rad(self, rad):
        self.rad = rad
        return self.rad


    def as_rad(self):
        return self.rad

    
    def as_deg(self):
        return self.rad*180.0/pi

    
    def as_shms(self):
        sgn      = sign_char(self.rad)
        abs_rad  = abs(self.rad)
        in_hours = abs_rad * 12/pi
        hours    = int(floor(in_hours))
        in_minutes = (in_hours-hours)*60.0
        minutes    = int(floor(in_minutes))
        in_seconds = (in_minutes - minutes)*60.0
        return (sgn, hours, minutes, in_seconds)

    def as_sdms(self):
        sgn      = sign_char(self.rad)
        abs_rad  = abs(self.rad)
        in_degrees = abs_rad * 180/pi
        degrees    = int(floor(in_degrees))
        in_minutes = (in_degrees - degrees)*60.0
        minutes    = int(floor(in_minutes))
        in_seconds = (in_minutes - minutes)*60.0
        return (sgn, degrees, minutes, in_seconds)


    def __float__(self):
        return self.rad

    def __add__(self, angle):
        return Angle(rad = self.as_rad() + float(angle))

    def __sub__(self, angle):
        return Angle(rad = self.as_rad() - float(angle))
    
    def __mul__(self, factor):
        return Angle(rad = self.as_rad() * float(factor))
    
    def __div__(self, divisor):
        return Angle(rad = self.as_rad() / float(divisor))
