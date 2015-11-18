from momxml.observation  import *
from momxml.targetsource import *
from momxml.utilities    import *
from momxml.sourcecatalogue import SourceCatalogue
import momxml

import ephem

cal_time_s = 120.0
src_time_s = 20*60.0
gap_s      = 60.0
duration_s = 4*3600.0
start_date = ephem.Date((2013,  1, 17,  18, 53,  5.0))
end_date   = ephem.Date(start_date + duration_s*ephem.second)
antenna_set = 'HBA_DUAL_INNER'
bit_mode   = 8


lc0_003_fields = [['A', ('+', 3, 32, 59.30), ('+', 54, 34, 43.6)],
                  ['B', ('+', 3, 15,  5.15), ('+', 54, 34, 43.6)],
                  ['C', ('+', 3, 23, 46.70), ('+', 56, 49, 29.5)],
                  ['D', ('+', 3, 24, 16.38), ('+', 52, 19, 57.7)],
                  ['E', ('+', 3, 41, 42.22), ('+', 52, 19, 57.7)],
                  ['F', ('+', 3, 42, 11.90), ('+', 56, 49, 29.5)],
                  ['G', ('+', 3, 50, 53.45), ('+', 54, 34, 43.6)],
                  ['H', ('+', 2, 40, 31.67), ('+', 61, 18, 45.6)]]

targets = [TargetSource(name,
                        ra_angle  = momxml.Angle(shms = ra),
                        dec_angle = momxml.Angle(sdms = dec))
           for name, ra, dec in lc0_003_fields]

cal_list = SourceCatalogue()

calibrator = momxml.simbad('3C 147')
exclude    = ['CS013']
subbands   = '115..131,207..223,279..295,427..443'


cal_beam   = Beam(calibrator, subbands)
src_beams  = [Beam(target   , subbands) for target in targets[0:-1]]
src_beams += [Beam(targets[-1], '207..218')]

observations = []
current_date = start_date
while current_date < end_date:
    observations.append(Observation(
        beam_list        = [cal_beam],
        antenna_set      = antenna_set,
        frequency_range  = 'HBA_LOW',
        start_date       = ephem.Date(current_date).tuple(),
        duration_seconds = cal_time_s,
        stations         = station_list('nl', exclude = exclude),
        clock_mhz        = 200,
        integration_time_seconds = 2,
        channels_per_subband     = 64,
        bit_mode         = bit_mode))

    current_date += cal_time_s * ephem.second
    current_date += gap_s      * ephem.second
    
    observations.append(Observation(
        beam_list        = src_beams,
        antenna_set      = antenna_set,
        frequency_range  = 'HBA_LOW',
        start_date       = ephem.Date(current_date).tuple(),
        duration_seconds = src_time_s,
        stations         = station_list('nl', exclude = exclude),
        clock_mhz        = 200,
        integration_time_seconds = 2,
        channels_per_subband     = 64,
        bit_mode         = bit_mode))

    current_date += src_time_s * ephem.second
    current_date += gap_s      * ephem.second
        


observations.append(Observation(
    beam_list        = [cal_beam],
    antenna_set      = antenna_set,
    frequency_range  = 'HBA_LOW',
    start_date       = ephem.Date(current_date).tuple(),
    duration_seconds = cal_time_s,
    stations         = station_list('nl', exclude = exclude),
    clock_mhz        = 200,
    integration_time_seconds = 2,
    channels_per_subband     = 64,
    bit_mode         = bit_mode))


subfolder = Folder('2013-01-16', children = observations, description = 'Initial LC0_003 test observations')

folder    = Folder('Test observations', children = [subfolder],
                   description = 'Test observations',
                   mom_id = 191281)

print as_xml_mom_project([folder], 'LC0_003')
