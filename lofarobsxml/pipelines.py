r'''
The pipelines module contains classes that represent data procesing
pipelines. At this moment, only NDPPP is implemented here, but later
on, this module will also support calibrator/target pipelines and
imaging settings.
'''

from lofarobsxml.observationspecificationbase import ObservationSpecificationBase
from lofarobsxml.utilities import AutoReprBaseClass, typecheck, lower_case, unique, indent
from lofarobsxml.momformats import mom_duration, mom_timestamp, check_mom_topology
import ephem

        
class NDPPP(AutoReprBaseClass):
    r'''
    The demixing- and averaging parameters for NDPPP.

    **Parameters**

    avg_freq_step : int
        How many channels to average.
    
    avg_time_step : int
        How many time steps to average.

    demix_freq_step : int
        Width (in channels) of the window over which demixing is
        done. This must be a multiple of ``avg_freq_step``.

    demix_time_step : int
        Length (in time slots) of the demixing window. This must be a
        multiple of ``avg_time_step``.

    demix_always : None or list of strings
        Sources to always demix. Valid source names are: ['CasA',
        'CygA', 'TauA', 'HydraA', 'VirA', 'HerA'].

    ignore_target : None or bool
        See imagoing cookbook documentation. None implies observatory
        default.

    **Examples**
    
    >>> dmx = NDPPP(16, 2, demix_freq_step=64, demix_time_step=10,
    ...             demix_always=['CygA', 'CasA'])
    >>> dmx
    NDPPP(avg_freq_step   = 16,
          avg_time_step   = 2,
          demix_always    = ['CygA', 'CasA'],
          demix_freq_step = 64,
          demix_if_needed = None,
          demix_time_step = 10,
          ignore_target   = None)
    >>> print(dmx.xml())
    <BLANKLINE>
    <demixingParameters>
      <averagingFreqStep>16</averagingFreqStep>
      <averagingTimeStep>2</averagingTimeStep>
      <demixFreqStep>64</demixFreqStep>
      <demixTimeStep>10</demixTimeStep>
      <demixAlways>[CygA,CasA]</demixAlways>
      <demixIfNeeded></demixIfNeeded>
      <ignoreTarget></ignoreTarget>
    </demixingParameters>

    Of course, several consistency checks are made:
    >>> NDPPP(16, 2, demix_freq_step=64, demix_time_step=5,
    ...                       demix_always=['CygA', 'CasA'])
    Traceback (most recent call last):
    ...
    ValueError: NDPPP.demix_time_step(5) is not a multiple of NDPPP.avg_time_step(2)
    >>> NDPPP(16, 2.5, demix_freq_step=64, demix_time_step=5,
    ...                demix_always=['CygA', 'CasA'])
    Traceback (most recent call last):
    ...
    TypeError: type(NDPPP.avg_time_step)(2.5) not in ['int']

    '''
    def __init__(self,
                 avg_freq_step = 64, avg_time_step = 1,
                 demix_freq_step = 64, demix_time_step = 10,
                 demix_always = None, demix_if_needed = None,
                 ignore_target = None):
        self.avg_freq_step   = avg_freq_step
        self.avg_time_step   = avg_time_step
        self.demix_freq_step = demix_freq_step
        self.demix_time_step = demix_time_step
        self.demix_always    = demix_always
        if type(self.demix_always) is str:
            self.demix_always = [self.demix_always]
        self.demix_if_needed = demix_if_needed
        if type(self.demix_if_needed) is str:
            self.demix_if_needed = [self.demix_if_needed]
        self.ignore_target = ignore_target
        self.validate()



    def validate(self):
        r'''
        Raise a ValueError or TypeError if problems with the
        specification are detected.
        '''
        typecheck(self.avg_freq_step, int, 'NDPPP.avg_freq_step')
        typecheck(self.avg_time_step, int, 'NDPPP.avg_time_step')
        typecheck(self.demix_freq_step, int, 'NDPPP.demix_freq_step')
        typecheck(self.demix_time_step, int, 'NDPPP.demix_time_step')
        typecheck(self.demix_always, [list, type(None)],
                  'NDPPP.demix_always')
        typecheck(self.demix_if_needed, [list, type(None)],
                  'NDPPP.demix_if_needed')
        if self.demix_freq_step % self.avg_freq_step != 0:
            raise ValueError('NDPPP.demix_freq_step(%r) is not a multiple of NDPPP.avg_freq_step(%r)' %
                             (self.demix_freq_step,
                              self.avg_freq_step))
        if self.demix_time_step % self.avg_time_step != 0:
            raise ValueError('NDPPP.demix_time_step(%r) is not a multiple of NDPPP.avg_time_step(%r)' %
                             (self.demix_time_step,
                              self.avg_time_step))
        typecheck(self.ignore_target, [type(None), type(True)],
                  'NDPPP.ignore_target')

    def xml(self):
        r'''
        Produce an xml representation of demixing settings.
        '''
        template = '''
<demixingParameters>
  <averagingFreqStep>%(avg_freq_step)d</averagingFreqStep>
  <averagingTimeStep>%(avg_time_step)d</averagingTimeStep>
  <demixFreqStep>%(demix_freq_step)d</demixFreqStep>
  <demixTimeStep>%(demix_time_step)d</demixTimeStep>
  <demixAlways>%(demix_always)s</demixAlways>
  <demixIfNeeded>%(demix_if_needed)s</demixIfNeeded>
  <ignoreTarget>%(ignore_target)s</ignoreTarget>
</demixingParameters>'''
        args = {'avg_freq_step'   : self.avg_freq_step,
                'avg_time_step'   : self.avg_time_step,
                'demix_freq_step' : self.demix_freq_step,
                'demix_time_step' : self.demix_time_step,
                'demix_always'    : '',
                'demix_if_needed' : '',
                'ignore_target'   : ''}
        if self.demix_always is not None:
            args['demix_always'] = '['+','.join(self.demix_always)+']'
        if self.demix_if_needed is not None:
            args['demix_if_needed'] = '['+','.join(self.demix_if_needed)+']'
        if self.ignore_target is not None:
            args['ignore_target'] = lower_case(self.ignore_target)
        return template % args





class AveragingPipeline(ObservationSpecificationBase):
    r'''
    **Parameters**
    
    processing_nr_tasks should be roughly nr of subbands divided by 3.

    flagging_strategy: 'LBAdefault', 'HBAdefault', or None
        NDPPP flagging strategy.

    initial_status : string
        Either 'opened' or 'approved'


    **Examples**

    >>> from lofarobsxml             import TargetSource, Angle
    >>> from lofarobsxml.backend     import BackendProcessing
    >>> from lofarobsxml.observation import Observation
    >>> from lofarobsxml.beam        import Beam
    >>> target = TargetSource(name      = 'Cyg A',
    ...                       ra_angle  = Angle(hms  = (19, 59, 28.3566)),
    ...                       dec_angle = Angle(sdms = ('+', 40, 44, 2.097)))

    >>> bm = Beam(0, target, '77..324')
    >>> obs = Observation('HBA_DUAL_INNER', 'LBA_LOW', (2013, 10, 20, 18, 5, 0),
    ...                   duration_seconds = 600, name = 'Main observation',
    ...                   stations  = ['CS001', 'RS106', 'DE601'],
    ...                   clock_mhz = 200, beam_list = [bm],
    ...                   backend   = BackendProcessing())

    >>> avg = AveragingPipeline(name = 'Avg Pipeline', ndppp = NDPPP())
    >>> avg.add_input_data_product(obs.children[0])
    >>> obs.append_child(avg)
    >>> avg
    AveragingPipeline(parent               = Observation('Main observation'),
                      children             = None,
                      default_template     = 'Preprocessing Pipeline',
                      duration_s           = None,
                      flagging_strategy    = None,
                      initial_status       = 'opened',
                      input_data           = [Beam(parent            = Observation('Main observation'),
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
                                                  tied_array_beams  = None)],
                      name                 = 'Avg Pipeline',
                      ndppp                = NDPPP(avg_freq_step   = 64,
                                                   avg_time_step   = 1,
                                                   demix_always    = None,
                                                   demix_freq_step = 64,
                                                   demix_if_needed = None,
                                                   demix_time_step = 10,
                                                   ignore_target   = None),
                      predecessor_label    = None,
                      processing_cluster   = 'CEP4',
                      processing_nr_cores  = 2,
                      processing_nr_tasks  = 163,
                      processing_partition = 'cpu',
                      start_date           = None,
                      storage_cluster      = 'CEP4',
                      storage_partition    = '/data/projects')


    >>> print(avg.xml('Project name'))
    <lofar:pipeline xsi:type="lofar:AveragingPipelineType">
      <topology>Main_observat.1.Avg_Pipeline.uv.dps</topology>
      <predecessor_topology>Main_observat</predecessor_topology>
      <name>Avg Pipeline</name>
      <description>Avg Pipeline: "Preprocessing Pipeline"</description>
      <processingCluster>
        <name>CEP4</name>
        <partition>cpu</partition>
        <numberOfTasks>163</numberOfTasks>
        <numberOfCoresPerTask>2</numberOfCoresPerTask>
      </processingCluster>
      <currentStatus>
        <mom2:openedStatus/>
      </currentStatus>
      <averagingPipelineAttributes>
        <defaultTemplate>Preprocessing Pipeline</defaultTemplate>
        <duration></duration>
        <startTime></startTime>
        <endTime></endTime>
        <demixingParameters>
          <averagingFreqStep>64</averagingFreqStep>
          <averagingTimeStep>1</averagingTimeStep>
          <demixFreqStep>64</demixFreqStep>
          <demixTimeStep>10</demixTimeStep>
          <demixAlways></demixAlways>
          <demixIfNeeded></demixIfNeeded>
          <ignoreTarget></ignoreTarget>
        </demixingParameters>
        <flaggingStrategy>HBAdefault</flaggingStrategy>
      </averagingPipelineAttributes>
      <usedDataProducts>
        <item>
          <lofar:uvDataProduct topology="Main_observat.0.Cyg_A.SAP000.uv.dps">
            <name>Main_observat.0.Cyg_A.SAP000.uv.dps</name>
          </lofar:uvDataProduct>
        </item>
      </usedDataProducts>
      <resultDataProducts>
        <item>
          <lofar:uvDataProduct>
            <name>Main_observat.1.Avg_Pipeline.uv.dps</name>
            <topology>Main_observat.1.Avg_Pipeline.uv.dps</topology>
            <status>no_data</status>
            <storageCluster>
              <name>CEP4</name>
              <partition>/data/projects</partition>
            </storageCluster>
          </lofar:uvDataProduct>
        </item>
      </resultDataProducts>
    </lofar:pipeline>

    '''
    def __init__(self, name, ndppp, input_data = None,
                 duration_s = None, start_date = None,
                 flagging_strategy = None,
                 parent   = None, children = None,
                 predecessor_label = None,
                 initial_status='opened',
                 processing_cluster='CEP4',
                 processing_partition=None,
                 processing_nr_tasks = 163,  #This is a sensible default for CEP4 NDPPP pipelines, not for all pipelines
                 processing_nr_cores = 2): #This is a sensible default for CEP4 NDPPP pipelines, not for all pipelines
        super(AveragingPipeline, self).__init__(name=name,
                                                parent=parent,
                                                children=children,
                                                initial_status=initial_status)
        self.ndppp            = ndppp
        self.input_data       = None
        self.duration_s       = duration_s
        self.start_date       = start_date
        self.flagging_strategy = flagging_strategy
        self.default_template = 'Preprocessing Pipeline'
        self.predecessor_label = predecessor_label
        if input_data is not None:
            for item in input_data:
                self.add_input_data_product(item)
        self.processing_cluster = processing_cluster.upper()
        self.storage_cluster = self.processing_cluster
        self.processing_partition = processing_partition
        self.processing_nr_tasks  = processing_nr_tasks
        self.processing_nr_cores  = processing_nr_cores
        if self.processing_partition is None:
            if self.processing_cluster == 'CEP2':
                self.processing_partition = 'cpu' #We also set this one to 'cpu' but it doesn't mean anything
                self.storage_partition = "/data" #This path is now coded in multiple locations, can probably be refactored into the base class?
                raise ValueError('CEP2 has been decommissioned long ago. Please select another cluster.')
            elif self.processing_cluster == 'CEP4':
                self.processing_partition = 'cpu' #We also have 'gpu' but that's not used right now
                self.storage_partition = "/data/projects" #This path is now coded in multiple locations, can probably be refactored into the base class?
        if self.processing_partition is None:
            raise ValueError('No processing partition specified for cluster %s' %
                             self.processing_cluster)
        self.validate()


    def validate(self):
        r'''
        '''
        typecheck(self.ndppp, NDPPP,
                  'AveragingPipeline.NDPPP')
        typecheck(self.predecessor_label, [type(None), str],
                  'AveragingPipeline.predecessor_label')


    def add_input_data_product(self, input_sap):
        r'''
        '''
        if self.input_data is None:
            self.input_data = []
        self.input_data.append(input_sap)



    def predecessor(self):
        r'''
        '''
        if self.predecessor_label is not None:
            return self.predecessor_label

        predecessor_observations = unique(
            [data_set.parent.label()
             for data_set in self.input_data
             if data_set.parent is not None])
        if len(predecessor_observations) != 1:
            raise ValueError('AveragingPipeline: more than one predecessor (%r)' %
                             predecessor_observations)
        return predecessor_observations[0]
        
        

    def xml_prefix(self, project_name = None):
        template ='''<lofar:pipeline xsi:type="lofar:AveragingPipelineType">
  <topology>%(label)s</topology>
  <predecessor_topology>%(predecessor)s</predecessor_topology>
  <name>%(name)s</name>
  <description>%(name)s: "%(default_template)s"</description>
  <processingCluster>
    <name>%(processing_cluster)s</name>
    <partition>%(processing_partition)s</partition>
    <numberOfTasks>%(processing_nr_tasks)s</numberOfTasks>
    <numberOfCoresPerTask>%(processing_nr_cores)s</numberOfCoresPerTask>
  </processingCluster>
  <currentStatus>
    <mom2:%(initial_status)sStatus/>
  </currentStatus>
  <averagingPipelineAttributes>
    <defaultTemplate>%(default_template)s</defaultTemplate>
    <duration>%(duration)s</duration>
    <startTime>%(start_time)s</startTime>
    <endTime></endTime>%(ndppp)s
    <flaggingStrategy>%(flagging_strategy)s</flaggingStrategy>
  </averagingPipelineAttributes>
  <usedDataProducts>%(used_data_products)s
  </usedDataProducts>
  <resultDataProducts>
    <item>
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
  </resultDataProducts>
'''
        used_data_product_template = '''\n<item>
  <lofar:uvDataProduct topology="%(name)s">
    <name>%(name)s</name>
  </lofar:uvDataProduct>
</item>'''
        args = {
            'label'       : check_mom_topology(self.label() + '.uv.dps'),
            'predecessor' : self.predecessor(),
            'name'        : self.name,
            'default_template' : self.default_template,
            'duration'    : '',
            'start_time'  : '',
            'flagging_strategy': self.flagging_strategy,
            'ndppp'       : indent(self.ndppp.xml(), 4),
            'used_data_products' : '',
            'initial_status': self.initial_status,
            'processing_cluster': self.processing_cluster,
            'processing_partition': self.processing_partition,
            'processing_nr_tasks': self.processing_nr_tasks,
            'processing_nr_cores': self.processing_nr_cores,
            'storage_cluster': self.storage_cluster,
            'storage_partition': self.storage_partition
        }
        if self.duration_s is not None:
            args['duration'] = mom_duration(seconds = self.duration_s)
        if self.start_date is not None:
            start_date = ephem.Date(self.start_date).tuple()
            rounded_start_date = start_date[:-1]+(int(round(start_date[-1])),)
            args['start_time'] = mom_timestamp(*rounded_start_date)
        if self.input_data is None:
            raise ValueError('AveragingPipeline.input_data is None!')
        if self.flagging_strategy is None:
            args['flagging_strategy'] = self.input_data[0].parent.antenna_set[0:3].upper()+'default'
        elif self.flagging_strategy in ['HBAdefault', 'LBAdefault']:
            args['flagging_strategy'] = self.flagging_strategy
        else:
            raise ValueError('lofarobsxml.AverigingPipeline: unknown flagging strategy %r' %
                             self.flagging_strategy)
        args['used_data_products'] = indent(
            '\n'.join([
                used_data_product_template % {'name' : sap.data_products_label()} #TODO this needs a proper fix as the topology for the observation has changed
                for sap in self.input_data]),
            4)
        return template % args

    def xml_suffix(self, project_name= None):
        return '</lofar:pipeline>'
