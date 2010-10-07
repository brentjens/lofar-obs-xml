import ephem
from math import pi

def unique(sequence):
    return list(set(sequence))


def lofar_current_sidereal_time():
    """
    Returns an ephem.Angle object with the current sidereal time at
    LOFAR CS002 LBA.
    """
    # CS002 LBA in ITRF2005, epoch 2009.5
    lofar           = ephem.Observer()
    lofar.long      = +6.869837540*pi/180
    lofar.lat       = +52.915122495*pi/180
    lofar.elevation = +49.344
    return lofar.sidereal_time()



def get_station_list(station_set, include_list=[], exclude_list=[]):
    superterp= ['CS002', 'CS003', 'CS004', 'CS005', 'CS006', 'CS007']
    core     = ['CS001']+superterp+['CS017', 'CS021', 'CS024', 'CS026', 'CS030',
                                    'CS032', 'CS101', 'CS103', 'CS201', 'CS301',
                                    'CS302', 'CS401', 'CS501']
    remote   = ['RS106', 'RS205', 'RS208', 'RS306', 'RS307', 'RS503']
    nl       = core + remote
    europe   = ['DE601', 'DE602', 'DE603', 'DE604', 'UK608', 'FR606']
    all_stations = nl + europe

    lookup_table = {'superterp': superterp,
                    'core'     : core,
                    'remote'   : remote,
                    'nl'       : nl,
                    'europe'   : europe,
                    'all'      : all_stations}
    superset= unique(lookup_table[station_set] + include_list)
    return sorted([s for s in superset if s not in exclude_list])

