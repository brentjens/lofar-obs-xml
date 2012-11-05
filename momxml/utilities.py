r'''
Various support functions that did not fit anywhere else.
'''

import ephem
from math import pi
import sys

class InvalidStationSetError(ValueError):
    r'''
    To be raised if an invalid station set is provided.
    '''


def unique(sequence):
    r'''
    Return a list containing all unique elements of a sequence.

    **Parameters**

    sequence : sequence
        List from which to return all unique elements.

    **Returns**

    A list.

    **Examples**

    >>> unique([1, 2, 3, 4])
    [1, 2, 3, 4]
    >>> unique([2, 'a', 4, 'a', 2])
    ['a', 2, 4]
    '''
    return list(set(sequence))


def flatten_list(list_of_lists):
    r'''
    Takes a list of lists and spits out one list with all sub lists
    concatenated. [[1, 2, 3], [4, 5]] -> [1, 2, 3, 4, 5]

    **Parameters**

    list_of_lists : list of lists
        The list to flatten.

    **Returns**

    A one dimensional list.

    **Examples**

    >>> flatten_list([[1, 2, 3], ['a', True], ['b', ['c', 4]]])
    [1, 2, 3, 'a', True, 'b', ['c', 4]]
    '''
    return [element for sub_list in list_of_lists for element in sub_list]


def lofar_sidereal_time(date):
    r'''
    Returns an ephem.Angle object with the current sidereal time at
    LOFAR CS002 LBA. The CS002 LBA position in ITRF2005 coordinates at
    epoch 2009.5.

    **Examples**

    >>> type(lofar_sidereal_time(ephem.Observer().date))
    <type 'ephem.Angle'>
    >>> lofar           = ephem.Observer()
    >>> lofar.long      = +6.869837540*pi/180
    >>> lofar.lat       = +52.915122495*pi/180
    >>> lofar.elevation = +49.344
    >>> lofar.date      = ephem.Observer().date
    >>> abs(lofar.sidereal_time() - lofar_sidereal_time(lofar.date))
    0.0
    '''
    # CS002 LBA in ITRF2005, epoch 2009.5
    lofar           = ephem.Observer()
    lofar.long      = +6.869837540*pi/180
    lofar.lat       = +52.915122495*pi/180
    lofar.elevation = +49.344
    lofar.date      = date
    return lofar.sidereal_time()



def station_list(station_set, include = None, exclude = None):
    r'''
    Provides a sorted list of station names, given a station set name,
    a list of stations to include, and a list of stations to
    exclude. Names use upper case letters.

    **Parameters**

    station_set : string
        One of 'superterp', 'core', 'remote', 'nl', 'all', or 'none', where
        'nl' is the concatenation of the 'core' and 'remote' sets, and
        all is 'nl' plus 'europe'.

    include : None or list of strings
        List of station names to append to the station set.

    exclude : None or list of strings
        List of station names to remove from the station set.

    **Returns**

    A sorted list of strings containing LOFAR station names.

    **Examples**

    >>> station_list('superterp')
    ['CS002', 'CS003', 'CS004', 'CS005', 'CS006', 'CS007']
    >>> len(station_list('core'))
    24
    >>> station_list('remote')
    ['RS106', 'RS205', 'RS208', 'RS306', 'RS307', 'RS406', 'RS503', 'RS508', 'RS509']
    >>> len(station_list('nl'))
    33
    >>> (station_list('nl', exclude = station_list('remote')) ==
    ...  station_list('core'))
    True
    >>> station_list('europe')
    ['DE601', 'DE602', 'DE603', 'DE604', 'DE605', 'FR606', 'SE607', 'UK608']
    >>> station_list('all')==station_list('nl', include=station_list('europe'))
    True
    >>> len(unique(station_list('all')))
    41
    >>> station_list('wsrt')
    Traceback (most recent call last):
    ...
    InvalidStationSetError: wsrt is not a valid station set.

    '''
    superterp = ['CS002', 'CS003', 'CS004', 'CS005', 'CS006', 'CS007']
    core      = ['CS001'] + superterp + ['CS011', 'CS013', 'CS017', 'CS021',
                                         'CS024', 'CS026', 'CS028', 'CS030',
                                         'CS031', 'CS032', 'CS101', 'CS103',
                                         'CS201', 'CS301', 'CS302', 'CS401',
                                         'CS501']
    remote    = ['RS106', 'RS205', 'RS208', 'RS305', 'RS306', 'RS307',
                 'RS406', 'RS407', 'RS409', 'RS503','RS508', 'RS509']
    netherlands = core + remote
    europe    = ['DE601', 'DE602', 'DE603', 'DE604', 'DE605', 'FR606', 'SE607',
                   'UK608']
    all_stations = netherlands + europe

    lookup_table = {'superterp': superterp,
                    'core'     : core,
                    'remote'   : remote,
                    'nl'       : netherlands,
                    'europe'   : europe,
                    'all'      : all_stations,
                    'none'     : []}
    try:
        if include is None:
            include_list = []
        else:
            include_list = include
        superset = unique(lookup_table[station_set] + include_list)
    except (KeyError,):
        raise InvalidStationSetError('%s is not a valid station set.' %
                                     sys.exc_info()[1].args[0])
    if exclude is None:
        exclude_list = []
    else:
        exclude_list = exclude
    return sorted([s for s in superset if s not in exclude_list])



def validate_enumeration(name, value, allowed):
    r'''
    If ``value`` of kind ``name`` is not in the list of ``allowed``
    values, raise a ``ValueError``. Very useful to verify if a caller
    provided a wrong value for a string that is part of an
    enumeration.

    **Parameters**

    name : string
        The kind of thing the value could represent.

    value : string
        The value to be tested.

    allowed : list of strings
        List of all valid values.

    **Returns**

    True if ``value`` is in ``allowed``.

    **Raises**

    ValueError
        If ``value`` is not in ``allowed``.

    **Example**

    >>> validate_enumeration('observation antenna set', 'core',
    ...                      allowed = ['core', 'remote', 'nl', 'all'])
    True
    >>> validate_enumeration('observation antenna set', 'wsrt',
    ...                      allowed = ['core', 'remote', 'nl', 'all'])
    Traceback (most recent call last):
    ...
    ValueError: 'wsrt' is not a valid observation antenna set; choose one of 'core', 'remote', 'nl', 'all'

    '''
    if value not in allowed:
        raise ValueError('%r is not a valid %s; choose one of %s' %
                         (value, name, '\''+'\', \''.join(allowed)+'\''))
    return True
