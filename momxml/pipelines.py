r'''
The pipelines module contains classes that represent data procesing
pipelines. At this moment, only NDPPP is implemented here, but later
on, this module will also support calibrator/target pipelines and
imaging settings.
'''

from momxml.observationspecificationbase import ObservationSpecificationBase
from momxml.utilities import AutoReprBaseClass, typecheck, lower_case


        
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
          demix_freq_step = 64,
          ignore_target   = None,
          demix_time_step = 10,
          demix_if_needed = None,
          demix_always    = ['CygA', 'CasA'])
    >>> print dmx.xml()
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
        template = '''<demixingParameters>
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


#class NDPPP(ObservationSpecificationBase):
#    r'''
#    '''
#    #def __init__(self, 
