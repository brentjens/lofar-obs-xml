from momformats import *
from targetsource import *
import ephem


class Observation:
    def __init__(self, target_source, antennaset, frequency_range, start_date, duration_seconds, station_list, clock_mhz, subband_spec):
        """
        """
        self.target_source    = target_source
        self.antennaset       = antennaset
        self.frequency_range  = frequency_range
        self.duration_seconds = duration_seconds
        self.station_list     = station_list
        self.clock_mhz        = clock_mhz
        self.start_date       = start_date
        self.subband_spec     = subband_spec
        pass

    def __str__(self):
        obs_name=self.target_source.name+' '+self.antennaset
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
              <antenna>"""+mom_antenna_name_from_mac_name(self.antennaset)+"""</antenna>
              <clock mode=\""""+str(self.clock_mhz)+""" MHz\"/>
              <instrumentFilter>"""+mom_frequency_range(self.frequency_range)+"""</instrumentFilter>
              <integrationInterval>1</integrationInterval>
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
              <endTime>"""+mom_timestamp(*ephem.Date(ephem.Date(self.start_date)+ephem.second*self.duration_seconds).tuple())+"""</endTime>
              <duration>"""+str(self.duration_seconds)+"""</duration>
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





def as_xml_mom_project(observations):
    """
    Format a list of *observations* as an XML string that can be
    uploaded to MoM.
    """
    return """
<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<mom2:project xmlns:lofar=\"http://www.astron.nl/MoM2-Lofar\"
    xmlns:mom2=\"http://www.astron.nl/MoM2\"
    xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xsi:schemaLocation=\"http://www.astron.nl/MoM2-Lofar http://lofar.astron.nl:8080/mom3/schemas/LofarMoM2.xsd http://www.astron.nl/MoM2 http://lofar.astron.nl:8080/mom3/schemas/MoM2.xsd \">
    <name>LOFAROPS</name>
    <description>LOFAROPS</description>
    <children>
      <item>"""+'      </item>\n      <item>'.join(map(str, observations))+"""
      </item>
    </children>
</mom2:project>
"""


