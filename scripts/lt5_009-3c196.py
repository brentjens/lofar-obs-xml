#!/usr/bin/env python

import momxml
import ephem
import sys
from numpy import sin, cos, sqrt, arctan2, arcsin, array, pi


def lm_from_ra_dec(ra_angle, dec_angle, ra0_angle, dec0_angle):
    l_rad = cos(float(dec_angle))*sin(float(ra_angle - ra0_angle))
    m_rad = sin(float(dec_angle))*cos(float(dec0_angle)) - cos(float(dec_angle))*sin(float(dec0_angle))*cos(float(ra_angle - ra0_angle))
    return (l_rad, m_rad)


def ra_dec_from_lm(l_rad, m_rad, ra0_angle, dec0_angle):
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
                

def single_observation(start_search_0ut):
        start_search_date = momxml.ephem.Date(start_search_0ut+' 14:00:00')
        target       = momxml.TargetSource(name      = '3C196',
                                           ra_angle  = momxml.Angle(shms = ('+', 8, 13, 36.0678)),
                                           dec_angle = momxml.Angle(sdms = ('+', 48, 13, 2.581)))

        auxiliary = momxml.TargetSource(name      = '3C196-32A',
                                        ra_angle  = momxml.Angle(shms=('+',  8, 22, 36.91)),
                                        dec_angle = momxml.Angle(sdms=('+', 51, 12, 29.5)))

        transit_date = momxml.next_date_with_lofar_lst(target.ra_angle.as_rad(), start_search_date)

        target.name = '3C196-%4d-%02d-%02d' % start_search_date.tuple()[0:3]

        antenna_set     = 'HBA_DUAL_INNER'
        band            = 'HBA_LOW'
        stations        = momxml.station_list('all')
        int_s           = 2.0 # 2.0
        chan            = 64
        target_subbands = '62..393' # 380 subbands 115 -- 189 MHz
        subbands_main = '70..394'
        subbands_aux = '70..232'

        target_duration_s = 6*3600
        sys.stderr.write('MAIN: '+str(target) + '\n')
        sys.stderr.write(' AUX: '+str(auxiliary)+ '\n')

        current_date = transit_date - 0.5*target_duration_s*ephem.second

        backend = momxml.BackendProcessing(channels_per_subband     = chan,
                                           integration_time_seconds = int_s)

        return momxml.Observation(
            beam_list        = [momxml.Beam(target, subbands_main, storage_cluster='CEP4'),
                                momxml.Beam(auxiliary, subbands_aux, storage_cluster='CEP4')],
                                antenna_set      = antenna_set,
                                frequency_range  = band,
                                start_date       = ephem.Date(current_date).tuple(),
                                duration_seconds = target_duration_s,
                                stations         = stations,
                                clock_mhz        = 200,
                                backend = backend,
                                bit_mode         = 8,
                                initial_status   = 'approved')

observations = []
if len(sys.argv) == 1:
    for start_search_0ut in open('schedule-eor-3c196.txt').readlines():
        observations.append(single_observation(start_search_0ut))
else:
    for start_search_0ut in sys.argv[1:]:
        observations.append(single_observation(start_search_0ut))
    
obs_folder = momxml.Folder(name        = 'EoR-3C196',
                           description = 'EoR 3C 196 observations',
                           children    = observations,
                           grouping_parent = True)

with open('eor-3c196-lc7_022-20170127.xml', 'w') as output:
    output.write(momxml.xml([obs_folder], 'LC7_022', description='The LOFAR EoR project'))
