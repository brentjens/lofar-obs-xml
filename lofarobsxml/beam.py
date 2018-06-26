from lofarobsxml.observationspecificationbase import ObservationSpecificationBase
from lofarobsxml.momformats import mom_duration, check_mom_topology
from lofarobsxml.utilities import parse_subband_list, indent

class Beam(ObservationSpecificationBase):
    r'''
    Represents a beam within an Observation. Beams (Sub Array
    Pointings) are one of the possible kinds of children of an
    observation. Pipelines are another kind of observation
    children. To fully generate its XML, a Beam needs information from
    its parent Observation.

    **Parameters**
    
    sap_id : int
        SAP_ID of the beam.
    
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

    >>> from lofarobsxml import TargetSource, Angle
    >>> from lofarobsxml.backend import BackendProcessing
    >>> target = TargetSource(name      = 'Cyg A',
    ...                       ra_angle  = Angle(hms  = (19, 59, 28.3566)),
    ...                       dec_angle = Angle(sdms = ('+', 40, 44, 2.097)))

    >>> bm = Beam(0, target, '77..324')
    >>> bm
    Beam(parent            = NoneType,
         children          = None,
         duration_s        = None,
         initial_status    = 'opened',
         measurement_type  = 'Target',
         name              = 'Cyg A',
         sap_id            = 0,
         storage_cluster   = 'CEP4',
         storage_partition = '/data/projects',
         subband_spec      = '77..324',
         target_source     = TargetSource(name      = 'Cyg A',
                                          ra_angle  = Angle(shms = ('+', 19, 59, 28.3566)),
                                          dec_angle = Angle(sdms = ('+', 40, 44, 2.097))),
         tied_array_beams  = None)
    >>> observation_stub = ObservationSpecificationBase('Observation')
    >>> observation_stub.backend = BackendProcessing()
    >>> observation_stub.clock_mhz = 200
    >>> observation_stub.frequency_range = 'HBA_LOW'
    >>> observation_stub.append_child(bm)
    >>> print(bm.xml('Project name'))
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
          <name>Observation.0.Cyg_A.SAP000.uv.dps</name>
          <topology>Observation.0.Cyg_A.SAP000.uv.dps</topology>
          <status>no_data</status>
          <storageCluster>
            <name>CEP4</name>
            <partition>/data/projects</partition>
          </storageCluster>
        </lofar:uvDataProduct>
      </item>
    </resultDataProducts>
    </lofar:measurement>
    '''

    def __init__(self,
                 sap_id,
                 target_source, subband_spec,
                 duration_s=None,
                 tied_array_beams=None,
                 measurement_type='Target',
                 storage_cluster='CEP4',
                 storage_partition=None):
        super(Beam, self).__init__(target_source.name,
                                   parent = None, children = None)
        self.sap_id           = sap_id
        self.target_source    = target_source
        self.subband_spec     = subband_spec
        self.measurement_type = measurement_type
        self.duration_s       = duration_s
        self.tied_array_beams = tied_array_beams

        self.storage_cluster = storage_cluster.upper()
        self.storage_partition = storage_partition
        if self.storage_partition is None:
            if self.storage_cluster == 'CEP2':
                self.storage_partition = '/data'
                raise ValueError('CEP2 has been decommissioned long ago. Please select another cluster.')
            elif self.storage_cluster == 'CEP4':
                self.storage_partition = '/data/projects'
        if self.storage_partition is None:
            raise ValueError('No storage partition specified for cluster %s' %
                             self.storage_cluster)

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

    def data_products_label(self):
        r'''
        Return the name of the data products produced by this beam.
        '''
        return self.label()+'.SAP%03d.uv.dps' % self.sap_id # Quick and dirty fix as this is used in the pipelines.py


    def xml_result_data_products(self, backend, storage_cluster, storage_partition):
        r'''
        Return the xml for the data products produced by this beam.
        '''
        # We don't need this? if not backend.need_beam_observation():
        result = r'''
<resultDataProducts>
'''
        if backend.correlated_data:
            xc_topology = self.label() + '.SAP%03d.uv.dps' % self.sap_id
            check_mom_topology(xc_topology)
            result += r'''  <item>
    <lofar:uvDataProduct>
      <name>%(label)s</name>
      <topology>%(label)s</topology>
      <status>no_data</status>
      <storageCluster>
        <name>%(storage_cluster)s</name>
        <partition>%(storage_partition)s</partition>
      </storageCluster>
    </lofar:uvDataProduct>
  </item>
''' % {'label': xc_topology,
         'storage_cluster': storage_cluster,
         'storage_partition': storage_partition}

        if backend.coherent_stokes_data or backend.incoherent_stokes_data:
            bf_topology = self.label() + '.'
            if backend.coherent_stokes_data:
                bf_topology += 'cs'
            if backend.incoherent_stokes_data:
                bf_topology += 'is'
            check_mom_topology(bf_topology)
            result += r'''  <item>
    <lofar:bfDataProduct>
      <name>%(label)s</name>
      <topology>%(label)s</topology>
      <status>no_data</status>
      <storageCluster>
        <name>%(storage_cluster)s</name>
        <partition>%(storage_partition)s</partition>
      </storageCluster>
    </lofar:bfDataProduct>
  </item>
''' % {'label': bf_topology,
         'storage_cluster': storage_cluster,
         'storage_partition': storage_partition}
        result += r'''</resultDataProducts>'''
        return result

    def xml_prefix(self, project_name, current_date = None):
        backend    = self.parent.backend
        obs_name   = self.target_source.name
        if self.parent.name:
            obs_name = self.parent.name

        duration_s = 0
        if self.duration_s is not None:
            duration_s = int(round(self.duration_s))

        tied_array_beams = ''
        if backend.need_beam_observation() or self.tied_array_beams:
            if self.tied_array_beams is None:
                self.tied_array_beams = backend.tied_array_beams
            tied_array_beams = indent(
                self.tied_array_beams.xml(project_name),
                amount = 4)


        result_data_products = self.xml_result_data_products(backend,
                                                             self.storage_cluster,
                                                             self.storage_partition)
        
        sub_bands     = parse_subband_list(self.subband_spec)
        if len(sub_bands) == 0:
            raise('Empty subband list %r' % self.subband_spec)
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
            'reference_frame'          : self.target_source.reference_frame,
            'mom_duration'             : mom_duration(seconds = duration_s),
            'bandwidth_mhz'            : bandwidth_mhz,
            'central_frequency_mhz'    : central_frequency_mhz,
            'subband_spec'             : self.subband_spec,
            'tied_array_beams'         : tied_array_beams,
            'result_data_products'     : result_data_products,
            'initial_status'           : self.parent.initial_status,
        }
        prefix_format = '''<lofar:measurement xsi:type=\"%(backend_measurement_type)s\">
<name>%(name)s</name>
<description>%(description)s</description>
<topology>%(topology)s</topology>
<currentStatus>
  <mom2:%(initial_status)sStatus/>
</currentStatus>
<lofar:%(backend_attributes)s>
  <measurementType>%(measurement_type)s</measurementType>
  <specification>
    <targetName>%(target_name)s</targetName>
    <ra>%(ra_deg)r</ra>
    <dec>%(dec_deg)r</dec>
    <equinox>%(reference_frame)s</equinox>
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
