from momxml.observation import *
from momxml.utilities import station_list
import ephem

subbands = [159, 189, 220, 251, 276, 307, 338, 379]
duration = 60



radec = [tuple([float(x) for x in line.split()]) for line in open('radeclist.txt')]

observations = []

for i, subband in enumerate(subbands):

    beam_list = [Beam(TargetSource(name = ('Cyg A field %03d' % field_id),
                                   ra_angle   = Angle(deg = pos[0]),
                                   dec_angle  = Angle(deg = pos[1])),
                                   subband_spec = str(subband))
                for field_id, pos in enumerate(radec)]
    observations.append(
        Observation(antenna_set      = 'LBA_INNER',
                    frequency_range  = 'LBA_HIGH',
                    start_date       = ephem.Date(ephem.Date((2012, 5, 3, 4, 0, 1.0))+4*ephem.minute*i).tuple(),
                    duration_seconds = 60,
                    stations         = station_list('all', exclude = ['CS013', 'CS301', 'RS306', 'DE601', 'SE607']),
                    clock_mhz        = 200,
                    beam_list        = beam_list))

print as_xml_mom_project(observations)
