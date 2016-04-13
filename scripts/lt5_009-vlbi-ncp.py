#!/usr/bin/env python

import momxml
import ephem
import sys
from numpy import array

# 17:29 - 06:10

cal_duration_s   = 5*60
source_catalogue = momxml.SourceCatalogue()

mid_day    = momxml.ephem.Date(sys.argv[1])
start_date = momxml.ephem.Date(momxml.next_sunset(mid_day)  + 20*momxml.ephem.minute)
end_date   = momxml.ephem.Date(momxml.next_sunrise(start_date) - 20*momxml.ephem.minute)

total_duration_s = (end_date - start_date)*24*3600.0
target_duration_s = total_duration_s - 2*cal_duration_s - 2*61.0

target       = momxml.simbad('NCP')
target.name = 'NCP-VLBI-%4d-%02d-%02d' % start_date.tuple()[0:3]

pre_cal      = source_catalogue.cal_source(start_date, 'HBA')
post_cal     = source_catalogue.cal_source(start_date+(target_duration_s+2*cal_duration_s)*ephem.second, 'HBA')
cal_fields   = [momxml.TargetSource(
    name='J%02d%02d%04.1f+%02d%02d%04.1f'% (ra+dec),
    ra_angle=momxml.Angle(hms=ra),
    dec_angle=momxml.Angle(sdms=('+',)+dec))
                for ra, dec in [
                        (( 1, 17, 28.7,),    (89, 28, 49.1)),
                        ((10, 57, 40.0,),    (88, 58, 47.0)),
                        (( 1, 10, 47.3,),    (87, 38, 21.1)),
                        ((22, 36, 21.1,),    (88, 14, 54.7)),
                        (( 6, 22,  9.8,),    (87, 19, 50.0)),
                        (( 5, 32, 46.4,),    (87, 31, 40.8)),
                        (( 8,  9, 33.0,),    (87,  2,  0.0)),
                        ((12, 14, 18.0,),    (87, 50,  0.0)),
                        ((20, 11, 59.2,),    (88, 11, 48.2))
                ]]

antenna_set     = 'HBA_DUAL_INNER'
band            = 'HBA_LOW'
stations        = momxml.station_list('all', exclude = [], include=['PL610', 'PL611', 'PL612'])
int_s           = 1.0
chan            = 32
target_subbands = '74..79,111..116,141..146,173..178,214..219,250..255,288..293,326..331,370..375'

#scintillation_3c220_3 = momxml.TargetSource(name      = '3C 220.3',
#                                     ra_angle  = momxml.Angle(shms = ('+', 9, 39, 23.4)),
#                                     dec_angle = momxml.Angle(sdms = ('+', 83, 15, 26.2)))


# 01 17 28.7    89 28 49.1
# 10 57 40.0    88 58 47.0
# 01 10 47.3    87 38 21.1
# 22 36 21.1    88 14 54.7
# 06 22 09.8    87 19 50.0
# 05 32 46.4    87 31 40.8
# 08 09 33.0    87 02 00.0
# 12 14 18.0    87 50 00.0
# 20 11 59.2    88 11 48.2

# 74-79
# 111-116
# 141-146
# 173-178
# 214-219
# 250-255
# 288-293
# 326-331
# 370-375



sys.stderr.write('PRE : '+str(pre_cal)+ '\n')
sys.stderr.write('MAIN: '+str(target) + '\n')
for cal in cal_fields:
    sys.stderr.write(' CAL: '+str(cal)+ '\n')
sys.stderr.write('POST: '+ str(post_cal)+'\n')

backend = momxml.BackendProcessing(channels_per_subband     = chan,
                                   integration_time_seconds = int_s)

observations = []
current_date = start_date

observations.append(momxml.Observation(
    beam_list        = [momxml.Beam(pre_cal, target_subbands)],
    antenna_set      = antenna_set,
    frequency_range  = band,
    start_date       = ephem.Date(current_date).tuple(),
    duration_seconds = cal_duration_s,
    stations         = stations,
    clock_mhz        = 200,
    bit_mode         = 8,
    backend          = backend,
    initial_status   = 'approved'))

current_date += cal_duration_s*ephem.second + 61*ephem.second

observations.append(momxml.Observation(
    beam_list        = [momxml.Beam(target, '77,78')] + [momxml.Beam(field, target_subbands) for field in cal_fields],
    antenna_set      = antenna_set,
    frequency_range  = band,
    start_date       = ephem.Date(current_date).tuple(),
    duration_seconds = target_duration_s,
    stations         = stations,
    clock_mhz        = 200,
    bit_mode         = 8,
    backend          = backend,
    initial_status   = 'approved'))

        
        
current_date += target_duration_s*ephem.second + 61*ephem.second

        
observations.append(momxml.Observation(
    beam_list        = [momxml.Beam(post_cal, target_subbands)],
    antenna_set      = antenna_set,
    frequency_range  = band,
    start_date       = ephem.Date(current_date).tuple(),
    duration_seconds = cal_duration_s,
    stations         = stations,
    clock_mhz        = 200,
    bit_mode         = 8,
    backend          = backend,
    initial_status   = 'approved'))


date_folder = momxml.Folder(children=observations, name='EoR-%s' % target.name,
                            description = 'EoR-%s' % target.name,
                            grouping_parent = True)
main_folder = momxml.Folder(children=[date_folder], name='EoR-NCP', description='EoR NCP observations')


with open('eor-ncp-vlbi-%d%02d%02d.xml' % (start_date.tuple()[0:3]), 'w') as output:
    output.write(momxml.xml([main_folder], 'LT5_009', description='The LOFAR EoR project'))
