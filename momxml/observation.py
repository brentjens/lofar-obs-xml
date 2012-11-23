from momformats   import *
from targetsource import *
from utilities    import *
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



class Observation(object):
    def __init__(self, antenna_set, frequency_range, start_date, duration_seconds, stations, clock_mhz, beam_list, integration_time_seconds=2, channels_per_subband=64, name=None, bit_mode=16):
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
        *integration_time_seconds: Correlator integration time in seconds. Default is 2
        *channels_per_subband*   : Number of channels per subband. Default is 64
        *name*                   : Name of the observation. Defaults to name of first target plus antenna set.
        *bit_mode*               : number of bits per sample. Either 4, 8, or 16.
        """
        self.antenna_set              = antenna_set
        self.frequency_range          = frequency_range
        self.duration_seconds         = duration_seconds
        self.stations                 = stations
        self.clock_mhz                = int(clock_mhz)
        self.start_date               = start_date
        self.integration_time_seconds = int(round(integration_time_seconds))
        self.channels_per_subband     = channels_per_subband
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
            <instrument>Interferometer</instrument>
            <userSpecification>
              <correlatedData>true</correlatedData>
              <filteredData>false</filteredData>
              <beamformedData>false</beamformedData>
              <coherentStokesData>false</coherentStokesData>
              <incoherentStokesData>false</incoherentStokesData>
              <antenna>"""+mom_antenna_name_from_mac_name(self.antenna_set)+"""</antenna>
              <clock mode=\""""+str(self.clock_mhz)+""" MHz\"/>
              <instrumentFilter>"""+mom_frequency_range(self.frequency_range)+"""</instrumentFilter>
              <integrationInterval>"""+str(self.integration_time_seconds)+"""</integrationInterval>
              <channelsPerSubband>"""+str(self.channels_per_subband)+"""</channelsPerSubband>
              <coherentDedisperseChannels>false</coherentDedisperseChannels>
              <pencilBeams>
                <flyseye>false</flyseye>
                <pencilBeamList/>
              </pencilBeams>
              <tiedArrayBeams>
                  <flyseye>false</flyseye>
                  <tiedArrayBeamList/>
              </tiedArrayBeams>

              <stokes>
                <integrateChannels>false</integrateChannels>
              </stokes>
              <stationSet>Custom</stationSet>
              <stations>
                """+'\n                '.join(['<station name=\"'+n+'\" />' for n in self.stations])+"""
              </stations>
              <timeFrame>UT</timeFrame>
              <startTime>"""+mom_timestamp(*rounded_start_date)+"""</startTime>
              <endTime>"""+mom_timestamp(*rounded_end_date)+"""</endTime>
              <duration>"""+mom_duration(seconds = self.duration_seconds)+"""</duration>
              <bypassPff>false</bypassPff>
              <enableSuperterp>false</enableSuperterp>
              <numberOfBitsPerSample>"""+str(self.bit_mode)+"""</numberOfBitsPerSample>
            </userSpecification>
            <systemSpecification>
              <correlatedData>true</correlatedData>
              <filteredData>false</filteredData>
              <beamformedData>false</beamformedData>
              <coherentStokesData>false</coherentStokesData>
              <incoherentStokesData>false</incoherentStokesData>
              <pencilBeams>
                <flyseye>false</flyseye>
                <pencilBeamList/>
              </pencilBeams>
              <tiedArrayBeams>
                  <flyseye>false</flyseye>
                  <tiedArrayBeamList/>
              </tiedArrayBeams>
              <stokes>
                <integrateChannels>false</integrateChannels>
              </stokes>
              <stations/>
              <bypassPff>false</bypassPff>
              <enableSuperterp>false</enableSuperterp>
            </systemSpecification>
          </lofar:observationAttributes>
          <children>
        """

        for id,beam in enumerate(self.beam_list):
            observation_str +="""
            <item index=\""""+str(id)+"""\">
              <lofar:measurement xsi:type=\"lofar:UVMeasurementType\">
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
                <lofar:uvMeasurementAttributes>
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
                    </subbandsSpecification>
                    <tiedArrayBeams>
                        <flyseye>false</flyseye>
                        <tiedArrayBeamList/>
                    </tiedArrayBeams>
                  </specification>
                </lofar:uvMeasurementAttributes>
              </lofar:measurement>
            </item>"""
        observation_str+="""
          </children>
        </lofar:observation>
"""
        return observation_str





def as_xml_mom_project(observations, project='2012LOFAROBS'):
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
