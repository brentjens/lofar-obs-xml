#!/usr/bin/env python

import momxml
import ephem
import sys
from numpy import sin, cos, sqrt, arctan2, arcsin, array, pi



# #  ra         dec   (J2000, HMS, DMS)

# 08 01 35.59    50 09 42.00   = SAP000
# 08 03 36.16    45 48 48.04
# 08 04 14.07    47 04 39.66
# 08 05 08.66    48 01 59.99
# 08 06 46.30    48 42 00.00
# 08 07 55.17    49 46 28.99
# 08 10 57.00    49 31 37.50
# 08 13 20.44    50 12 34.00
# 08 13 36.44    48 13 01.88   = SAP008
# 08 14 30.34    45 56 38.70
# 08 14 47.26    47 36 15.00
# 08 16 13.36    44 35 46.74
# 08 19 47.74    52 32 43.23
# 08 20 35.59    47 52 46.67
# 08 21 33.65    47 02 28.50
# 08 22 39.00    51 12 52.40
# 08 25 15.89    44 36 32.22
# 08 25 34.88    48 17 42.81
# 08 30 35.98    45 43 34.54
# 08 33 21.09    51 03 07.95   = SAP019


# #  ra         dec    (J2000, radians)

#   2.101346   0.875486
#   2.110115   0.799594
#   2.112871   0.821661
#   2.116841   0.838340
#   2.123942   0.849975
#   2.128950   0.868733
#   2.142173   0.864411
#   2.152605   0.876320
#   2.153768   0.841549
#   2.157688   0.801875
#   2.158918   0.830849
#   2.165180   0.778352
#   2.180770   0.917089
#   2.184250   0.835657
#   2.188472   0.821025
#   2.193224   0.893863
#   2.204633   0.778573
#   2.206015   0.842911
#   2.227911   0.798074
#   2.239918   0.891029



# subband IDs   (4 groups of 6 contiguous subbands, for SNR purposes in
# VLBI, broadband spectra and to look for direction-dependent 1 MHz structure in the bandpass)

#  80- 85 185-190
# 280-285
# 360-365

# 32channels/subband   !

# 1s time integration  !

# hence 20 x 4x6 = 480 subbands total

# The remaining 8 subbands can go to 3C196  spread over the gaps in
# frequency (e.g. subband ID's   120, 140, 160, 210, 230, 250, 320, 340 


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
                

start_search_date = momxml.ephem.Date(sys.argv[1]+' 14:00:00')

target       = momxml.TargetSource(name      = '3C196',
                                   ra_angle  = momxml.Angle(shms = ('+', 8, 13, 36.0678)),
                                   dec_angle = momxml.Angle(sdms = ('+', 48, 13, 2.581)))

transit_date = momxml.next_date_with_lofar_lst(target.ra_angle.as_rad(), start_search_date)

target.name = '3C196-VLBI%4d%02d%02d' % start_search_date.tuple()[0:3]



cal_fields   = [momxml.TargetSource(
    name='J%02d%02d%04.1f+%02d%02d%04.1f'% (ra+dec),
    ra_angle=momxml.Angle(hms=ra),
    dec_angle=momxml.Angle(sdms=('+',)+dec))
                for ra, dec in [
                        (( 8, 13, 36.0678),   (48, 13,  2.581)),
#                       (( 8, 13, 36.44),    (48, 13,  1.88)),
                        (( 8,  1, 35.59),    (50,  9, 42.00)),
                        (( 8,  3, 36.16),    (45, 48, 48.04)),
                        (( 8,  4, 14.07),    (47,  4, 39.66)),
                        (( 8,  5,  8.66),    (48,  1, 59.99)),
                        (( 8,  6, 46.30),    (48, 42,  0.00)),
                        (( 8,  7, 55.17),    (49, 46, 28.99)),
                        (( 8, 10, 57.00),    (49, 31, 37.50)),
                        (( 8, 13, 20.44),    (50, 12, 34.00)),
                        (( 8, 14, 30.34),    (45, 56, 38.70)),
                        (( 8, 14, 47.26),    (47, 36, 15.00)),
                        (( 8, 16, 13.36),    (44, 35, 46.74)),
                        (( 8, 19, 47.74),    (52, 32, 43.23)),
                        (( 8, 20, 35.59),    (47, 52, 46.67)),
                        (( 8, 21, 33.65),    (47,  2, 28.50)),
                        (( 8, 22, 39.00),    (51, 12, 52.40)),
                        (( 8, 25, 15.89),    (44, 36, 32.22)),
                        (( 8, 25, 34.88),    (48, 17, 42.81)),
                        (( 8, 30, 35.98),    (45, 43, 34.54)),
                        (( 8, 33, 21.09),    (51,  3,  7.95))
                ]]

antenna_set     = 'HBA_DUAL_INNER'
band            = 'HBA_LOW'
stations        = momxml.station_list('all')
int_s           = 1.0 # 2.0
chan            = 32
#  80- 85 185-190
# 280-285
# 360-365

target_subbands = '80..85,120,140,160,185..190,280..285,210,230,250,320,340,360..365'
aux_subbands =  '80..85,185..190,280..285,360..365'
#ubbands_base = array([ 62,  75,  88, 101, 114, 127, 140, 153, 166, 179, 192, 205, 218,
#                           231, 244, 257, 270, 283, 296, 309, 322, 335, 348, 361, 374, 387])
#ubbands_offset = int(sys.argv[2])*6
#al_subbands    = ','.join([str(sb) for sb in (subbands_base+subbands_offset)])
#rint(cal_subbands)
#'77,99,121,144,166,188,211,233,257,278,299,321,345,367,389,412,434,456'

target_duration_s = 8*3600


sys.stderr.write('MAIN: '+str(target) + '\n')
for cal in cal_fields:
    sys.stderr.write(' CAL: '+str(cal)+ '\n')


observations = []
current_date = transit_date - 0.5*target_duration_s*ephem.second

backend = momxml.BackendProcessing(channels_per_subband     = chan,
                                   integration_time_seconds = int_s)

observations.append(momxml.Observation(
    beam_list        = [momxml.Beam(target, target_subbands)] + [momxml.Beam(field, aux_subbands) for field in cal_fields[1:]],
    antenna_set      = antenna_set,
    frequency_range  = band,
    start_date       = ephem.Date(current_date).tuple(),
    duration_seconds = target_duration_s,
    stations         = stations,
    clock_mhz        = 200,
    backend = backend,
    bit_mode         = 8,
    initial_status   = 'approved'))

obs_folder = momxml.Folder(name        = 'EoR-3C196',
                           description = 'EoR 3C 196 observations',
                           children    = observations,
                           grouping_parent = True)

with open('eor-3c196-vlbi-%d%02d%02d.xml' % (start_search_date.tuple()[0:3]), 'w') as output:
    output.write(momxml.xml([obs_folder], 'LT5_009', description='The LOFAR EoR project'))
