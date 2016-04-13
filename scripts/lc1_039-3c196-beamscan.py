import momxml
import ephem
import sys
from numpy import arange, sin, cos, sqrt, arctan2, arcsin, pi


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
                

start_search_date = momxml.ephem.Date(momxml.next_sunset(sys.argv[1]))

target       = momxml.TargetSource(name      = '3C196',
                                   ra_angle  = momxml.Angle(shms = ('+', 8, 13, 36.0678)),
                                   dec_angle = momxml.Angle(sdms = ('+', 48, 13, 2.581)))

transit_date = momxml.next_date_with_lofar_lst(target.ra_angle.as_rad(), start_search_date)

target.name = '3C196-%4d-%02d-%02d' % transit_date.tuple()[0:3]


degree  = pi/180.0
offsets =  arange(-3,4)*1.0*degree

lm_pointings = [(l, m) for l in offsets for m in offsets if (l, m) != (0.0, 0.0)]
ra_dec_pointings = [ra_dec_from_lm(l, m, target.ra_angle, target.dec_angle)
                    for (l, m) in lm_pointings]

aux_pointings = [momxml.TargetSource(name = '3C196-GRID-%02d' % field_id,
                                     ra_angle = ra,
                                     dec_angle = dec)
                 for field_id, (ra, dec) in enumerate(ra_dec_pointings)]
                                     

antenna_set     = 'HBA_DUAL_INNER'
band            = 'HBA_LOW'
stations        = momxml.station_list('nl')
int_s           = 2.0
chan            = 64
subbands        = '77,124,173,226,265,314,361,407,451'
target_duration_s = 6*3600


sys.stderr.write('MAIN: '+str(target) + '\n')
for field in aux_pointings:
    sys.stderr.write(' GRID: '+str(field)+ '\n')

all_fields = [target] + aux_pointings

observations = []
current_date = transit_date - 0.5*target_duration_s*ephem.second

backend = momxml.BackendProcessing(channels_per_subband     = chan,
                                   integration_time_seconds = int_s)

observations.append(momxml.Observation(
    beam_list        = [momxml.Beam(field, subbands) for field in all_fields],
    antenna_set      = antenna_set,
    frequency_range  = band,
    start_date       = ephem.Date(current_date).tuple(),
    duration_seconds = target_duration_s,
    stations         = stations,
    clock_mhz        = 200,
    backend          = backend,
    bit_mode         = 8))

obs_folder = momxml.Folder(name        = 'EoR-3C196',
                           description = 'EoR 3C 196 observations',
                           children    = observations,
                           mom_id      = 322103)

print momxml.xml([obs_folder], 'LC1_039')
