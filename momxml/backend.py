from momxml.observationspecificationbase import ObservationSpecificationBase
from momxml.utilities import lower_case


class TiedArrayBeams(ObservationSpecificationBase):
    r'''
    Description of Tied Array Beam (TAB) settings.

    **Parameters**

    flyseye : bool
        If True, store data streams from each station individually.

    beam_offsets : list of pairs of float
        The offsets of the phase centres of the TABs in $lm$
        coordinates in a SIN projection towards the pointing centre of
        the stations. *Units are unclear to me!*

    nr_tab_rings : int
        Alternatively, one can specify with how many rings one wants
        to tile the beam.
    
    tab_ring_size : float
        Distance between TAB rings. *Units are unclear to me*

    **Examples**
    
    >>> tab = TiedArrayBeams()
    >>> tab
    TiedArrayBeams(parent        = NoneType,
                   nr_tab_rings  = 0,
                   name          = 'TAB',
                   flyseye       = False,
                   beam_offsets  = None,
                   tab_ring_size = 0,
                   children      = None)
    >>> print(tab.xml('Project Name'))
    <BLANKLINE>
    <tiedArrayBeams>
      <flyseye>false</flyseye>
      <nrTabRings>0</nrTabRings>
      <tabRingSize>0.000000</tabRingSize>
      <tiedArrayBeamList/>
    </tiedArrayBeams>

    >>> tab_fe = TiedArrayBeams(flyseye      = True,
    ...                         beam_offsets = [(0.0, 0.0), (0.1, -0.05)])
    >>> tab_fe
    TiedArrayBeams(parent        = NoneType,
                   nr_tab_rings  = 0,
                   name          = 'TAB',
                   flyseye       = True,
                   beam_offsets  = [(0.0, 0.0), (0.1, -0.05)],
                   tab_ring_size = 0,
                   children      = None)
    >>> print(tab_fe.xml('Project Name'))
    <BLANKLINE>
    <tiedArrayBeams>
      <flyseye>true</flyseye>
      <nrTabRings>0</nrTabRings>
      <tabRingSize>0.000000</tabRingSize>
      <tiedArrayBeamList>
        <tiedArrayBeam><coherent>true</coherent><angle1>0.000000</angle1><angle2>0.000000</angle2></tiedArrayBeam>
        <tiedArrayBeam><coherent>true</coherent><angle1>0.100000</angle1><angle2>-0.050000</angle2></tiedArrayBeam>
      </tiedArrayBeamList>
    </tiedArrayBeams>
    '''
    def __init__(self, flyseye    = False,
                 beam_offsets     = None,
                 nr_tab_rings     = 0,
                 tab_ring_size    = 0):
        super(TiedArrayBeams, self).__init__(name   = 'TAB',
                                             parent = None, children = None)
        self.flyseye          = flyseye
        self.beam_offsets     = beam_offsets
        self.nr_tab_rings     = nr_tab_rings
        self.tab_ring_size    = tab_ring_size


    def xml_prefix(self, project_name = None):
        output = ('''
<tiedArrayBeams>
  <flyseye>%s</flyseye>
  <nrTabRings>%d</nrTabRings>
  <tabRingSize>%f</tabRingSize>''' %
                  (lower_case(self.flyseye),
                   self.nr_tab_rings,
                   self.tab_ring_size))
        if self.beam_offsets and len(self.beam_offsets) > 0:
            output += ('''
  <tiedArrayBeamList>
    %s
  </tiedArrayBeamList>''' %
                       '\n    '.join(
                           ['<tiedArrayBeam><coherent>true</coherent><angle1>%f</angle1><angle2>%f</angle2></tiedArrayBeam>'
        % (angle_1, angle_2)
                            for angle_1, angle_2 in self.beam_offsets]))
        else:
            output += '''
  <tiedArrayBeamList/>'''
        return output


    def xml_suffix(self, project_name = None):
        return '\n</tiedArrayBeams>'









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


    def xml(self, project_name, child_id = None, parent_label = None):
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
        if self.tied_array_beams  is None:
            self.tied_array_beams = TiedArrayBeams()
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


    def xml(self, project_name, child_id=None, parent_label=None):
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
        output += '''
              <channelsPerSubband>'''+str(self.channels_per_subband)+'''</channelsPerSubband>
              <pencilBeams>
                <flyseye>'''+lower_case(flyseye)+'''</flyseye>
                <pencilBeamList/>
              </pencilBeams>''' + self.tied_array_beams.xml(project_name)+'''
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
