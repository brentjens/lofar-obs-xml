from momxml.observation  import *
from momxml.targetsource import *
from momxml.utilities    import *
import ephem


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



target = TargetSource('L227+69',
                      ra_angle  = Angle(shms = ('+', 15,  7, 49.5652)),
                      dec_angle = Angle(sdms = ('+', 69, 14, 24.0)))

calibrator = TargetSource('3C295',
                          ra_angle  = Angle(shms = ('+', 14, 11, 20.6)),
                          dec_angle = Angle(sdms = ('+', 52, 12,  9.0)))

# target = TargetSource('3C468.1',
#                       ra_angle  = Angle(shms=('+', 23, 50, 54.849)),
#                       dec_angle = Angle(sdms=('+', 64, 40, 19.54)))

# calibrator = TargetSource('3C196',
#                           ra_angle  = Angle(shms=('+', 8, 13, 36.0)),
#                           dec_angle = Angle(sdms=('+', 48, 13, 3.0)))

exclude = []

base_subbands = [ 77, 109, 142, 175, 207, 240,
                 272, 305, 337, 370, 403, 435]
subbands   = flatten_list([range(base, base+10) for base in base_subbands])

cal_time_s = 60.0
src_time_s = 900.0
gap_s      = 60.0
duration_s = 6*3600.0

cal_beam   = Beam(calibrator, subbands)
src_beam   = Beam(target    , subbands)

start_date = ephem.Date((2012, 6, 21,  17, 3, 1.0))
end_date   = ephem.Date(start_date + duration_s*ephem.second)

observations = []
current_date = start_date
while current_date < end_date:
    observations.append(Observation(
        beam_list        = [cal_beam],
        antenna_set      = 'HBA_DUAL',
        frequency_range  = 'HBA_LOW',
        start_date       = ephem.Date(current_date).tuple(),
        duration_seconds = cal_time_s,
        stations         = station_list('nl', exclude = exclude),
        clock_mhz        = 200,
        integration_time_seconds = 2,
        channels_per_subband     = 64))

    current_date += cal_time_s * ephem.second
    current_date += gap_s      * ephem.second
    
    observations.append(Observation(
        beam_list        = [src_beam],
        antenna_set      = 'HBA_DUAL',
        frequency_range  = 'HBA_LOW',
        start_date       = ephem.Date(current_date).tuple(),



observations.append(Observation(
    beam_list        = [cal_beam],
    antenna_set      = 'HBA_DUAL',
    frequency_range  = 'HBA_LOW',
    start_date       = ephem.Date(current_date).tuple(),
    duration_seconds = cal_time_s,
    stations         = station_list('nl', exclude = exclude),
    clock_mhz        = 200,
    integration_time_seconds = 2,
    channels_per_subband     = 64))


print as_xml_mom_project(observations)


# Lockman 
