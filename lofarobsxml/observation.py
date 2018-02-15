from lofarobsxml.observationspecificationbase import ObservationSpecificationBase
from lofarobsxml.momformats   import mom_duration, mom_timestamp, mom_frequency_range
from lofarobsxml.momformats   import mom_antenna_name_from_mac_name, check_mom_topology
from lofarobsxml.targetsource import TargetSource
from lofarobsxml.utilities    import validate_enumeration, indent
from math import ceil
import ephem



class Observation(ObservationSpecificationBase):
    def __init__(self, antenna_set, frequency_range, start_date, duration_seconds,
                 stations, clock_mhz, beam_list, backend, name = None, bit_mode=16,
                 allow_tbb=True, allow_aartfaac=True, initial_status='opened'):
        """
        *antenna_set*            : One of 'LBA_INNER', 'LBA_OUTER', 'LBA_SPARSE_ODD',
                                   'LBA_SPARSE_EVEN', 'HBA_ZERO', 'HBA_ONE',
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
        *initial_status*         : status when first imported into MoM. Either 'opened' or 'approved'

    allow_tbb : bool
       If True, allow piggy-back observing with Transient Buffer Boards [TBB].
       Default: True.

    allow_aartfaac : bool
       If True, allow piggy-back observing with AARTFAAC.
       Default: True.

        """
        super(Observation, self).__init__(name = name, parent = None, children = None,
                                          initial_status=initial_status)

        self.antenna_set              = antenna_set
        self.frequency_range          = frequency_range
        self.duration_seconds         = duration_seconds
        self.stations                 = stations
        self.clock_mhz                = int(clock_mhz)
        self.start_date               = start_date
        self.bit_mode                 = bit_mode
        self.allow_aartfaac           = allow_aartfaac
        self.allow_tbb                = allow_tbb
        self.backend                  = backend
        for beam in beam_list:
            self.append_child(beam)
        self.validate()
        pass



    def validate(self):
        valid_antenna_sets = ['LBA_INNER', 'LBA_OUTER',
                              'LBA_SPARSE_ODD', 'LBA_SPARSE_EVEN',
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



    def xml_prefix(self, project_name):
        obs_name = self.children[0].target_source.name+' '+self.antenna_set
        if self.name:
            obs_name = self.name

        now = ephem.Observer().date

        start_date = self.start_date
        end_date = ephem.Date(ephem.Date(self.start_date) + ephem.second*(self.duration_seconds)).tuple()
        rounded_start_date = start_date[:-1]+(int(round(start_date[-1])),)
        rounded_end_date   = end_date[:-1]+(int(round(end_date[-1])),)
        now = now.tuple()[:-1] + (int(round(now.tuple()[-1])),)
        topology = self.label()
        check_mom_topology(topology)
        
        observation_str = '''<lofar:observation>
  <name>'''+obs_name+'''</name>
  <description>'''+obs_name+'''</description>
  <topology>'''+topology+'''</topology>
  <currentStatus>
    <mom2:'''+self.initial_status+'''Status/>
  </currentStatus>
  <lofar:observationAttributes>
    <name>'''+obs_name+'''</name>
    <projectName>'''+project_name+'''</projectName>
    <instrument>'''+self.backend.instrument_name()+'''</instrument>
    <defaultTemplate>'''+self.backend.default_template+'''</defaultTemplate>
    <tbbPiggybackAllowed>'''+str(self.allow_tbb).lower()+'''</tbbPiggybackAllowed>
    <aartfaacPiggybackAllowed>'''+str(self.allow_aartfaac).lower()+'''</aartfaacPiggybackAllowed>
    <userSpecification>
      <antenna>'''+mom_antenna_name_from_mac_name(self.antenna_set)+'''</antenna>
      <clock mode=\"'''+str(self.clock_mhz)+''' MHz\"/>
      <instrumentFilter>'''+mom_frequency_range(self.frequency_range, self.clock_mhz)+'''</instrumentFilter>
'''+indent(self.backend.xml(), 6)+'''      <stationSet>Custom</stationSet>
      <stations>
        '''+'\n        '.join(['<station name=\"'+n+'\" />' for n in self.stations])+'''
      </stations>
      <timeFrame>UT</timeFrame>
      <startTime>'''+mom_timestamp(*rounded_start_date)+'''</startTime>
      <endTime>'''+mom_timestamp(*rounded_end_date)+'''</endTime>
      <duration>'''+mom_duration(seconds = self.duration_seconds)+'''</duration>
      <numberOfBitsPerSample>'''+str(self.bit_mode)+'''</numberOfBitsPerSample>
    </userSpecification>
    <systemSpecification/>
  </lofar:observationAttributes>'''
        return observation_str



    def xml_suffix(self, project_name = None):
        observation_str = '\n</lofar:observation>'
        return observation_str



def xml(items, project='2015LOFAROBS_new', description=None):
    """
    Format a list of *items* as an XML string that can be
    uploaded to a MoM project with name *project*.
    """
    return """<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<lofar:project xmlns:lofar=\"http://www.astron.nl/MoM2-Lofar\"
    xmlns:mom2=\"http://www.astron.nl/MoM2\"
    xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xsi:schemaLocation=\"http://www.astron.nl/MoM2-Lofar http://lofar.astron.nl:8080/mom3/schemas/LofarMoM2.xsd http://www.astron.nl/MoM2 http://lofar.astron.nl:8080/mom3/schemas/MoM2.xsd \">
    <version>1.16</version>
    <name>"""+project+"""</name>
    <description>"""+ (description or project) +"""</description>
    <children>
      <item>\n"""+'      </item>\n      <item>'.join([indent(item.xml(project), 8)
                                                    for child_id, item in enumerate(items)])+"""
      </item>
    </children>
</lofar:project>
"""
