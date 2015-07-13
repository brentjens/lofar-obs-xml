r'''
Various support functions that did not fit anywhere else.
'''

import ephem
from numpy import pi, cos, sin, arcsin, sqrt, arctan2
from momxml import Angle
import sys

class InvalidStationSetError(ValueError):
    r'''
    To be raised if an invalid station set is provided.
    '''



class AutoReprBaseClass(object):
    r'''
    Base class that implements a simplistic __repr__ function. The
    order in which the members are printed is the same as that in
    which the arguments are set in bthe constructor body.
    '''
    def __repr__(self):
        name    = self.__class__.__name__
        as_dict = self.__dict__
        members = sorted(as_dict.keys())
        longest_member = sorted([len(s) for s in members])[-1]
        member_strings = [mem.ljust(longest_member)+' = '+repr(as_dict[mem])
                          for mem in members]
        sep = '\n'+' '*(len(name)+1)
        indented_member_strings = [('\n'+ ' '*(longest_member+3)).join(
            member.split('\n'))
                                   for member in member_strings]
        unadjusted =  ',\n'.join(indented_member_strings)
        return name+'('+sep.join(unadjusted.split('\n'))+')'




def with_auto_repr(cls):
    r'''
    Class decorator that adds a nicer default __repr__ method to a class.

    **Examples**

    >>> class Elements(object):
    ...     def __init__(self, a, b):
    ...         self.a = a
    ...         self.b = b
    >>> aa = Elements(1, '3')
    >>> print(repr(aa)[0:-16])
    <momxml.utilities.Elements object at
    >>> Elements = with_auto_repr(Elements)
    >>> bb = Elements (1, 'v')
    >>> print(repr(bb))
    Elements(a = 1,
             b = 'v')
    '''
    class AutoReprClass(cls):
        r'''
        Base class that implements a simplistic __repr__ function. The
        order in which the members are printed is the same as that in
        which the arguments are set in bthe constructor body.

        '''

        def __repr__(self):
            name    = cls.__name__
            as_dict = self.__dict__
            members = sorted(as_dict.keys())
            longest_member = sorted([len(s) for s in members])[-1]
            member_strings = [mem.ljust(longest_member)+' = '+repr(as_dict[mem])
                              for mem in members]
            sep = '\n'+' '*(len(name)+1)
            indented_member_strings = [('\n'+ ' '*(longest_member+3)).join(
                member.split('\n'))
                                       for member in member_strings]
            unadjusted =  ',\n'.join(indented_member_strings)
            return name+'('+sep.join(unadjusted.split('\n'))+')'

    return AutoReprClass




def typecheck(variable, type_class, name = None):
    r'''
    Raise TypeError if ``variable`` is not an instance of
    ``type_class``.

    **Parameters**

    variable : any object
        The variable that will be type-checked.

    type_class : type or list of types
        The desired type of ``variable``.

    name : string
        A descriptive name of the variable, used in the error
        message.

    **Examples**

    >>> typecheck(4.0 , float)
    >>> typecheck(None, [int, type(None)])
    >>> typecheck(5   , [int, type(None)])
    >>> typecheck(4.0, [int, type(None)])
    Traceback (most recent call last):
    ...
    TypeError: type(4.0) not in ['int', 'NoneType']
    >>> a = 'blaargh'
    >>> typecheck(a, int, 'a')
    Traceback (most recent call last):
    ...
    TypeError: type(a)('blaargh') not in ['int']
    '''
    template = 'type(%(var)r) not in %(types)r'
    if name is not None:
        template = 'type(%(name)s)(%(var)r) not in %(types)r'
    if type(type_class) == list:
        type_list = type_class
    else:
        type_list = [type_class]
    if type(variable) not in type_list:
            raise TypeError(template %
                            {'name'  : name,
                             'var'   : variable,
                             'types' : [tp.__name__ for tp in type_list]})




def indent(string, amount):
    r'''
    Indent a multi-line string by the given amount.

    string : string
        The string to indent.

    amount : int
        The direction and amount to indent.

    **Examples**

    >> indent('Hi\nThere', 2)
      Hi
      There

    >> indent('Hi\nThere\n\n', -1)
    i
    here
    <BLANKLINE>
    <BLANKLINE>
    '''
    lines = string.split('\n')
    if amount > 0:
        lines = [line if '' == line else ' '*amount + line for line in lines]
    if amount < 0:
        lines = [line[-amount:] for line in lines]
    return '\n'.join(lines)





def unique(sequence):
    r'''
    Return a list containing all unique elements of a sequence.

    **Parameters**

    sequence : sequence
        List from which to return all unique elements.

    **Returns**

    A list.

    **Examples**

    >>> sorted(unique([3, 2, 4, 3, 1, 1, 2]))
    [1, 2, 3, 4]
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




def lower_case(boolean):
    r'''
    Return lower case string representation of a boolean value.

    **Parameters**

    boolean : bool
        The value to convert to a string.

    **Examples**
    >>> lower_case(True)
    'true'
    >>> lower_case(False)
    'false'
    '''
    return repr(boolean).lower()




def parse_subband_list(parset_subband_list):
    r'''
    Parse a subband list from a parset or SAS/MAC / MoM spec.

    **Parameters**

    parset_subband_list : string
        Value of Observation.Beam[0].subbandList

    **Returns**

    A list of integers containing the subband numbers.

    **Raises**

    ValueError
        If a syntax problem is encountered.

    **Examples**

    >>> sb_spec = '[154..163,185..194,215..224,245..254,275..284,10*374]'
    >>> parse_subband_list(sb_spec)
    [154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 374, 374, 374, 374, 374, 374, 374, 374, 374, 374]
    >>> sb_spec = '[77..87,116..127,155..166,194..205,233..243,272..282]'
    >>> parse_subband_list(sb_spec)
    [77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282]
    >>> parse_subband_list('[]')
    []
    >>> parse_subband_list('1,2,10..15,200..202,400')
    [1, 2, 10, 11, 12, 13, 14, 15, 200, 201, 202, 400]
    '''
    stripped_subband_list = parset_subband_list.strip('[] \n\t')
    if stripped_subband_list == '':
        return []
    sub_lists = [word.strip().split('..')
                 for word in stripped_subband_list.split(',')]
    subbands = []
    for sub_list in sub_lists:
        if len(sub_list) == 1:
            multiplication = sub_list[0].split('*')
            if len(multiplication) == 2:
                subbands += [int(multiplication[1])]*int(multiplication[0])
            else:
                subbands.append(int(sub_list[0]))
        elif len(sub_list) == 2:
            subbands += range(int(sub_list[0]), int(sub_list[1])+1)
        else:
            raise ValueError('%r is not a valid sub_range in a subband list' %
                             sub_list)
    return subbands




def lofar_observer(date = None):
    r'''
    **Parameters**

    date : ephem.Date
        The date to set for the ephem.Observer() instance

    **Returns**

    An ephem.Observer() instance for the LOFAR core.

    **Examples**

    >>> lofar_observer('2013/04/15 12:34:56')
    <ephem.Observer date='2013/4/15 12:34:56' epoch='2000/1/1 12:00:00' lon=6:52:11.4 lat=52:54:54.4 elevation=49.343999999999994m horizon=0:00:00.0 temp=15.0C pressure=1010.0mBar>

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
    <class 'ephem.Angle'>
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
    2013/4/3 18:11:18
    '''

    if observer is None:
        observer = lofar_observer(date)
    return observer.next_setting(ephem.Sun())



def antenna_field_sort_key(name):
    r'''
    Produce a sort key for station names.

    **Parameters**

    name : string
        The antenna field's name.

    **Examples**

    >>> antenna_field_sort_key('CS002HBA1')
    21
    >>> antenna_field_sort_key('CS021LBA')
    210
    >>> antenna_field_sort_key('RS106HBA')
    10600
    >>> antenna_field_sort_key('UK608HBA')
    60800
    '''
    station_number = int(name[2:5])*10
    if name[0:2].upper() != 'CS':
        station_number *=10
    if 'HBA1' in name:
        station_number += 1
    return station_number


def sort_station_list(stations):
    r'''
    Sort a station list so we first get the CS, then the RS and EU in
    numerical order.

    **Parameters**

    stations : list of strings
        The station list to sort.

    **Examples**

    >>> sort_station_list(['UK608', 'RS407', 'DE603', 'RS106',
    ...     'RS205', 'CS026', 'SE607', 'CS501', 'DE605', 'RS509',
    ...     'CS001'])
    ['CS001', 'CS026', 'CS501', 'RS106', 'RS205', 'RS407', 'RS509', 'DE603', 'DE605', 'SE607', 'UK608']
    >>> sort_station_list(['UK608HBA', 'RS407HBA', 'DE603HBA', 'RS106HBA',
    ...     'CS026HBA1', 'SE607HBA', 'CS026HBA0', 'CS501HBA0', 'DE605HBA', 'RS509HBA',
    ...     'CS001HBA1'])
    ['CS001HBA1', 'CS026HBA0', 'CS026HBA1', 'CS501HBA0', 'RS106HBA', 'RS407HBA', 'RS509HBA', 'DE603HBA', 'DE605HBA', 'SE607HBA', 'UK608HBA']

    '''
    return sorted(stations, key=antenna_field_sort_key)



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
    38
    >>> (station_list('nl', exclude = station_list('remote')) ==
    ...  station_list('core'))
    True
    >>> station_list('eu')
    ['DE601', 'DE602', 'DE603', 'DE604', 'DE605', 'FR606', 'SE607', 'UK608', 'DE609']
    >>> station_list('all')==station_list('nl', include=station_list('eu'))
    True
    >>> len(unique(station_list('all')))
    47
    >>> station_list('wsrt')
    Traceback (most recent call last):
    ...
    momxml.utilities.InvalidStationSetError: wsrt is not a valid station set.

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
                   'UK608', 'DE609']
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
    return sort_station_list([s for s in superset if s not in exclude_list])



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
    >>> exclude_conflicting_eu_stations(['CS001', 'CS002', 'CS028', 'RS407',
    ...                                  'DE601', 'DE605', 'UK608'])
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
    >>> exclude_conflicting_nl_stations(['CS001', 'CS002', 'CS028',
    ...                                  'RS407', 'DE601', 'DE605', 'UK608'])
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

    >>> validate_enumeration('station set', 'core',
    ...                      allowed = ['core', 'remote', 'nl', 'all'])
    True
    >>> validate_enumeration('station set', 'wsrt',
    ...                      allowed = ['core', 'remote', 'nl', 'all'])
    Traceback (most recent call last):
    ...
    ValueError: 'wsrt' is not a valid station set; choose one of 'core', 'remote', 'nl', 'all'

    '''
    if value not in allowed:
        raise ValueError('%r is not a valid %s; choose one of %s' %
                         (value, name, '\''+'\', \''.join(allowed)+'\''))
    return True




def lm_from_radec(ra_angle, dec_angle, ra0_angle, dec0_angle):
    cos_dec  = cos(float(dec_angle))
    sin_dec  = sin(float(dec_angle))
    cos_dec0 = cos(float(dec0_angle))
    sin_dec0 = sin(float(dec0_angle))
    sin_dra  = sin(float(ra_angle - ra0_angle))
    cos_dra  = cos(float(ra_angle - ra0_angle))

    l_rad = cos_dec*sin_dra
    m_rad = sin_dec*cos_dec0 - cos_dec*sin_dec0*cos_dra
    return (l_rad, m_rad)


def radec_from_lm(l_rad, m_rad, ra0_angle, dec0_angle):
    n_rad  = sqrt(1.0 - l_rad*l_rad - m_rad*m_rad)
    cos_dec0 = cos(float(dec0_angle))
    sin_dec0 = sin(float(dec0_angle))
    ra_rad = float(ra0_angle) + arctan2(l_rad,
                                        cos_dec0*n_rad - m_rad*sin_dec0)
    dec_rad = arcsin(m_rad*cos_dec0 + sin_dec0*n_rad)
    return (Angle(rad = ra_rad), Angle(rad = dec_rad))


def rotate_lm_CCW(l_rad, m_rad, ccw_angle):
    cs = cos(float(ccw_angle))
    ss = sin(float(ccw_angle))

    l_new =  l_rad*cs + m_rad*ss
    m_new = -l_rad*ss + m_rad*cs
    return l_new, m_new
