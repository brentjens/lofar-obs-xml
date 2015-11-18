import momxml
import ephem
import sys
from math import pi
from numpy import angle, array, exp

def stderr(string):
    sys.stderr.write(string+'\n')
    sys.stderr.flush()

"""
A) The near-LH set,
[Triplet I]
1. H157+58	10:28:51.6456	+58:04:48.000
2. H156+56	10:25:42.8571	+55:39:36.000
3. H158+61	10:32:25.9459	+60:30:00.000
[Triplet II]
1. H162+58	10:47:05.3165	+58:04:48.000
2. H161+56	10:42:51.4286	+55:39:36.000
3. H163+61	10:51:53.5135	+60:30:00.000
[Triplet III]
1. H166+58	11:05:18.9873	+58:04:48.000
2. H165+56	11:00:00.0000	+55:39:36.000
3. H168+61	11:11:21.0811	+60:30:00.000

B) The near-CygA set,
[Triplet I]
1. H281+51	18:45:57.4468	+50:49:12.000
2. H282+48	18:47:16.3636	+48:24:00.000
3. H282+53	18:48:00.0000	+53:14:24.000
[Triplet II]
1. H285+51	19:01:16.5957	+50:49:12.000
2. H285+48	19:01:49.0909	+48:24:00.000
3. H286+53	19:03:60.0000	+53:14:24.000
[Triplet III]
1. H289+51	19:16:35.7447	+50:49:12.000
2. H289+48 	19:16:21.8182	+48:24:00.000
3. H290+53	19:19:60.0000	+53:14:24.000

C) The near-L227+69 set,
[Triplet I]
1. H222+70	14:49:24.7059	+70:10:48.000
2. H224+68	14:56:50.5263	+67:45:36.000
3. H220+73	14:39:60.0000	+72:36:00.000
[Triplet II]
1. H229+70	15:17:38.8235	+70:10:48.000
2. H231+68	15:22:06.3158	+67:45:36.000
3. H228+73	15:11:60.0000	+72:36:00.000
[Triplet III]
1. H236+70	15:45:52.9412	+70:10:48.000
2. H237+68	15:47:22.1053	+67:45:36.000
3. H236+73	15:43:60.0000	+72:36:00.000



Observational setup should be "standard" for MSSS-HBA observations, which is to say
1 min calibrator with 80 subbands
1 min gap
7 min target triplet (240 subbands on 3 target fields, no calibrator)
1 min gap
(next set)

"""


TARGETS_LH = [['Lockman I',
               ['H157+58', '10:28:51.6456', '+58:04:48.000'],
               ['H156+56', '10:25:42.8571', '+55:39:36.000'],
               ['H158+61', '10:32:25.9459', '+60:30:00.000']],
              ['Lockman II',
               ['H162+58', '10:47:05.3165', '+58:04:48.000'],
               ['H161+56', '10:42:51.4286', '+55:39:36.000'],
               ['H163+61', '10:51:53.5135', '+60:30:00.000']],
              ['Lockman III',
               ['H166+58', '11:05:18.9873', '+58:04:48.000'],
               ['H165+56', '11:00:00.0000', '+55:39:36.000'],
               ['H168+61', '11:11:21.0811', '+60:30:00.000']]]

TARGETS_CYG_A = [['near Cyg A I',
                  ['H281+51', '18:45:57.4468', '+50:49:12.000'],
                  ['H282+48', '18:47:16.3636', '+48:24:00.000'],
                  ['H282+53', '18:48:00.0000', '+53:14:24.000']],
                 ['near Cyg A II',
                  ['H285+51', '19:01:16.5957', '+50:49:12.000'],
                  ['H285+48', '19:01:49.0909', '+48:24:00.000'],
                  ['H286+53', '19:03:60.0000', '+53:14:24.000']],
                 ['near Cyg A III',
                  ['H289+51', '19:16:35.7447', '+50:49:12.000'],
                  ['H289+48', '19:16:21.8182', '+48:24:00.000'],
                  ['H290+53', '19:19:60.0000', '+53:14:24.000']]]

TARGETS_L227P69 = [['near L227+69 I',
                    ['H222+70', '14:49:24.7059', '+70:10:48.000'],
                    ['H224+68', '14:56:50.5263', '+67:45:36.000'],
                    ['H220+73', '14:39:60.0000', '+72:36:00.000']],
                   ['near L227+69 II',
                    ['H229+70', '15:17:38.8235', '+70:10:48.000'],
                    ['H231+68', '15:22:06.3158', '+67:45:36.000'],
                    ['H228+73', '15:11:60.0000', '+72:36:00.000']],
                   ['near L227+69 III',
                    ['H236+70', '15:45:52.9412', '+70:10:48.000'],
                    ['H237+68', '15:47:22.1053', '+67:45:36.000'],
                    ['H236+73', '15:43:60.0000', '+72:36:00.000']]]


TARGETS_8bit = [['Sextuplet I',
                 ['H222+70', '14:49:24.7059', '+70:10:48.000'],
                 ['H224+68', '14:56:50.5263', '+67:45:36.000'],
                 ['H220+73', '14:39:60.0000', '+72:36:00.000'],
                 ['H229+70', '15:17:38.8235', '+70:10:48.000'],
                 ['H231+68', '15:22:06.3158', '+67:45:36.000'],
                 ['H228+73', '15:11:60.0000', '+72:36:00.000']],
                ['Sextuplet II',
                 ['H236+70', '15:45:52.9412', '+70:10:48.000'],
                 ['H237+68', '15:47:22.1053', '+67:45:36.000'],
                 ['H236+73', '15:43:60.0000', '+72:36:00.000'],
                 ['H244+70', '16:14:07.0588', '+70:10:48.000'],
                 ['H243+68', '16:12:37.8947', '+67:45:36.000'],
                 ['H244+73', '16:15:60.0000', '+72:36:00.000']],
                ['Sextuplet III',
                 ['H220+63', '14:38:49.4118', '+62:55:12.000'],
                 ['H221+61', '14:45:24.3243', '+60:30:00.000'],
                 ['H220+65', '14:39:60.0000', '+65:20:24.000'],
                 ['H225+63', '15:00:00.0000', '+62:55:12.000'],
                 ['H226+61', '15:04:51.8919', '+60:30:00.000'],
                 ['H226+65', '15:02:51.4286', '+65:20:24.000']],
                ['Sextuplet IV',
                 ['H230+63', '15:21:10.5882', '+62:55:12.000'],
                 ['H231+61', '15:24:19.4595', '+60:30:00.000'],
                 ['H231+65', '15:25:42.8571', '+65:20:24.000'],
                 ['H236+63', '15:42:21.1765', '+62:55:12.000'],
                 ['H236+61', '15:43:47.0270', '+60:30:00.000'],
                 ['H237+65', '15:48:34.2857', '+65:20:24.000']],
                ['Sextuplet V',
                 ['H241+63', '16:03:31.7647', '+62:55:12.000'],
                 ['H241+61', '16:03:14.5946', '+60:30:00.000'],
                 ['H243+65', '16:11:25.7143', '+65:20:24.000'],
                 ['H246+63', '16:24:42.3529', '+62:55:12.000'],
                 ['H246+61', '16:22:42.1622', '+60:30:00.000'],
                 ['H249+65', '16:34:17.1429', '+65:20:24.000']],
                ['Sextuplet VI',
                 ['H251+63', '16:45:52.9412', '+62:55:12.000'],
                 ['H251+61', '16:42:09.7297', '+60:30:00.000'],
                 ['H254+65', '16:57:08.5714', '+65:20:24.000'],
                 ['H257+63', '17:07:03.5294', '+62:55:12.000'],
                 ['H255+61', '17:01:37.2973', '+60:30:00.000'],
                 ['H260+65', '17:19:60.0000', '+65:20:24.000']]]

HOUR_ANGLES = [-2*pi/12., +2*pi/12.0]


class MSSSFieldSet(object):
    def __init__(self,
                 name,
                 target_list,
                 base_subbands = [96,123,143,175,217,238,258,286],
                 int_s         = 2.0,
                 channels      = 64,
                 pointing_s    = 7*60.0,
                 cal_s         = 60.0,
                 bit_mode      = 8):
        self.subbands = momxml.flatten_list([range(sb, sb+10)
                                             for sb in base_subbands])
        self.bit_mode    = bit_mode
        self.int_s       = int_s
        self.channels    = channels
        self.pointing_s  = pointing_s 
        self.cal_s       = cal_s
        self.name        = name
        self.target_list = target_list
        self.gap_s       = 60.0
        self.stations    = momxml.station_list('nl', exclude = ['CS013', 'RS407', 'RS409'])

    def mean_ra_rad(self):
        targets = [momxml.TargetSource(name,
                                       momxml.Angle(rad = float(ephem.hours(ra_str))),
                                       momxml.Angle(rad = float(ephem.degrees(dec_str))))
                   for name, ra_str, dec_str in  self.target_list]
        return angle(array([exp(1j*float(target.ra_angle)) for target in targets]).mean())

        
    def make_obs(self, name, targets, start_date, duration_s):
        #stderr(str(targets))
        return momxml.Observation(
            name             = name,
            antenna_set      = 'HBA_DUAL_INNER',
            frequency_range  = 'HBA_LOW',
            start_date       = ephem.Date(start_date).tuple(),
            duration_seconds = duration_s,
            stations         = self.stations,
            clock_mhz        = 200,
            integration_time_seconds = self.int_s,
            bit_mode                 = self.bit_mode,
            channels_per_subband     = self.channels,
            beam_list = [momxml.Beam(target, self.subbands) for target in targets])
            

    def obs_list(self, central_date):
        observations = []
        duration_s   =  self.sequence_duration_s()
        start_date   = ephem.Date(central_date) - 0.5*duration_s*ephem.second
        current_date = ephem.Date(start_date)
        end_date     = current_date + duration_s*ephem.second
        cal_source   = momxml.SourceCatalogue().cal_source(current_date + (0.5*duration_s)*ephem.second, 'HBA')

        obs_name   = self.name
        targets = [momxml.TargetSource(beam_name,
                                       momxml.Angle(rad = float(ephem.hours(ra_str))),
                                       momxml.Angle(rad=float(ephem.degrees(dec_str))))
                   for beam_name, ra_str, dec_str in  self.target_list]

        observations.append(self.make_obs(None, [cal_source], current_date, self.cal_s))
        current_date += (self.cal_s + self.gap_s)*ephem.second
        observations.append(self.make_obs(obs_name, targets, current_date, self.pointing_s))
        return observations

            
    def sequence_duration_s(self):
        duration_s = (self.cal_s + self.gap_s + self.pointing_s)
        return duration_s
        



start_date = (2012, 12, 16, 6, 0, 0)

all_fields = TARGETS_8bit
field_sets = [MSSSFieldSet(obs[0], obs[1:]) for obs in all_fields]

date_tagged_field_sets = []
for field_set in field_sets:
    for ha in HOUR_ANGLES:
        date_tagged_field_sets.append((field_set,
                                       momxml.next_date_with_lofar_lst(field_set.mean_ra_rad() + ha,
                                                                       start_date = start_date)))
            
observations = []
for field_set, date in sorted(date_tagged_field_sets, key=lambda x:str(ephem.Date(x[1]))):
    stderr('%20s: %s' % (field_set.name, str(ephem.Date(date))))
    observations += field_set.obs_list(date)

subfolder = momxml.Folder(name        = 'MSSS-HBA-2012-12-16',
                          description = '8 bit MSSS HBA experiment',
                          children    = observations)

folder    = momxml.Folder(name        = 'MSSS commissioning',
                          description = 'MSSS experimental observations',
                          mom_id      = 173637,
                          children    = [subfolder])

print momxml.as_xml_mom_project([folder], 'Commissioning2012')
