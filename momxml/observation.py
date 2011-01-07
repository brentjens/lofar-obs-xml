from momformats   import *
from targetsource import *
from utilities    import *
import ephem


class Observation:
    def __init__(self, target_source, antenna_set, frequency_range, start_date, duration_seconds, station_list, clock_mhz, subband_spec, channels_per_subband=64):
        """
        *target_source*    : Instance of class TargetSource
        *antenna_set*      : One of 'LBA_INNER', 'LBA_OUTER', 'HBA_ZERO', 'HBA_ONE',
                             'HBA_DUAL', or 'HBA_JOINED'
        *frequency_range*  : One of 'LBA_LOW' (10-90/70 MHz), 'LBA_HIGH' (30-90/70 MHz),
                             'HBA_LOW' (110-190 MHz), 'HBA_MID' (170-230 MHz), or
                             'HBA_HIGH' (210-250 MHz)
        *start_date*       : UTC time of the beginning of the observation as a tuple
                             with format (year, month, day, hour, minute, second)
        *duration_seconds* : Observation duration in seconds
        *station_list*     : List of stations, e.g. ['CS001', 'RS205', 'DE601']. An
                             easy way to generate such a list is through the
                             utilities.get_station_list() function.
        *clock_mhz*        : An integer value of 200 or 160.
        *subband_spec*     : Either a string with a MoM compatible subband specification,
                             for example '77..324', or a list of integers, for example
                             [77, 79, 81]
        """
        self.target_source    = target_source
        self.antenna_set       = antenna_set
        self.frequency_range  = frequency_range
        self.duration_seconds = duration_seconds
        self.station_list     = station_list
        self.clock_mhz        = int(clock_mhz)
        self.start_date       = start_date
        self.channels_per_subband=channels_per_subband
        if type(subband_spec) == type(''):
            self.subband_spec     = subband_spec
        elif type(subband_spec) == type([]):
            self.subband_spec = ','.join(map(str,subband_spec))
        else:
            raise ValueError('subband specification must be a string or a list of integers; you provided %s instead' % (str(subband_spec),))
        self.validate()
        pass



    def validate(self):
        valid_antenna_sets = ['LBA_INNER', 'LBA_OUTER',
                              'HBA_ZERO', 'HBA_ONE',
                              'HBA_DUAL', 'HBA_JOINED']
        valid_frequency_ranges = ['LBA_LOW', 'LBA_HIGH', 'HBA_LOW', 'HBA_MID', 'HBA_HIGH']
        valid_clocks           = [160, 200]

        validate_enumeration('Observation antenna set', self.antenna_set, valid_antenna_sets)
        validate_enumeration('Observation frequency range', self.frequency_range, valid_frequency_ranges)
        validate_enumeration('Observation clock frequency', self.clock_mhz, valid_clocks)

        if type(self.start_date) != type(tuple([])) or len(self.start_date) != 6:
            raise ValueError('Observation start_date must be a tuple of length 6; you provided %s'%(self.start_date,))
        pass



    def __str__(self):
        obs_name=self.target_source.name+' '+self.antenna_set
        now=ephem.Observer().date
        return """
        <lofar:observation>
          <name>"""+obs_name+"""</name>
          <description>"""+obs_name+"""</description>
          <statusHistory>
            <item index=\"0\">
              <mom2ObjectStatus>
                <name>Brentjens,  Michiel</name>
                <roles>Friend</roles>
                <user id=\"791\"/>
                <timeStamp>"""+mom_timestamp(*now.tuple())+"""</timeStamp>
                <mom2:openedStatus/>
              </mom2ObjectStatus>
            </item>
          </statusHistory>
          <currentStatus>
            <mom2:openedStatus/>
          </currentStatus>
          <lofar:observationAttributes>
            <name>"""+obs_name+"""</name>
            <projectName>LOFAROPS</projectName>
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
              <integrationInterval>1</integrationInterval>
              <channelsPerSubband>"""+str(self.channels_per_subband)+"""</channelsPerSubband>
              <pencilBeams>
                <flyseye>false</flyseye>
                <pencilBeamList/>
              </pencilBeams>
              <stokes>
                <integrateChannels>false</integrateChannels>
              </stokes>
              <stationSet>Custom</stationSet>
              <stations>
                """+'\n                '.join(['<station name=\"'+n+'\" />' for n in self.station_list])+"""
              </stations>
              <startTime>"""+mom_timestamp(*self.start_date)+"""</startTime>
              <endTime>"""+mom_timestamp(*ephem.Date(ephem.Date(self.start_date)+ephem.second*(self.duration_seconds+0.0001)).tuple())+"""</endTime>
              <duration>"""+mom_duration(seconds=self.duration_seconds)+"""</duration>
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
              <stokes>
                <integrateChannels>false</integrateChannels>
              </stokes>
              <stations/>
            </systemSpecification>
          </lofar:observationAttributes>
          <children>
            <item index=\"0\">
              <lofar:measurement xsi:type=\"lofar:UVMeasurementType\">
                <name>"""+self.target_source.name+"""</name>
                <description>"""+obs_name+"""</description>
                <statusHistory>
                  <item index=\"0\">
                    <mom2ObjectStatus>
                      <name>Brentjens,  Michiel</name>
                      <roles>Friend</roles>
                      <user id=\"791\"/>
                      <timeStamp>"""+mom_timestamp(*now.tuple())+"""</timeStamp>
                      <mom2:openedStatus/>
                    </mom2ObjectStatus>
                  </item>
                </statusHistory>
                <currentStatus>
                  <mom2:openedStatus/>
                </currentStatus>
                <lofar:uvMeasurementAttributes>
                  <measurementType>Target</measurementType>
                  <specification>
                    <targetName>"""+self.target_source.name+"""</targetName>
                    <ra>"""+repr(self.target_source.ra_deg())+"""</ra>
                    <dec>"""+repr(self.target_source.dec_deg())+"""</dec>
                    <equinox>J2000</equinox>
                    <duration>"""+mom_duration(seconds=self.duration_seconds)+"""</duration>
                    <subbandsSpecification>
                      <bandWidth unit=\"MHz\">48.4375</bandWidth>
                      <centralFrequency unit=\"MHz\">139.21875</centralFrequency>
                      <contiguous>true</contiguous>
                      <subbands>"""+self.subband_spec+"""</subbands>
                    </subbandsSpecification>
                  </specification>
                </lofar:uvMeasurementAttributes>
              </lofar:measurement>
            </item>
          </children>
        </lofar:observation>
"""





def as_xml_mom_project(observations, project='LOFAROPS'):
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
      <item>"""+'      </item>\n      <item>'.join(map(str, observations))+"""
      </item>
    </children>
</mom2:project>
"""


