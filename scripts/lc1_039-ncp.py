import momxml
import ephem
import sys

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

antenna_set     = 'HBA_DUAL_INNER'
band            = 'HBA_LOW'
stations        = momxml.station_list('nl', exclude = [])
int_s           = 2.0
chan            = 64
target_subbands = '77..456' # 380 subbands 115 -- 189 MHz
cal_subbands    = '77,99,121,144,166,188,211,233,257,278,299,321,345,367,389,412,434,456'


for i in range(5):
    cal_fields.append(momxml.TargetSource('NCP-'+chr(ord('A')+i),
                                          ra_angle  = ra_3c61_1 + ra_inc*(i+1),
                                          dec_angle = dec_3c61_1))

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
    beam_list        = [momxml.Beam(target, target_subbands)] + [momxml.Beam(field, cal_subbands) for field in cal_fields],
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
main_folder = momxml.Folder(children=[date_folder], name='EoR-NCP', description='EoR NCP observations', mom_id=322102)
print momxml.xml([main_folder], 'LC1_039')
