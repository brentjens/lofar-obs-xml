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

    rad : None or float
        An angle in radians.

    hms : None or tuple
        An angle in hours, minutes, and seconds,
        e.g. (13, 59, 12.4).

    shms : None or tuple
        A signed  angle in hours, minutes, and seconds, e.g. ('+', 13, 59,
        12.4). The sign is required.

    sdms : None or tuple
        An angle in degrees, minutes, and seconds, e.g. ('-', 359, 59,
        12.4). The sign is required.

    deg : None or float
        An angle in degrees.

    **Raises**

    ValueError
        In case of problems with the provided arguments.

    **Examples**

    Direct values:

    >>> Angle(deg = 360.0)
    Angle(rad = 6.283185307179586)
    >>> Angle(rad = pi)
    Angle(rad = 3.141592653589793)

    Hours:

    >>> Angle(hms = (3, 15, 30.2))
    Angle(rad = 0.8530442163226618)
    >>> Angle(shms = ('-', 3, 15, 30.2))
    Angle(rad = -0.8530442163226618)

    Degrees:

    >>> Angle(sdms = ('+', 3, 15, 30.2))
    Angle(rad = 0.05686961442151079)
    >>> Angle(sdms = ('-', 3, 15, 30.2))
    Angle(rad = -0.05686961442151079)


    Whoops:
    >>> Angle(rad = -0.0568696144215, deg = 12)
    Traceback (most recent call last):
    ...
    ValueError: Specify *one* of hms, shms, sdms, rad, or deg.

    '''
    def __init__(self, rad = None, hms = None, shms = None, sdms = None,
                 deg = None):
        none_count = [hms, shms, sdms, rad, deg].count(None)
        if none_count != 4:
            raise ValueError('Specify *one* of hms, shms, sdms, rad, or deg.')
        self.rad = 0.0

        if hms is not None:
            self.set_shms('+', *hms)
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
        r'''
        Explicitly set angle with sign, hours, minutes, and seconds.

        **Parameters**

        sign : string
            One of '+' or '-'

        hours : positive number
            Number of hours. Does not need to be restricted to the
            [0..24] range. May also be a floating point number.

        minutes : positive number
            Number of minutes. Does not need to be restricted to
            [0..60]. May also be floating point.

        seconds : positive number
            Number of seconds. Does not need to be restricted to
            [0..60]. May also be floating point.

        **Returns**

        A float containing the angle in radians.

        **Examples**

        >>> a = Angle(rad = 2.0)
        >>> rad = a.set_shms('-', 2, 30, 45.2)
        >>> str(a.as_rad())
        '-0.6577855062557962'
        '''
        sgn      = int_from_sign_char(sign)
        self.rad = sgn*pi*(hours + minutes/60.0 + seconds/3600.0)/12.0
        return self.rad


    def set_sdms(self, sign, degrees, minutes, seconds):
        r'''
        Explicitly set angle with sign, degrees, minutes, and seconds.

        **Parameters**

        sign : string
            One of '+' or '-'

        degrees : positive number
            Number of degrees. Does not need to be restricted to the
            [0..360] range. May also be a floating point number.

        minutes : positive number
            Number of minutes. Does not need to be restricted to
            [0..60]. May also be floating point.

        seconds : positive number
            Number of seconds. Does not need to be restricted to
            [0..60]. May also be floating point.

        **Returns**

        A float containing the angle in radians.

        **Examples**

        >>> a = Angle(rad = 2.0)
        >>> rad = a.set_sdms('-', 2, 30, 45.2)
        >>> str(a.as_rad())
        '-0.04385236708371975'

        '''
        sgn      = int_from_sign_char(sign)
        self.rad = sgn*pi*(degrees + minutes/60.0 + seconds/3600.0)/180.0
        return self.rad


    def set_deg(self, deg):
        r'''
        Set the angle in degrees.

        **Parameters**

        degrees : float
            The angle in degrees.

        **Returns**

        A float containing the angle in radians.

        **Examples**

        >>> a = Angle(rad = 2.0)
        >>> str(a.set_deg(180.0))
        '3.141592653589793'
        >>> str(a.set_deg(-90.0))
        '-1.5707963267948966'
        '''
        self.rad = deg*pi/180.0
        return self.rad


    def set_rad(self, rad):
        r'''
        Set the angle in radians.

        **Parameters**

        rad : float
            The angle in radians.

        **Returns**

        A float containing the angle in radians.

        **Examples**

        >>> a = Angle(rad = 2.0)
        >>> a.set_rad(3.0)
        3.0
        >>> a.set_rad(-1.2)
        -1.2
        '''
        self.rad = rad
        return self.rad


    def as_rad(self):
        r'''
        Get angle in radians.

        **Returns**

        A float containing the angle in radians.

        **Examples**

        >>> a = Angle (rad = 3.0)
        >>> a.as_rad()
        3.0
        '''
        return self.rad


    def as_deg(self):
        r'''
        Get angle in degrees.

        **Returns**

        A float containing the angle in degrees.

        **Examples**

        >>> a = Angle (rad = 3.0)
        >>> str(a.as_deg())
        '171.88733853924697'
        '''
        return self.rad*180.0/pi


    def as_hours(self):
        r'''
        Get angle in hours.

        **Returns**

        A float containing the angle in hours.

        **Examples**

        >>> a = Angle (rad = 3.0)
        >>> str(a.as_hours())
        '11.459155902616464'
        '''
        return self.rad*12.0/pi



    def as_shms(self):
        r'''
        Get the angle in hours, minutes, and seconds. It does not
        round off the hours and minutes based on the seconds. See examples.

        **Returns**

        A tuple containing (sign, hours, minutes, seconds)

        **Examples**

        >>> fmt = '%s%02dh %02dm %06.3fs'
        >>> fmt % Angle(shms = ('+', 3, 10, 59.99999)).as_shms()
        '+03h 10m 60.000s'
        >>> fmt % Angle(shms = ('+', 3, 11, 0.0)).as_shms()
        '+03h 10m 60.000s'
        >>> fmt % Angle(shms = ('-', 3, 11, 0.1)).as_shms()
        '-03h 11m 00.100s'

        '''
        sgn      = sign_char(self.rad)
        abs_rad  = abs(self.rad)
        in_hours = abs_rad * 12/pi
        hours    = int(floor(in_hours))
        in_minutes = (in_hours-hours)*60.0
        minutes    = int(floor(in_minutes))
        in_seconds = (in_minutes - minutes)*60.0
        return (sgn, hours, minutes, in_seconds)

    def as_sdms(self):
        r'''
        Get the angle in degrees, minutes, and seconds. It does not
        round off the degrees and minutes based on the seconds. See examples.

        **Returns**

        A tuple containing (sign, degrees, minutes, seconds)

        **Examples**

        >>> fmt = '%s%02dd %02dm %06.3fs'
        >>> fmt % Angle(sdms = ('+', 3, 10, 59.99999)).as_sdms()
        '+03d 10m 60.000s'
        >>> fmt % Angle(sdms = ('+', 3, 11, 0.0)).as_sdms()
        '+03d 10m 60.000s'
        >>> fmt % Angle(sdms = ('-', 3, 11, 0.1)).as_sdms()
        '-03d 11m 00.100s'

        '''
        sgn      = sign_char(self.rad)
        abs_rad  = abs(self.rad)
        in_degrees = abs_rad * 180/pi
        degrees    = int(floor(in_degrees))
        in_minutes = (in_degrees - degrees)*60.0
        minutes    = int(floor(in_minutes))
        in_seconds = (in_minutes - minutes)*60.0
        return (sgn, degrees, minutes, in_seconds)


    def __float__(self):
        r'''
        Implement float(angle).

        **Returns**

        A float containing the angle in radians

        **Examples**

        >>> from math import sin, cos
        >>> str(sin(float(Angle(deg = 180.0))))
        '1.2246467991473532e-16'
        >>> cos(float(Angle(deg = 180.0)))
        -1.0
        '''
        return self.rad


    def __add__(self, angle):
        r'''
        Implement Angle() + something, where float(something) is in
        radians.

        **Returns**

        An Angle instance.

        **Examples**

        >>> (Angle(deg = 90) + Angle(deg = 45)).as_deg()
        135.0
        >>> Angle(rad = 2.0) + 2.0
        Angle(rad = 4.0)
        '''
        return Angle(rad = self.as_rad() + float(angle))


    def __sub__(self, angle):
        r'''
        Implement Angle() - something, where float(something) is in
        radians.

        **Returns**

        An Angle instance.

        **Examples**

        >>> (Angle(deg = 90) - Angle(deg = 45)).as_deg()
        45.0
        >>> Angle(rad = 2.0) - 0.5
        Angle(rad = 1.5)
        '''
        return Angle(rad = self.as_rad() - float(angle))


    def __mul__(self, factor):
        r'''
        Implement Angle() * factor

        **Parameters**

        factor : number
            The factor to multiply the angle by.

        **Returns**

        An Angle instance.

        **Examples**

        >>> (Angle(deg = 90)*3).as_deg()
        270.0
        >>> Angle(rad = 2.0)*3.0
        Angle(rad = 6.0)
        '''
        return Angle(rad = self.as_rad() * float(factor))



    def __div__(self, divisor):
        r'''
        Implement Angle()/divisor

        **Parameters**

        divisor : number
            The factor to divide the angle by.

        **Returns**

        An Angle instance.

        **Examples**

        >>> (Angle(deg = -90)/2).as_deg()
        -45.0
        >>> Angle(rad = 2.0)/4.0
        Angle(rad = 0.5)
        '''
        return Angle(rad = self.as_rad() / float(divisor))


    def __truediv__(self, divisor):
        r'''
        Implement Angle()/divisor

        **Parameters**

        divisor : number
            The factor to divide the angle by.

        **Returns**

        An Angle instance.

        **Examples**

        >>> (Angle(deg = -90)/2).as_deg()
        -45.0
        >>> Angle(rad = 2.0)/4.0
        Angle(rad = 0.5)
        '''
        return Angle(rad = self.as_rad() / float(divisor))

