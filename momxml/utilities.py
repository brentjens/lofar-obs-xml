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


def lofar_observer(date = None):
    r'''
    **Parameters**

    date : ephem.Date
        The date to set for the ephem.Observer() instance
    
    **Returns**
    
    An ephem.Observer() instance for the LOFAR core.

    **Examples**
    
    >>> lofar_observer('2013/04/15 12:34:56')
    <ephem.Observer date='2013/4/15 12:34:56' epoch='2000/1/1 12:00:00' lon=6:52:11.4 lat=52:54:54.4 elevation=49.344m horizon=0:00:00.0 temp=15.0C pressure=1010.0mBar>

    '''
    lofar           = ephem.Observer()
    lofar.long      = +6.869837540*pi/180
    lofar.lat       = +52.915122495*pi/180
    lofar.elevation = +49.344
    if date is not None:
        lofar.date = date
    return lofar

    

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
    lofar           = lofar_observer(date)
    return lofar.sidereal_time()


def next_date_with_lofar_lst(lst_rad, start_date = None):
    r'''
    '''
    if not start_date:
        start_date = ephem.Observer().date
    else:
        start_date = ephem.Date(start_date)
    lst = lst_rad
    lst_at_start_rad  = float(lofar_sidereal_time(start_date))
    while lst < lst_at_start_rad:
        lst = lst + 2*pi
    delta_lst_rad = lst - lst_at_start_rad
    delta_utc_rad = delta_lst_rad/1.002737904
    return ephem.Date(start_date + ephem.hour*(delta_utc_rad*12/pi))


def next_sunrise(date, observer = None):
    r'''
    Return an ephem.Date instance with the next sunrise at LOFAR, or
    any other ephem.Observer, if provided.

    **Parameters**
    
    date : ephem.Date
        Date from which to look for sunrise.

    observer : None or ephem.Observer
        Location for which Sunrise is computed. Default is LOFAR core
        if None is provided.

    **Returns**
    
    An ephem.Date instance.

    **Examples**
    
    >>> print(next_sunrise('2013/04/03 12:00:00'))
    2013/4/4 04:58:56
    '''

    if observer is None:
        observer = lofar_observer(date)
    return observer.next_rising(ephem.Sun())




def next_sunset(date, observer = None):
    r'''
    Return an ephem.Date instance with the next sunset at LOFAR, or
    any other ephem.Observer, if provided.

    **Parameters**
    
    date : ephem.Date
        Date from which to look for sunrise.

    observer : None or ephem.Observer
        Location for which Sunrise is computed. Default is LOFAR core
        if None is provided.

    **Returns**
    
    An ephem.Date instance.

    **Examples**
    
    >>> print(next_sunset('2013/04/03 12:00:00'))
    2013/4/3 18:11:17
    '''

    if observer is None:
        observer = lofar_observer(date)
    return observer.next_setting(ephem.Sun())



def station_list(station_set, include = None, exclude = None):
    r'''
    Provides a sorted list of station names, given a station set name,
    a list of stations to include, and a list of stations to
    exclude. Names use upper case letters.

    **Parameters**

    station_set : string
        One of 'superterp', 'core', 'remote', 'nl', 'all', or 'none', where
        'nl' is the concatenation of the 'core' and 'remote' sets, and
        all is 'nl' plus 'eu'.

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
    ['RS106', 'RS205', 'RS208', 'RS210', 'RS305', 'RS306', 'RS307', 'RS310', 'RS406', 'RS407', 'RS409', 'RS503', 'RS508', 'RS509']
    >>> len(station_list('nl'))
    37
    >>> (station_list('nl', exclude = station_list('remote')) ==
    ...  station_list('core'))
    True
    >>> station_list('eu')
    ['DE601', 'DE602', 'DE603', 'DE604', 'DE605', 'FR606', 'SE607', 'UK608']
    >>> station_list('all')==station_list('nl', include=station_list('europe'))
    True
    >>> len(unique(station_list('all')))
    45
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
    remote    = ['RS106', 'RS205', 'RS208', 'RS210', 'RS305', 'RS306', 'RS307',
                 'RS310', 'RS406', 'RS407', 'RS409', 'RS503', 'RS508', 'RS509']
    netherlands = core + remote
    europe    = ['DE601', 'DE602', 'DE603', 'DE604', 'DE605', 'FR606', 'SE607',
                   'UK608']
    all_stations = netherlands + europe

    lookup_table = {'superterp': superterp,
                    'core'     : core,
                    'remote'   : remote,
                    'nl'       : netherlands,
                    'eu'       : europe,
                    'all'      : all_stations,
                    'none'     : []}
    try:
        if include is None:
            include_list = []
        else:
            include_list = [station.upper() for station in include]
        superset = unique(lookup_table[station_set] + include_list)
    except (KeyError,):
        raise InvalidStationSetError('%s is not a valid station set.' %
                                     sys.exc_info()[1].args[0])
    if exclude is None:
        exclude_list = []
    else:
        exclude_list = [station.upper() for station in exclude]
    return sorted([s for s in superset if s not in exclude_list])



def exclude_conflicting_eu_stations(stations):
    r'''
    
    The international stations are connected to the same BlueGene
    IONodes as the HBA1 ear in some core stations. For HBA_ONE,
    HBA_DUAL_INNER, and HBA_DUAL mode, we need to remove either the
    core stations, or the eu stations that conflict. This function
    removes the conflicting eu stations.

    **Parameters**

    stations : list of strings
        The station names in the observation.

    **Returns**

    A list of strings containing only non-conflicting stations, from
    which the EU stations have been removed.

    **Examples**

    >>> exclude_conflicting_eu_stations(['CS001', 'CS002', 'RS407'])
    ['CS001', 'CS002', 'RS407']
    >>> exclude_conflicting_eu_stations(['CS001', 'CS002', 'RS407', 'DE605'])
    ['CS001', 'CS002', 'RS407', 'DE605']
    >>> exclude_conflicting_eu_stations(['CS001', 'CS002', 'CS028', 'RS407', 'DE601', 'DE605', 'UK608'])
    ['CS001', 'CS002', 'CS028', 'RS407', 'DE605', 'UK608']

    '''
    exclude_dict = {'DE601': 'CS001',
                    'DE602': 'CS031',
                    'DE603': 'CS028',
                    'DE604': 'CS011',
                    'DE605': 'CS401',
                    'FR606': 'CS030',
                    'SE607': 'CS301',
                    'UK608': 'CS013'}
    good_stations = []
    
    for station in stations:
        try:
            if exclude_dict[station] not in stations:
                good_stations.append(station)
        except KeyError:
            good_stations.append(station)
    return good_stations


def exclude_conflicting_nl_stations(stations):
    r'''
    
    The international stations are connected to the same BlueGene
    IONodes as the HBA1 ear in some core stations. For HBA_ONE,
    HBA_DUAL_INNER, and HBA_DUAL mode, we need to remove either the
    core stations, or the eu stations that conflict. This function
    removes the conflicting core stations.

    **Parameters**

    stations : list of strings
        The station names in the observation.

    **Returns**

    A list of strings containing only non-conflicting stations, from
    which the core stations have been removed.

    **Examples**

    >>> exclude_conflicting_nl_stations(['CS001', 'CS002', 'RS407'])
    ['CS001', 'CS002', 'RS407']
    >>> exclude_conflicting_nl_stations(['CS001', 'CS002', 'RS407', 'DE605'])
    ['CS001', 'CS002', 'RS407', 'DE605']
    >>> exclude_conflicting_nl_stations(['CS001', 'CS002', 'CS028', 'RS407', 'DE601', 'DE605', 'UK608'])
    ['CS002', 'CS028', 'RS407', 'DE601', 'DE605', 'UK608']

    '''
    exclude_dict = {'CS001': 'DE601',
                    'CS031': 'DE602',
                    'CS028': 'DE603',
                    'CS011': 'DE604',
                    'CS401': 'DE605',
                    'CS030': 'FR606',
                    'CS301': 'SE607',
                    'CS013': 'UK608'}
    good_stations = []
    
    for station in stations:
        try:
            if exclude_dict[station] not in stations:
                good_stations.append(station)
        except KeyError:
            good_stations.append(station)
    return good_stations



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




def lm_from_radec(ra_angle, dec_angle, ra0_angle, dec0_angle):
    l_rad = cos(float(dec_angle))*sin(float(ra_angle - ra0_angle))
    m_rad = sin(float(dec_angle))*cos(float(dec0_angle)) - cos(float(dec_angle))*sin(float(dec0_angle))*cos(float(ra_angle - ra0_angle))
    return (l_rad, m_rad)


def radec_from_lm(l_rad, m_rad, ra0_angle, dec0_angle):
    n_rad  = sqrt(1.0 - l_rad*l_rad - m_rad*m_rad)
    ra_rad = float(ra0_angle) + arctan2(l_rad,
                                        cos(float(dec0_angle))*n_rad - m_rad*sin(float(dec0_angle)))
    dec_rad = arcsin(m*cos(float(dec0_angle)) + sin(float(dec0_angle))*n_rad)
    return (momxml.Angle(rad=ra_rad), momxml.Angle(rad=dec_rad))


def rotate_lm_CCW(l_rad, m_rad, ccw_angle):
    cs = cos(float(ccw_angle))
    ss = sin(float(ccw_angle))

    l_new =  l_rad*cs + m_rad*ss
    m_new = -l_rad*ss + m_rad*cs
    return l_new, m_new
