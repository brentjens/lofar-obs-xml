#!/usr/bin/env python2

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
target.name = 'NCP-%4d-%02d-%02d' % start_date.tuple()[0:3]

pre_cal      = source_catalogue.cal_source(start_date, 'HBA')
post_cal     = source_catalogue.cal_source(start_date+(target_duration_s+2*cal_duration_s)*ephem.second, 'HBA')
cal_fields   = [momxml.simbad('3C61.1')]
ra_3c61_1    = cal_fields[0].ra_angle
dec_3c61_1   = cal_fields[0].dec_angle
ra_inc       = momxml.Angle(deg = 60.0)
ra_offset    = momxml.Angle(deg=30.0)

antenna_set     = 'HBA_DUAL_INNER'
band            = 'HBA_LOW'
stations        = momxml.station_list('all', exclude = [])
int_s           = 2.0
chan            = 64
target_subbands = '77..456' # 380 subbands 115 -- 189 MHz
cal_subbands_base = array([77, 101, 125, 149, 173, 197, 221, 245, 269, 293, 317, 341, 365, 389, 413, 437])
cal_subbands_offset = int(sys.argv[2])*6
cal_subbands    = [[','.join([str(sb) for sb in (cal_subbands_base+cal_subbands_offset)])]*5
                   + [','.join([str(sb) for sb in (cal_subbands_base+cal_subbands_offset)][:-1]), '77']][0]

scintillation_3c220_3 = momxml.TargetSource(name      = '3C 220.3',
                                     ra_angle  = momxml.Angle(shms = ('+', 9, 39, 23.4)),
                                     dec_angle = momxml.Angle(sdms = ('+', 83, 15, 26.2)))

cal_dec = momxml.Angle(deg=88.0)

cal_fields[0].name += '-rot30-88deg'
cal_fields[0].ra_angle = ra_3c61_1 + ra_offset
cal_fields[0].dec_angle = cal_dec
for i in range(5):
    cal_fields.append(momxml.TargetSource('NCP-'+chr(ord('A')+i),
                                          ra_angle  = ra_3c61_1 + ra_inc*(i+1)+ ra_offset,
                                          dec_angle = cal_dec))
cal_fields.append(scintillation_3c220_3)

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
    backend          = backend))

current_date += cal_duration_s*ephem.second + 61*ephem.second

observations.append(momxml.Observation(
    beam_list        = [momxml.Beam(target, target_subbands)] + [momxml.Beam(field, subbands) for field, subbands in zip(cal_fields, cal_subbands)],
    antenna_set      = antenna_set,
    frequency_range  = band,
    start_date       = ephem.Date(current_date).tuple(),
    duration_seconds = target_duration_s,
    stations         = stations,
    clock_mhz        = 200,
    bit_mode         = 8,
    backend          = backend))

        
        
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
    backend          = backend))


date_folder = momxml.Folder(children=observations, name='EoR-%s' % target.name,
                            description = 'EoR-%s' % target.name,
                            grouping_parent = True)
main_folder = momxml.Folder(children=[date_folder], name='EoR-NCP', description='EoR NCP observations', mom_id=449282)


with open('eor-ncp-%d%02d%02d.xml' % (start_date.tuple()[0:3]), 'w') as output:
    output.write(momxml.xml([main_folder], 'LC3_028'))
