import momxml
import ephem
import sys
from numpy import sin, cos, sqrt, arctan2, arcsin


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
                

start_search_date = (2013, 6, 17, 12, 0, 0.0)

target       = momxml.TargetSource(name      = 'ELAIS-N1',
                                   ra_angle  = momxml.Angle(shms = ('+', 16, 11, 0.0)),
                                   dec_angle = momxml.Angle(sdms = ('+', 55,  0, 0.0)))

transit_date = momxml.next_date_with_lofar_lst(target.ra_angle.as_rad(), start_search_date)

target.name = 'ELAIS-N1-%4d-%02d-%02d' % transit_date.tuple()[0:3]



cal_fields   = [momxml.TargetSource(name      = '87GB 160333.2+573543',
                                    ra_angle  = momxml.Angle(shms = ('+', 16,  4, 34.5)),
                                    dec_angle = momxml.Angle(sdms = ('+', 57, 28,  1.7)))
                ]
ra_4c45_16    = cal_fields[0].ra_angle
dec_4c45_16   = cal_fields[0].dec_angle
pos_angle_inc = momxml.Angle(deg = 60.0)

antenna_set     = 'HBA_DUAL_INNER'
band            = 'HBA_LOW'
stations        = momxml.station_list('nl')
int_s           = 2.0
chan            = 64
#target_subbands = '77,82,88,94,99,105,110,116,121,127,133,138,144,149,155,160,166,172,177,183,188,194,199,205,211,216,222,227,233,238,244,250,255,261,266,272,277,283,289,294,300,305,311,316,322,328,333,339,344,350,355,361,367,372,378,383,389,394,400,406,411,417,422,428,433,439,445,450,456'
#cal_subbands    = target_subbands
# DAB channel 5C (Friesland): 177.5 -- 179.25 MHz (sb 397..406 inclusive)
target_subbands = '77..396,402,407..456' # '51..442' # 371 subbands 115 -- 189 MHz
gb87_subbands   = '77,80,91,95,104,112,126,131,140,155,158,168,180,185,194,196,212,222,235,239,251,256,266,271,274,293,302,320,327,333,347,355,362,374,393,396,407,410,428,444,455,456'
cal_subbands    = '77,104,131,158,185,212,239,266,293,320,347,374,401,428,456'

#cal_subbands    = '77,99,121,144,155,166,188,211,233,257,278,299,321,345,367,389,412,434,456'
cal_duration_s    = 5*60
target_duration_s = 8*3600


for i in range(5):
    l0, m0 = lm_from_ra_dec(ra_4c45_16, dec_4c45_16, target.ra_angle, target.dec_angle)
    rot    = pos_angle_inc*(1+i)
    l, m   = rotate_lm_CCW(l0, m0, rot)
    ra_angle, dec_angle = ra_dec_from_lm(l, m, target.ra_angle, target.dec_angle)
    cal_fields.append(momxml.TargetSource('ELAIS-N1-'+chr(ord('A')+i),
                                          ra_angle  = ra_angle,
                                          dec_angle = dec_angle))

sys.stderr.write('MAIN: '+str(target) + '\n')
for cal in cal_fields:
    sys.stderr.write(' CAL: '+str(cal)+ '\n')


observations = []
current_date = transit_date - (0.5*target_duration_s + cal_duration_s + 61)*ephem.second

source_catalogue = momxml.SourceCatalogue()
pre_cal      = source_catalogue.cal_source(current_date, 'HBA')
post_cal     = source_catalogue.cal_source(current_date+(target_duration_s+2*cal_duration_s + 120)*ephem.second, 'HBA')

backend = momxml.BackendProcessing(channels_per_subband     = chan,
                                   integration_time_seconds = int_s)


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
    beam_list        = [momxml.Beam(target, target_subbands)] +
                       [momxml.Beam(cal_fields[0], gb87_subbands)] +
                       [momxml.Beam(field, cal_subbands) for field in cal_fields[1:]],
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


date_folder = momxml.Folder(children=observations,
                            name='EoR-%s' % target.name,
                            description = 'EoR-%s' % target.name,
                            grouping_parent = True,
                            label = '0')

obs_folder = momxml.Folder(name        = 'EoR-ELAIS-N1',
                           description = 'ELAIS N1 observations for the EoR',
                           children    = [date_folder],
                           mom_id      = 260476)

print momxml.xml([obs_folder], 'LC0_019')
