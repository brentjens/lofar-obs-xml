from momxml.momformats   import *
from momxml.targetsource import *
from momxml.utilities    import *
from math import ceil
import copy
import ephem


class Folder(object):
    def __init__(self, name, children=None, description=None, mom_id=None):
        self.name        = name
        self.children    = children
        self.description = description
        self.mom_id      = mom_id


    def xml(self, project_name):
        preamble        = ''
        children_string = ''
        appendix        = ''
        
        if self.mom_id:
            preamble = '''
<lofar:folder mom2Id="%s">''' % self.mom_id
        else:
            preamble = '''
<lofar:folder>'''
        
        preamble += '''
    <name>'''+self.name+'''</name>'''

        if self.description:
            preamble += '''<description>'''+self.description+'''</description>'''
        preamble += '''
    <children>
'''
        if self.children:
            preamble += '<item>\n'

            children_string = '''</item>
<item>'''.join([child.xml(project_name) for child in self.children])

            appendix += '</item>'

        appendix += '''
    </children>
    </lofar:folder>
        '''
        return preamble + children_string + appendix


def lower_case(boolean):
    return repr(boolean).lower()




class Beam(object):
    def __init__(self, target_source, subband_spec, measurement_type = 'Target'):
        """
        *target_source*        : Instance of class TargetSource
        *subband_spec*         : Either a string with a MoM compatible subband specification,
                                 for example '77..324', or a list of integers, for example
                                 [77, 79, 81]
        *measurement_type*     : 'Target' or 'Calibration'
        """
        self.target_source = target_source
        self.subband_spec  = subband_spec
        self.measurement_type = measurement_type

        if type(subband_spec) == type(''):
            self.subband_spec     = subband_spec
        elif type(subband_spec) == type([]):
            self.subband_spec = ','.join(map(str,subband_spec))
        else:
            raise ValueError('subband specification must be a string or a list of integers; you provided %s instead' % (str(subband_spec),))

        if measurement_type not in ['Target', 'Calibration']:
            raise ValueError('measurement_type %r not in [\'Target\', \'Calibration\']' % measurement_type)







class TiedArrayBeams(object):
    def __init__(self, flyseye    = False,
                 beam_offsets     = None,
                 nr_tab_rings     = 0,
                 tab_ring_size    = 0):
        self.flyseye          = flyseye
        self.beam_offsets     = beam_offsets
        self.nr_tab_rings     = nr_tab_rings
        self.tab_ring_size    = tab_ring_size


    def xml(self):
        output = ('''                        <tiedArrayBeams>
                            <flyseye>%s</flyseye>
                            <nrTabRings>%d</nrTabRings>
                            <tabRingSize>%f</tabRingSize>''' %
                  (lower_case(self.flyseye),
                   self.nr_tab_rings,
                   self.tab_ring_size))
        if len(self.beam_offsets) > 0:
            output += ('''
                            <tiedArrayBeamList>
                                %s
                            </tiedArrayBeamList>''' %
            '\n                                '.join(
                ['<tiedArrayBeam><coherent>true</coherent><angle1>%f</angle1><angle2>%f</angle2></tiedArrayBeam>' % (angle_1, angle_2) for angle_1, angle_2 in self.beam_offsets]))
        else:
            output += '''
                            <tiedArrayBeamList/>'''
        output += '''
                        </tiedArrayBeams>'''
        return output






class Stokes(object):
    r'''
    '''

    def __init__(self, mode, subbands_per_file = 512, number_collapsed_channels = 0, stokes_downsampling_steps = 1, polarizations = 'I'):
        r'''
        pol is either 'I' or 'IQUV'; mode is 'coherent' or 'incoherent'.
        '''
        self.mode                      = mode
        self.subbands_per_file         = subbands_per_file
        self.number_collapsed_channels = number_collapsed_channels
        self.stokes_downsampling_steps = stokes_downsampling_steps
        self.polarizations             = polarizations


    def stokes_suffix(self):
        r'''
        return CS or IS, depending on whether these are coherent or incoherent stokes settings.
        coherent stokes settings also need tied array beams / fly's eye stuff specified.
        '''
        return self.mode[0].upper()+'S'


    def xml(self, project_name):
        r'''
        '''
        return '''
                <subbandsPerFile%(suffix)s>%(subbands_per_file)d</subbandsPerFile%(suffix)s>
                <numberCollapsedChannels%(suffix)s>%(number_collapsed_channels)d</numberCollapsedChannels%(suffix)s>
                <stokesDownsamplingSteps%(suffix)s>%(stokes_downsampling_steps)d</stokesDownsamplingSteps%(suffix)s>
                <which%(suffix)s>%(polarizations)s</which%(suffix)s>
        ''' % {'suffix': self.stokes_suffix(),
               'subbands_per_file': self.subbands_per_file,
               'number_collapsed_channels': self.number_collapsed_channels,
               'stokes_downsampling_steps': self.stokes_downsampling_steps,
               'polarizations': self.polarizations}
               











class BackendProcessing(object):
    def __init__(self,
                 channels_per_subband     = 64,
                 integration_time_seconds = 2,
                 correlated_data          = True,
                 filtered_data            = False,
                 beamformed_data          = False,
                 coherent_stokes_data     = None,
                 incoherent_stokes_data   = None,
                 stokes_integrate_channels = False,
                 coherent_dedispersed_channels = False,
                 tied_array_beams              = None,
                 bypass_pff                    = False,
                 enable_superterp              = False
                 ):
        r'''
        '''
        self.channels_per_subband = channels_per_subband
        self.integration_time_seconds  = int(round(integration_time_seconds))
        self.correlated_data           = correlated_data
        self.filtered_data             = filtered_data
        self.beamformed_data           = beamformed_data
        self.coherent_stokes_data      = coherent_stokes_data
        self.tied_array_beams          = tied_array_beams
        self.incoherent_stokes_data    = incoherent_stokes_data
        self.stokes_integrate_channels = stokes_integrate_channels
        self.coherent_dedispersed_channels = coherent_dedispersed_channels
        self.bypass_pff                = bypass_pff
        self.enable_superterp          = enable_superterp


    def need_beam_observation(self):
        r'''
        '''
        return (self.coherent_stokes_data or self.incoherent_stokes_data or 
                self.filtered_data or self.beamformed_data)



    def instrument_name(self):
        r'''
        '''
        if self.need_beam_observation():
            return 'Beam Observation'
        else:
            return 'Interferometer'



    def default_template(self):
        r'''
        '''
        if self.need_beam_observation():
            return 'BeamObservation'
        else:
            return 'Interferometer'
        
            
    def measurement_type(self):
        if self.need_beam_observation():
            return 'lofar:BFMeasurementType'
        else:
            return 'lofar:UVMeasurementType'


    def measurement_attributes(self):
        if self.need_beam_observation():
            return 'bfMeasurementAttributes'
        else:
            return 'uvMeasurementAttributes'


    def tied_array_beam_list(self):
        if self.need_beam_observation():
            coherent = self.coherent_stokes_data is not None 
            if self.tied_array_beams is not None:
                return self.tied_array_beams.xml()
            else:
                return """
                      <tiedArrayBeamList>
                          <tiedArrayBeam>
                              <coherent>"""+lower_case(coherent)+"""</coherent>
                          </tiedArrayBeam>
                      </tiedArrayBeamList>"""
        else:
            return "                        <tiedArrayBeamList/>"



    def xml(self, project_name):
        r'''
        '''
        def lower_case(bool):
            return repr(bool).lower()
            
        incoherent_stokes = self.incoherent_stokes_data is not None
        coherent_stokes = self.coherent_stokes_data is not None
        flyseye = False
        if coherent_stokes:
            flyseye = self.tied_array_beams.flyseye

            
        output = '''
              <correlatedData>'''+lower_case(self.correlated_data)+'''</correlatedData>
              <filteredData>'''+lower_case(self.filtered_data)+'''</filteredData>
              <beamformedData>'''+lower_case(self.beamformed_data)+'''</beamformedData>
              <coherentStokesData>'''+lower_case(coherent_stokes)+'''</coherentStokesData>
              <incoherentStokesData>'''+lower_case(incoherent_stokes)+'''</incoherentStokesData>'''
        if self.correlated_data:
            output += '''
              <integrationInterval>'''+str(self.integration_time_seconds)+'''</integrationInterval>'''
        output +='''
              <channelsPerSubband>'''+str(self.channels_per_subband)+'''</channelsPerSubband>
              <pencilBeams>
                <flyseye>'''+lower_case(flyseye)+'''</flyseye>
                <pencilBeamList/>
              </pencilBeams>''' + self.tied_array_beam_list()+'''
              <stokes>
                <integrateChannels>'''+lower_case(self.stokes_integrate_channels)+'''</integrateChannels>'''
        if self.incoherent_stokes_data:
            output += '''
'''+self.incoherent_stokes_data.xml(project_name)
        if self.coherent_stokes_data:
            output += '''
'''+self.coherent_stokes_data.xml(project_name)

        output += '''
              </stokes>
              <bypassPff>'''+lower_case(self.bypass_pff)+'''</bypassPff>
              <enableSuperterp>'''+lower_case(self.enable_superterp)+'''</enableSuperterp>
        '''
        return output






class Observation(object):
    def __init__(self, antenna_set, frequency_range, start_date, duration_seconds,
                 stations, clock_mhz, beam_list, backend, name=None, bit_mode=16):
        """
        *antenna_set*            : One of 'LBA_INNER', 'LBA_OUTER', 'HBA_ZERO', 'HBA_ONE',
                                  'HBA_DUAL', or 'HBA_JOINED'
        *frequency_range*        : One of 'LBA_LOW' (10-90/70 MHz), 'LBA_HIGH' (30-90/70 MHz),
                                   'HBA_LOW' (110-190 MHz), 'HBA_MID' (170-230 MHz), or
                                   'HBA_HIGH' (210-250 MHz)
        *start_date*             : UTC time of the beginning of the observation as a tuple
                                   with format (year, month, day, hour, minute, second)
        *duration_seconds*       : Observation duration in seconds
        *stations*               : List of stations, e.g. ['CS001', 'RS205', 'DE601']. An
                                   easy way to generate such a list is through the
                                   utilities.station_list() function.
        *clock_mhz*              : An integer value of 200 or 160.
        *beam_list*              : A list of Beam objects, which contain source/subband
                                   specifications. Provide at least one beam.
        *backend*                : BackendProcessing instance with correlator settings
        *name*                   : Name of the observation. Defaults to name of first target plus antenna set.
        *bit_mode*               : number of bits per sample. Either 4, 8, or 16.
        """
        self.antenna_set              = antenna_set
        self.frequency_range          = frequency_range
        self.duration_seconds         = duration_seconds
        self.stations                 = stations
        self.clock_mhz                = int(clock_mhz)
        self.start_date               = start_date
        self.backend                  = backend
        self.beam_list                = copy.deepcopy(beam_list)
        self.name                     = name
        self.bit_mode                 = bit_mode
        self.validate()
        
        pass



    def validate(self):
        valid_antenna_sets = ['LBA_INNER', 'LBA_OUTER',
                              'HBA_ZERO', 'HBA_ONE',
                              'HBA_DUAL', 'HBA_JOINED',
                              'HBA_DUAL_INNER']
        valid_frequency_ranges = ['LBA_LOW', 'LBA_HIGH', 'HBA_LOW', 'HBA_MID', 'HBA_HIGH']
        valid_clocks           = [160, 200]
        valid_bit_modes        = [4, 8, 16]

        validate_enumeration('Observation antenna set', self.antenna_set, valid_antenna_sets)
        validate_enumeration('Observation frequency range', self.frequency_range, valid_frequency_ranges)
        validate_enumeration('Observation clock frequency', self.clock_mhz, valid_clocks)
        validate_enumeration('Observation observation bit mode', self.bit_mode, valid_bit_modes)

        if type(self.start_date) != type(tuple([])) or len(self.start_date) != 6:
            raise ValueError('Observation start_date must be a tuple of length 6; you provided %s'%(self.start_date,))
        pass



    def xml(self, project_name):
        obs_name=self.beam_list[0].target_source.name+' '+self.antenna_set
        if self.name:
            obs_name = self.name

        now=ephem.Observer().date

        start_date=self.start_date
        end_date=ephem.Date(ephem.Date(self.start_date) + ephem.second*(self.duration_seconds)).tuple()
        rounded_start_date = start_date[:-1]+(int(round(start_date[-1])),)
        rounded_end_date   = end_date[:-1]+(int(round(end_date[-1])),)
        now = now.tuple()[:-1] + (int(round(now.tuple()[-1])),)

        observation_str="""
        <lofar:observation>
          <name>"""+obs_name+"""</name>
          <description>"""+obs_name+"""</description>
          <statusHistory>
            <item index=\"0\">
              <mom2ObjectStatus>
                <name>Brentjens,  Michiel</name>
                <roles>Friend</roles>
                <user id=\"791\"/>
                <timeStamp>"""+mom_timestamp(*now)+"""</timeStamp>
                <mom2:openedStatus/>
              </mom2ObjectStatus>
            </item>
          </statusHistory>
          <currentStatus>
            <mom2:openedStatus/>
          </currentStatus>
          <lofar:observationAttributes>
            <name>"""+obs_name+"""</name>
            <projectName>"""+project_name+"""</projectName>
            <instrument>"""+self.backend.instrument_name()+"""</instrument>
            <defaultTemplate>"""+self.backend.default_template()+"""</defaultTemplate>
            <userSpecification>
              <antenna>"""+mom_antenna_name_from_mac_name(self.antenna_set)+"""</antenna>
              <clock mode=\""""+str(self.clock_mhz)+""" MHz\"/>
              <instrumentFilter>"""+mom_frequency_range(self.frequency_range)+"""</instrumentFilter>
"""+self.backend.xml(project_name)+"""
              <stationSet>Custom</stationSet>
              <stations>
                """+'\n                '.join(['<station name=\"'+n+'\" />' for n in self.stations])+"""
              </stations>
              <timeFrame>UT</timeFrame>
              <startTime>"""+mom_timestamp(*rounded_start_date)+"""</startTime>
              <endTime>"""+mom_timestamp(*rounded_end_date)+"""</endTime>
              <duration>"""+mom_duration(seconds = self.duration_seconds)+"""</duration>
              <numberOfBitsPerSample>"""+str(self.bit_mode)+"""</numberOfBitsPerSample>
            </userSpecification>
            <systemSpecification/>
          </lofar:observationAttributes>
          <children>
        """

        for id,beam in enumerate(self.beam_list):
            observation_str +="""
            <item index=\""""+str(id)+"""\">
              <lofar:measurement xsi:type=\""""+self.backend.measurement_type()+"""\">
                <name>"""+beam.target_source.name+"""</name>
                <description>"""+obs_name+"""</description>
                <statusHistory>
                  <item index=\"0\">
                    <mom2ObjectStatus>
                      <name>Brentjens,  Michiel</name>
                      <roles>Friend</roles>
                      <user id=\"791\"/>
                      <timeStamp>"""+mom_timestamp(*now)+"""</timeStamp>
                      <mom2:openedStatus/>
                    </mom2ObjectStatus>
                  </item>
                </statusHistory>
                <currentStatus>
                  <mom2:openedStatus/>
                </currentStatus>
                <lofar:"""+self.backend.measurement_attributes()+""">
                  <measurementType>"""+beam.measurement_type+"""</measurementType>
                  <specification>
                    <targetName>"""+beam.target_source.name+"""</targetName>
                    <ra>"""+repr(beam.target_source.ra_deg())+"""</ra>
                    <dec>"""+repr(beam.target_source.dec_deg())+"""</dec>
                    <equinox>J2000</equinox>
                    <duration>"""+mom_duration(seconds=self.duration_seconds)+"""</duration>
                    <subbandsSpecification>
                      <bandWidth unit=\"MHz\">48.4375</bandWidth>
                      <centralFrequency unit=\"MHz\">139.21875</centralFrequency>
                      <contiguous>false</contiguous>
                      <subbands>"""+beam.subband_spec+"""</subbands>
                    </subbandsSpecification>"""+self.backend.tied_array_beam_list()+"""
                  </specification>
                </lofar:"""+self.backend.measurement_attributes()+""">
              </lofar:measurement>
            </item>"""
        observation_str+="""
          </children>
        </lofar:observation>
"""
        return observation_str





def as_xml_mom_project(observations, project='2013LOFAROBS'):
    """
    Format a list of *observations* as an XML string that can be
    uploaded to a MoM project with name *project*.
    """
    return """<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<mom2:project xmlns:lofar=\"http://www.astron.nl/MoM2-Lofar\"
    xmlns:mom2=\"http://www.astron.nl/MoM2\"
    xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xsi:schemaLocation=\"http://www.astron.nl/MoM2-Lofar http://lofar.astron.nl:8080/mom3/schemas/LofarMoM2.xsd http://www.astron.nl/MoM2 http://lofar.astron.nl:8080/mom3/schemas/MoM2.xsd \">
    <name>"""+project+"""</name>
    <description>"""+project+"""</description>
    <children>
      <item>"""+'      </item>\n      <item>'.join([obs.xml(project) for obs in observations])+"""
      </item>
    </children>
</mom2:project>
"""
