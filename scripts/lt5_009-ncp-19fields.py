#!/usr/bin/env python

import lofarobsxml as momxml
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

targets       = [momxml.simbad('NCP')]
targets[0].name = 'NCP-%4d-%02d-%02d' % start_date.tuple()[0:3]

s3c61_1    = momxml.simbad('3C61.1')
ra_3c61_1  = s3c61_1.ra_angle
dec_3c61_1 = s3c61_1.dec_angle

aux_dec = momxml.Angle(deg=78.75000001)
ra_inc = momxml.Angle(deg=360/18.0)
ra_offset = momxml.Angle(deg=360/18.0)
aux_fields = []

for i in range(18):
    aux_fields.append(momxml.TargetSource('NCP-'+chr(ord('A')+i),
                                          ra_angle  = ra_3c61_1 + ra_inc*(i) - ra_offset,
                                          dec_angle = aux_dec))


pre_cal      = source_catalogue.cal_source(start_date, 'HBA')
post_cal     = source_catalogue.find_source('3C 196')
#source_catalogue.cal_source(start_date+(target_duration_s+2*cal_duration_s)*ephem.second,
               #                            'HBA')

station_set = 'all'
if len(sys.argv) >= 3:
    station_set = sys.argv[2]
antenna_set     = 'HBA_DUAL_INNER'
band            = 'HBA_LOW'
stations        = momxml.station_list(station_set, exclude = [])
int_s           = 2.0
chan            = 64
target_subbands = '61,67,79,91,103,115,127,139,151,159,202,216,223,230,237,250,256,279,296,301,330,343,365,372,379'



sys.stderr.write('PRE : '+str(pre_cal)+ '\n')
for target in targets+aux_fields:
    sys.stderr.write(' MAIN: '+str(target)+ '\n')
sys.stderr.write('POST: '+ str(post_cal)+'\n')

backend = momxml.BackendProcessing(channels_per_subband     = chan,
                                   integration_time_seconds = int_s)

observations = []
current_date = start_date

observations.append(momxml.Observation(
    beam_list        = [momxml.Beam(pre_cal, target_subbands, storage_cluster='CEP4')],
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
    beam_list        = [momxml.Beam(field, target_subbands, storage_cluster='CEP4')
                        for field in targets+aux_fields],
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
    beam_list        = [momxml.Beam(post_cal, target_subbands, storage_cluster='CEP4')],
    antenna_set      = antenna_set,
    frequency_range  = band,
    start_date       = ephem.Date(current_date).tuple(),
    duration_seconds = cal_duration_s,
    stations         = stations,
    clock_mhz        = 200,
    bit_mode         = 8,
    backend          = backend,
    initial_status   = 'approved'))


date_folder = momxml.Folder(children=observations, name='EoR-%s' % targets[0].name,
                            description = 'EoR-%s-13' % targets[0].name,
                            grouping_parent = True)
main_folder = momxml.Folder(children=[date_folder], name='EoR-NCP', description='EoR NCP observations')


with open('eor-ncp-%d%02d%02d.xml' % (start_date.tuple()[0:3]), 'w') as output:
    output.write(momxml.xml([main_folder], 'LT5_009', description='The LOFAR EoR project'))
