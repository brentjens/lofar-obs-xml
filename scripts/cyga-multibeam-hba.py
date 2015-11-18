from momxml.observation import *
from momxml.utilities import station_list
import ephem

#subbands = [102, 139, 176, 212, 249, 261, 285, 322, 358]
subbands =  [103,137,171,205,239]
duration = 60



radec = [tuple([float(x) for x in line.split()]) for line in open('radeclist_hba_high.txt')]

observations = []

for i, subband in enumerate(subbands):

    beam_list = [Beam(TargetSource(name   = ('Cyg A field %03d' % field_id),
                                   ra_angle  = Angle(deg = pos[0]),
                                   dec_angle = Angle(deg = pos[1])),
                                   subband_spec = str(subband))
                for field_id, pos in enumerate(radec)]
    observations.append(
        Observation(antenna_set      = 'HBA_DUAL',
                    frequency_range  = 'HBA_HIGH',
                    start_date       = ephem.Date(ephem.Date((2012, 7, 12, 0, 0, 1.0))+4*ephem.minute*i).tuple(),
                    duration_seconds = 60,
                    stations         = station_list('nl', exclude = ['CS013']),
                    clock_mhz        = 200,
                    beam_list        = beam_list))

print as_xml_mom_project(observations)
