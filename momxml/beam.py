from momxml.observationspecificationbase import ObservationSpecificationBase
from momxml.observationspecificationbase import indent
from momxml.momformats import mom_duration
from momxml.utilities import parse_subband_list

class Beam(ObservationSpecificationBase):
    r'''
    Represents a beam within an Observation. Beams (Sub Array
    Pointings) are one of the possible kinds of children of an
    observation. Pipelines are another kind of observation
    children. To fully generate its XML, a Beam needs information from
    its parent Observation.

    **Parameters**
    
    target_source :  TargetSource
        Contains the name and direction in which to observe.

    subband_spec : string or list of int
        Sub band specification for this beam. Examples: '77..324',
        [100, 200]

    duration_s : None or number
        Duration during which the beam is active. None implies during
        the entire observation.

    measurement_type : 'Target' or 'Calibration'
        Gives some intent for the observation.


    **Examples**

    >>> from momxml import TargetSource, Angle
    >>> from momxml.backend import BackendProcessing
    >>> target = TargetSource(name      = 'Cyg A',
    ...                       ra_angle  = Angle(hms  = (19, 59, 28.3566)),
    ...                       dec_angle = Angle(sdms = ('+', 40, 44, 2.097)))

    >>> bm = Beam(target, '77..324')
    >>> bm
    Beam(parent           = NoneType,
         name             = 'Cyg A',
         measurement_type = 'Target',
         duration_s       = None,
         target_source    = TargetSource(name      = 'Cyg A',
                                         ra_angle  = Angle(shms = ('+', 19, 59, 28.3566)),
                                         dec_angle = Angle(sdms = ('+', 40, 44, 2.097))),
         subband_spec     = '77..324',
         children         = None)
    >>> observation_stub = ObservationSpecificationBase('Observation')
    >>> observation_stub.backend = BackendProcessing()
    >>> observation_stub.clock_mhz = 200
    >>> observation_stub.frequency_range = 'HBA_LOW'
    >>> observation_stub.append_child(bm)
    >>> print bm.xml('Project name')
    <lofar:measurement xsi:type="lofar:UVMeasurementType">
    <name>Cyg A</name>
    <description>Observation</description>
    <topology>Observation.0.Cyg_A</topology>
    <currentStatus>
      <mom2:openedStatus/>
    </currentStatus>
    <lofar:uvMeasurementAttributes>
      <measurementType>Target</measurementType>
      <specification>
        <targetName>Cyg A</targetName>
        <ra>299.8681525</ra>
        <dec>40.733915833333334</dec>
        <equinox>J2000</equinox>
        <duration>PT00S</duration>
        <subbandsSpecification>
          <bandWidth unit="MHz">48.4375</bandWidth>
          <centralFrequency unit="MHz">139.1602</centralFrequency>
          <contiguous>false</contiguous>
          <subbands>77..324</subbands>
        </subbandsSpecification>
      </specification>
    </lofar:uvMeasurementAttributes>
    <resultDataProducts>
      <item>
        <lofar:uvDataProduct>
          <name>Observation.0.Cyg_A.dps</name>
          <topology>Observation.0.Cyg_A.dps</topology>
          <status>no_data</status>
        </lofar:uvDataProduct>
      </item>
    </resultDataProducts>
    </lofar:measurement>
    '''

    def __init__(self, target_source, subband_spec,
                 duration_s = None, measurement_type = 'Target'):
        super(Beam, self).__init__(target_source.name,
                                   parent = None, children = None)
        self.target_source    = target_source
        self.subband_spec     = subband_spec
        self.measurement_type = measurement_type
        self.duration_s       = duration_s

        if type(subband_spec) == type(''):
            self.subband_spec     = subband_spec
        elif type(subband_spec) == type([]):
            self.subband_spec = ','.join([str(sub) for sub in subband_spec])
        else:
            raise ValueError('subband_spec(%r) is not a string list of ints' %
                             subband_spec)

        if measurement_type not in ['Target', 'Calibration']:
            raise ValueError(
                'measurement_type %r not in [\'Target\', \'Calibration\']' %
                measurement_type)



    def xml_prefix(self, project_name, current_date = None):
        backend    = self.parent.backend
        obs_name   = self.target_source.name
        if self.parent.name:
            obs_name = self.parent.name

        duration_s = 0
        if self.duration_s is not None:
            duration_s = int(round(self.duration_s))

        tied_array_beams = ''
        if backend.need_beam_observation():
            tied_array_beams = indent(
                backend.tied_array_beams.xml(project_name),
                amount = 4)

        result_data_products = ''
        if not backend.need_beam_observation():
            result_data_products = '''
<resultDataProducts>
  <item>
    <lofar:uvDataProduct>
      <name>%(label)s</name>
      <topology>%(label)s</topology>
      <status>no_data</status>
    </lofar:uvDataProduct>
  </item>
</resultDataProducts>''' % {'label': self.label()+'.dps'}
        
        sub_bands     = parse_subband_list(self.subband_spec)
        bandwidth_mhz = len(sub_bands)*(self.parent.clock_mhz/1024.0)
        mean_sub_band = sum(sub_bands)/float(len(sub_bands))
        central_frequency_mhz = mean_sub_band*(self.parent.clock_mhz/1024.0)
        if self.parent.frequency_range == 'HBA_LOW':
            central_frequency_mhz += self.parent.clock_mhz/2.0
        if self.parent.frequency_range in ['HBA_MID', 'HBA_HIGH']:
            central_frequency_mhz += self.parent.clock_mhz

        parameters = {
            'backend_measurement_type' : backend.measurement_type(),
            'name'                     : self.target_source.name,
            'description'              : obs_name,
            'topology'                 : self.label(),
            'backend_attributes'       : backend.measurement_attributes(),
            'measurement_type'         : self.measurement_type,
            'target_name'              : self.target_source.name,
            'ra_deg'                   : self.target_source.ra_deg(),
            'dec_deg'                  : self.target_source.dec_deg(),
            'mom_duration'             : mom_duration(seconds = duration_s),
            'bandwidth_mhz'            : bandwidth_mhz,
            'central_frequency_mhz'    : central_frequency_mhz,
            'subband_spec'             : self.subband_spec,
            'tied_array_beams'         : tied_array_beams,
            'result_data_products'     : result_data_products
        }
        prefix_format = '''<lofar:measurement xsi:type=\"%(backend_measurement_type)s\">
<name>%(name)s</name>
<description>%(description)s</description>
<topology>%(topology)s</topology>
<currentStatus>
  <mom2:openedStatus/>
</currentStatus>
<lofar:%(backend_attributes)s>
  <measurementType>%(measurement_type)s</measurementType>
  <specification>
    <targetName>%(target_name)s</targetName>
    <ra>%(ra_deg)r</ra>
    <dec>%(dec_deg)r</dec>
    <equinox>J2000</equinox>
    <duration>%(mom_duration)s</duration>
    <subbandsSpecification>
      <bandWidth unit=\"MHz\">%(bandwidth_mhz).4f</bandWidth>
      <centralFrequency unit=\"MHz\">%(central_frequency_mhz).4f</centralFrequency>
      <contiguous>false</contiguous>
      <subbands>%(subband_spec)s</subbands>
    </subbandsSpecification>%(tied_array_beams)s
  </specification>
</lofar:%(backend_attributes)s>%(result_data_products)s'''

        return prefix_format % parameters

        
    def xml_suffix(self, project_name):
        return '\n</lofar:measurement>'
