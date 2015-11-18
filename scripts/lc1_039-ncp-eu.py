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
cal_fields   = [momxml.simbad('3C61.1'),
                momxml.TargetSource('J0121+8928',
                                    momxml.Angle(hms=(1, 17, 32.82)),
                                    momxml.Angle(sdms=('+', 89, 28, 48.7)))]
antenna_set     = 'HBA_DUAL_INNER'
band            = 'HBA_LOW'
stations        = momxml.station_list('all', exclude = [])
int_s           = 2.0
chan            = 64
target_subbands = '77..456' # 380 subbands 115 -- 189 MHz
cal_subbands    = ','.join([str(i) for i in (range(50, 207, 6)+range(213, 396, 7))])


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
                            description = 'EoR-EU-%s' % target.name,
                            grouping_parent = True)
main_folder = momxml.Folder(children=[date_folder], name='EoR-NCP', description='EoR NCP observations', mom_id=322102)
print momxml.xml([main_folder], 'LC1_039')
