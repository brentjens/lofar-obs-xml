r'''
Module to convert common values to a LOFAR MoM specific ASCII
representation.
'''

def mom_antenna_name_from_mac_name(mac_name):
    r'''
    Converts 'HBA_ONE' to 'HBA One', 'LBA_SPARSE_EVEN' to 'LBA Sparse
    Even', etc.

    **Parameters**

    mac_name : string
        One of ['LBA_INNER', 'LBA_OUTER', 'LBA', 'HBA', 'HBA_ZERO',
        'HBA_ONE', 'HBA_DUAL', 'HBA_JOINED']

    **Returns**

    A string.

    **Examples**

    >>> valid_names =  ['LBA_INNER', 'LBA_OUTER', 'LBA', 'HBA', 'HBA_ZERO', 
    ...                 'HBA_ONE', 'HBA_DUAL', 'HBA_JOINED', 'HBA_DUAL_INNER']
    >>> [mom_antenna_name_from_mac_name(name) for name in valid_names]
    ['LBA Inner', 'LBA Outer', 'LBA', 'HBA', 'HBA Zero', 'HBA One', 'HBA Dual', 'HBA Joined', 'HBA Dual Inner']
    '''
    name = mac_name.split('_')
    return ' '.join([name[0]] + [s.capitalize() for s in name[1:]])



def mom_frequency_range(freq_band_name, clock_mhz):
    r'''
    Obtain a string containing the MoM frequency range for a given
    frequency band.

    **Parameters**

    freq_band_name : string
        Allowed frequency bands are: 'LBA_LOW' (10-90), 'LBA_HIGH'
        (30-90), 'HBA_LOW' (110-190), 'HBA_MID' (170-230), and
        'HBA_HIGH' (210-250).

    clock_mhz : int
        Clock frequency in MHz. Either 200 or 160.

    **Returns**

    A string.

    **Examples**

    >>> for band in ['LBA_LOW', 'LBA_HIGH', 'HBA_LOW', 'HBA_HIGH']:
    ...    mom_frequency_range(band, 200)
    '10-90 MHz'
    '30-90 MHz'
    '110-190 MHz'
    '210-250 MHz'
    >>> for band in ['LBA_LOW', 'LBA_HIGH', 'HBA_MID']:
    ...    mom_frequency_range(band, 160)
    '10-70 MHz'
    '30-70 MHz'
    '170-230 MHz'

    '''
    if clock_mhz == 200:
        translation_table = {'LBA_LOW' : '10-90 MHz',
                             'LBA_HIGH': '30-90 MHz',
                             'HBA_LOW' : '110-190 MHz',
                             'HBA_HIGH': '210-250 MHz'}
    elif clock_mhz == 160:
        translation_table = {'LBA_LOW' : '10-70 MHz',
                             'LBA_HIGH': '30-70 MHz',
                             'HBA_MID' : '170-230 MHz'}
    else:
        translation_table = {}
    return translation_table[freq_band_name]



def mom_timestamp(year, month, day, hours, minutes, seconds):
    r'''
    Return the MoM representation of a date.

    **Parameters**

    year : int
        The year. Example: 2012.

    mont : int
        The month in the range 1 (January) to 12 (December).

    day : int
        The day of the month in the range 1 to 31.

    hours : int
        The hours since the beginning of the day in the range 0 to 23.

    minutes : int
        The minutes since the beginning of the hour in the range 0 to 59.

    seconds : int
        The seconds since the beginning of the minute in the range 0
        to 60, just in case of leap seconds.

    **Returns**

    A string.

    **Raises**

    ValueError
        If one of the arguments is out of range.

    **Examples**

    >>> mom_timestamp(2012,  1,  1,  0,  0,  0)
    '2012-01-01T00:00:00'
    >>> mom_timestamp(2012,  1,  2,  3,  4,  5)
    '2012-01-02T03:04:05'
    >>> mom_timestamp(2012, 12, 31, 23, 59, 59)
    '2012-12-31T23:59:59'

    Some bad examples:

    >>> mom_timestamp(2012,  0,  12, 13, 14, 15)
    Traceback (most recent call last):
    ...
    ValueError: month (0) not in range 1..12
    >>> mom_timestamp(2012,  13, 12, 13, 14, 15)
    Traceback (most recent call last):
    ...
    ValueError: month (13) not in range 1..12
    >>> mom_timestamp(2012,  11,  0, 13, 14, 15)
    Traceback (most recent call last):
    ...
    ValueError: day (0) not in range 1..31
    >>> mom_timestamp(2012,  11, 32, 13, 14, 15)
    Traceback (most recent call last):
    ...
    ValueError: day (32) not in range 1..31
    >>> mom_timestamp(2012,  11, 12, -1, 14, 15)
    Traceback (most recent call last):
    ...
    ValueError: hours (-1) not in range 0..23
    >>> mom_timestamp(2012,  11, 12, 24, 14, 15)
    Traceback (most recent call last):
    ...
    ValueError: hours (24) not in range 0..23
    >>> mom_timestamp(2012,  11, 12, 13, -1, 15)
    Traceback (most recent call last):
    ...
    ValueError: minutes (-1) not in range 0..59
    >>> mom_timestamp(2012,  11, 12, 13, 60, 15)
    Traceback (most recent call last):
    ...
    ValueError: minutes (60) not in range 0..59
    >>> mom_timestamp(2012,  11, 12, 13, 14, -1)
    Traceback (most recent call last):
    ...
    ValueError: seconds (-1) not in range 0..60
    >>> mom_timestamp(2012,  11, 12, 13, 14, 61)
    Traceback (most recent call last):
    ...
    ValueError: seconds (61) not in range 0..60

    But:

    >>> mom_timestamp(2012,  6, 30, 23, 59, 60)
    '2012-06-30T23:59:60'

    '''
    if not month in range(1, 13):
        raise ValueError('month (%r) not in range 1..12' % month)
    if not day in range(1, 32):
        raise ValueError('day (%r) not in range 1..31' % day)
    if not hours in range(0, 24):
        raise ValueError('hours (%r) not in range 0..23' % hours)
    if not minutes in range(0, 60):
        raise ValueError('minutes (%r) not in range 0..59' % minutes)
    if not seconds in range(0, 61):
        raise ValueError('seconds (%r) not in range 0..60' % seconds)
    
    return '%4d-%02d-%02dT%02d:%02d:%02d' % (year, month, day,
                                             hours, minutes, seconds)


def mom_duration(hours = None, minutes = None, seconds = None):
    r'''
    Format an observation- or beam duration.

    **Parameters**

    hours : int
        Amount of hours for the observation.

    minutes : int
        Amount of minutes for the observation.

    seconds : int
        Amount of seconds for the observation.
        
    **Returns**

    A string.

    **Examples**

    >>> mom_duration(hours = 3)
    'PT03H'
    >>> mom_duration(minutes = 100)
    'PT100M'
    >>> mom_duration(seconds = 200) 
    'PT200S'
    >>> mom_duration(hours = 2, minutes = 0, seconds = 59)
    'PT02H00M59S'
    
    '''
    duration = 'PT'
    if hours is not None:
        duration += '%02dH' % int(hours)
    if minutes is not None:
        duration += '%02dM' % int(minutes)
    if seconds is not None:
        duration += '%02dS' % int(seconds)
    return duration


def check_mom_topology(topology_str):
    if len(topology_str) >= 90:
        raise ValueError('Topology %r is more than 89 characters long' % topology_str)
    return topology_str
