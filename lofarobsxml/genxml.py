import copy
from lofarobsxml.utilities  import parse_subband_list
from lofarobsxml.momformats import mom_antenna_name_from_mac_name as mom_antenna_name
from lofarobsxml.momformats import mom_frequency_range




class Preprocessing(object):
    r'''
    Preprocessing pipeline options. This handles averaging and demixing.

    **Parameters**

    freq_avg_factor: int


    **Examples**

    >>> ndppp = Preprocessing(freq_avg_factor = 16, time_avg_factor = 5,
    ...                       demix_freq_step = 64, demix_time_step = 10)
    >>> ndppp
    Preprocessing(
        freq_avg_factor = 16,
        time_avg_factor = 5,
        demix_freq_step = 64,
        demix_time_step = 10,
        demix_always    = None,
        demix_if_needed = None,
        ignore_target   = None)
    >>> str(ndppp)
    'Demix:16;5;64;10;;;'
    >>> ndppp = Preprocessing(freq_avg_factor = 16, time_avg_factor = 5,
    ...                       demix_freq_step = 64, demix_time_step = 10,
    ...                       demix_always    = ['CasA', 'CygA'],
    ...                       demix_if_needed = ['TauA', 'HydraA', 'VirA', 'HerA'],
    ...                       ignore_target   = False)
    >>> ndppp
    Preprocessing(
        freq_avg_factor = 16,
        time_avg_factor = 5,
        demix_freq_step = 64,
        demix_time_step = 10,
        demix_always    = ['CasA', 'CygA'],
        demix_if_needed = ['TauA', 'HydraA', 'VirA', 'HerA'],
        ignore_target   = False)
    >>> str(ndppp)
    'Demix:16;5;64;10;[CasA,CygA];[TauA,HydraA,VirA,HerA];F'
    '''

    def __init__(self, freq_avg_factor, time_avg_factor,
                 demix_freq_step, demix_time_step,
                 demix_always = None,
                 demix_if_needed = None,
                 ignore_target = None):
        self.freq_avg_factor = freq_avg_factor
        self.time_avg_factor = time_avg_factor
        self.demix_freq_step = demix_freq_step
        self.demix_time_step = demix_time_step
        self.demix_always = demix_always
        self.demix_if_needed = demix_if_needed
        self.ignore_target = ignore_target



    def __repr__(self):
        args = (self.freq_avg_factor,
                self.time_avg_factor,
                self.demix_freq_step,
                self.demix_time_step,
                self.demix_always,
                self.demix_if_needed,
                self.ignore_target)
        return r'''Preprocessing(
    freq_avg_factor = %d,
    time_avg_factor = %d,
    demix_freq_step = %d,
    demix_time_step = %d,
    demix_always    = %r,
    demix_if_needed = %r,
    ignore_target   = %r)''' % args


    def __str__(self):
        line = 'Demix:%(freq_avg_factor)d;%(time_avg_factor)d;%(demix_freq_step)d;%(demix_time_step)d;' % self.__dict__
        if self.demix_always is None:
            line += ';'
        else:
            line += '['+','.join(self.demix_always)+'];'

        if self.demix_if_needed is None:
            line += ';'
        else:
            line += '['+','.join(self.demix_if_needed)+'];'

        if self.ignore_target is not None:
            line += repr(self.ignore_target)[0]

        return line





class Calibration(object):
    r'''
    '''
    def __init__(self, sky_model = None,
                 baselines = None, correlations = None,
                 enable_beam_model = True,
                 solve_parms = None, solve_uv_range = None,
                 strategy_baselines = None,
                 strategy_time_range = None):
        self.sky_model = sky_model
        self.baselines = baselines
        self.correlations = correlations
        self.enable_beam_model = enable_beam_model
        self.solve_parms = solve_parms
        self.solve_uv_range = solve_uv_range
        self.strategy_baselines = strategy_baselines
        self.strategy_time_range = strategy_time_range

    def __str__(self):
        bbs_spec = 'BBS:'
        if self.sky_model is not None:
            bbs_spec += self.sky_model
        bbs_spec += ';'
        if self.baselines is not None:
            bbs_spec += self.baselines
        bbs_spec += ';'
        if self.correlations is not None:
            bbs_spec += self.correlations
        bbs_spec += ';'
        if self.enable_beam_model is not None:
            bbs_spec += repr(self.enable_beam_model)[0].upper()
        bbs_spec += ';'
        if self.solve_parms is not None:
            bbs_spec += self.solve_parms
        bbs_spec += ';'
        if self.solve_uv_range is not None:
            bbs_spec += self.solve_uv_range
        bbs_spec += ';'
        if self.strategy_baselines is not None:
            bbs_spec += self.strategy_baselines
        bbs_spec += ';'
        if self.strategy_time_range is not None:
            bbs_spec += self.strategy_time_range
        return bbs_spec





#class Imaging(object):
#    pass


class Pipeline(object):
    r'''
    '''
    def __init__(self, preprocessing = None, calibration = None, duration_s = None):
        self.preprocessing = preprocessing
        self.calibration = calibration
        self.duration_s = duration_s

    def __repr__(self):
        return ('''Pipeline(
    preprocessing = %r,
    calibration   = %r,
    duration_s    = %r)''' %
                (self.preprocessing, self.calibration, self.duration_s))


    def __str__(self):
        stages = [str(stage) for stage in [self.preprocessing, self.calibration]
                  if stage is not None]
        return '\n'.join(stages)

    def sky_model(self):
        if self.calibration:
            return self.calibration.sky_model
        else:
            return None





class Beam(object):
    r'''
    **Examples**

    >>> from lofarobsxml.angles import Angle
    >>> beam = Beam(name = '3Cwhatever',
    ...             ra  = Angle(rad = 3.6),
    ...             dec = Angle(rad = 1.2),
    ...             subband_spec = '96..105,123..132,143..152,175..184,217..226,238..247,258..267,286..295',
    ...             pipeline     = None)
    >>> beam
    Beam(
        name         = '3Cwhatever',
        ra           = Angle(rad = 3.6),
        dec          = Angle(rad = 1.2),
        subband_spec = '96..105,123..132,143..152,175..184,217..226,238..247,258..267,286..295',
        pipeline     = None)
    >>> str(beam)
    '206.264806;68.754935;3Cwhatever;96..105,123..132,143..152,175..184,217..226,238..247,258..267,286..295;80;F'
    >>> beam.number_of_subbands
    80
    >>> beam = Beam(name = '3Cwhatever',
    ...             ra  = Angle(rad = 3.6),
    ...             dec = Angle(rad = 1.2),
    ...             subband_spec = '96..105,123..132,143..152,175..184,217..226,238..247,258..267,286..295',
    ...             pipeline     = Pipeline(Preprocessing(16, 5, 64, 10),
    ...                                     Calibration(sky_model='3C48'),
    ...                                     duration_s = 120))
    >>> print(str(beam))
    206.264806;68.754935;3Cwhatever;96..105,123..132,143..152,175..184,217..226,238..247,258..267,286..295;80;T;120
    Demix:16;5;64;10;;;
    BBS:3C48;;;T;;;;
    '''
    def __init__(self, name, ra, dec, subband_spec, pipeline=None):
        self.name = name
        self.ra = ra
        self.dec = dec
        self.subband_spec = subband_spec
        self.number_of_subbands = len(parse_subband_list(subband_spec))
        self.pipeline = pipeline


    def __repr__(self):
        args = (self.name, self.ra, self.dec, self.subband_spec, self.pipeline)
        return '''Beam(
    name         = %r,
    ra           = %r,
    dec          = %r,
    subband_spec = %r,
    pipeline     = %r)''' % args



    def __str__(self):
        args = (self.ra.as_deg(), self.dec.as_deg(), self.name,
                self.subband_spec, self.number_of_subbands,
                str(self.pipeline != None)[0])
        beam_spec = '%.6f;%.6f;%s;%s;%d;%s' % args
        if self.pipeline:
            if self.pipeline.duration_s:
                beam_spec += ';%d' % self.pipeline.duration_s
            beam_spec += '\n'
            beam_spec += str(self.pipeline)
        return beam_spec




class ObservationPackage(object):
    r'''

    '''
    def __init__(self, project_name, package_name, description, setup_mode):
        self.project_name = project_name
        self.package_name = package_name
        self.description = description
        self.setup_mode = setup_mode

    def __str__(self):
        return '''
'''



def xml_generator_input_single_set(**kwargs):
    r'''

    **Parameters**

    setup_mode : string
        Calobs, Calbeam, Preprocessing, Calibration.
    number_of_slices : int
        Number of calibrator / target pairs. Irrelevant in case of
        Calbeam observations.

    package_name : string
        Directory into which the observations are stored.

    package_tag : string
        A short string to prepend to all observation and pipeline names.

    package_description : string
        Description to add to this directory.

    create_calibrator_observations : bool
        Set to True if calibrator observations are required, even if
        no specific pipelines are requested.

    antenna_mode : string
        Allowed antenna modes are 'LBA_INNER', 'LBA_OUTER',
        'HBA_ZERO', 'HBA_ONE', 'HBA_DUAL', 'HBA_JOINED',
        'HBA_ZERO_INNER', 'HBA_ONE_INNER', 'HBA_DUAL_INNER'

    clock_mhz : int
        Clock frequency. Either 200 or 160.

    instrument_filter : string
        Instrument filter name. One of 'LBA_LOW', 'LBA_HIGH',
        'HBA_LOW', 'HBA_MID', 'HBA_HIGH'

    bits_per_sample : int
        Number of bits per beamforming sample. 4, 8, or 16.

    integration_time : int
        Number of "seconds" of integration time per correlator sample.

    channels_per_subband : int
        Number of channels per subband at the correlator. Must be a
        power of two. Most common for standard interferometry is 64
        channels per subband.

    stations : list of strings
        The stations to use in the observation. Use the station_list
        function to gnerate this list.

    calibrator_source : string
        Source model name for the calibrator source. Examples are '3C295', '3C196'.

    calibrator_duration_s : int
        Duration of calibrator scans.

    target_duration_s : int
        Duration of target scans.

    subbands_per_image : int
        Number of subbands to combine in one image per imaging pipeline.

    start_date_utc : string
        Start date. Format: 'yyyy-mm-dd hh:mm:ss'

    cal_target_gap_s : int
        Gap between calibrator and target scan in seconds.

    target_cal_gap_s : int
        Gap between target and calibrator scan in seconds.

    calibrator_beam : Beam
        The calibrator beam and associated pipeline specs.

    target_beams : list of Beam
        The target observation beams with associated pipeline specs.

    **Examples**

    >>> from lofarobsxml.angles import Angle
    >>> calibrator_beam = Beam('3C whatever',
    ...                        ra  = Angle(rad = 3.6),
    ...                        dec = Angle(rad = 1.2),
    ...                        subband_spec = '96..105,123..132',
    ...                        pipeline = Pipeline(Preprocessing(64, 10, 64, 10),
    ...                                            Calibration(sky_model='3Cmodel')))
    >>> target_beams    = [Beam('3C interest',
    ...                         ra  = Angle(rad = 2.4),
    ...                         dec = Angle(rad = -0.8),
    ...                         subband_spec = '96..105,123..132',
    ...                         pipeline = Pipeline(Preprocessing(64, 10, 64, 10))),
    ...                    Beam('3C cute',
    ...                         ra  = Angle(rad = 1.6),
    ...                         dec = Angle(rad = +0.4),
    ...                         subband_spec = '96..105,123..132',
    ...                         pipeline = Pipeline(Preprocessing(64, 10, 64, 10)))]
    >>> print(xml_generator_input_single_set(
    ...     setup_mode = 'Calobs',
    ...     number_of_slices = 2,
    ...     package_name     = 'MSSS HBA 2013-02-07',
    ...     package_tag      = 'MSSS20130207',
    ...     package_description = 'Initial MSSS HBA survey fields',
    ...     create_calibrator_observations = True,
    ...     antenna_mode = 'HBA_DUAL_INNER',
    ...     clock_mhz = 200,
    ...     instrument_filter = 'HBA_LOW',
    ...     bits_per_sample = 8,
    ...     integration_time = 2,
    ...     channels_per_subband = 64,
    ...     stations = ['CS001', 'RS310', 'DE605'],
    ...     calibrator_source = '3Cmodel',
    ...     calibrator_duration_s = 60,
    ...     target_duration_s = 420,
    ...     subbands_per_image = 10,
    ...     start_date_utc = '2013-02-07 04:00:01',
    ...     cal_target_gap_s = 60,
    ...     target_cal_gap_s = 4*3600 - 540,
    ...     calibrator_beam = calibrator_beam,
    ...     target_beams = target_beams))
    # setup_mode can be one of Calobs, Calbeam, Preprocessing, Calibration
    setup_mode=Calobs
    number_of_slices=2
    <BLANKLINE>
    packageName=MSSS HBA 2013-02-07
    packageDescription=Initial MSSS HBA survey fields
    packageTag=MSSS20130207
    <BLANKLINE>
    create_calibrator_observations=true
    create_target_cal_beam=false
    create_extra_ncp_beam=false
    antennaMode=HBA Dual Inner
    clock=200 MHz
    instrumentFilter=110-190 MHz
    numberOfBitsPerSample=8
    integrationTime=2
    channelsPerSubband=64
    stationList=CS001,RS310,DE605
    calibratorDuration_s=60
    targetDuration_s=420
    tbbPiggybackAllowed=true
    <BLANKLINE>
    # Imaging parameters
    nrSubbandsPerImage=10
    # the following imaging parameters are optional, if not specified the default value is used for that parameter
    maxBaseline_m=
    fieldOfView_deg=
    weightingScheme=
    robustParameter=
    nrOfIterations=
    cleaningThreshold=
    uvMin_klambda=
    uvMax_klambda=
    stokesToImage=
    <BLANKLINE>
    # startTimeUTC, the start time of the first observation. format: yyyy-MM-dd hh:mm:ss
    # un-comment the startTimeUTC to have the observation start times generated
    startTimeUTC=2013-02-07 04:00:01
    # timeStep's in seconds
    timeStep1=60
    timeStep2=13860
    <BLANKLINE>
    # calibrator beam and calibrator pipeline
    # ra(degrees); dec(degrees); target name; subband list; nrSubbands; create_pipeline;
    # optionally followed by its own 'BBS:' and/or 'Demix:' settings
    # BBS:SkyModel;BBS_baselines;BBS_correlations;BBS_beamModelEnable;BBS_solveParms;BBS_solveUVRange;BBS_strategyBaselines;BBS_strategyTimeRange;
    # Demix:avg freq step; avg time step; demix freq step; demix time step; demix_always; demix_if_needed; ignore_target
    calibratorBeam=
    206.264806;68.754935;3C whatever;96..105,123..132;20;T
    Demix:64;10;64;10;;;
    BBS:3Cmodel;;;T;;;;
    <BLANKLINE>
    # target beams and target pipelines
    # ra(degrees) ;dec(degrees); targetname; subbandList; nrSubbands; create_pipeline;
    # optionally followed by BBS and/or demixing settings
    # BBS:SkyModel;BBS_baselines;BBS_correlations;BBS_beamModelEnable;BBS_solveParms;BBS_solveUVRange;BBS_strategyBaselines;BBS_strategyTimeRange;
    # Demixer:avg freq step; avg time step; demix freq step; demix time step; demix_always; demix_if_needed; ignore_target
    targetBeams=
    137.509871;-45.836624;3C interest;96..105,123..132;20;T
    Demix:64;10;64;10;;;
    91.673247;22.918312;3C cute;96..105,123..132;20;T
    Demix:64;10;64;10;;;
    <BLANKLINE>

    '''

    args                      = copy.deepcopy(kwargs)
    args['create_calibrator_observations'] = \
        str(kwargs['create_calibrator_observations']).lower()
    args['antenna_mode']      = mom_antenna_name(kwargs['antenna_mode'])
    args['instrument_filter'] = mom_frequency_range(kwargs['instrument_filter'], kwargs['clock_mhz'])
    args['stations']          = ','.join(kwargs['stations']).upper()
    args['calibrator_source'] = ''.join(kwargs['calibrator_source'].split())
    args['calibrator_beam_specs'] = str(kwargs['calibrator_beam'])
    args['target_beam_specs']     = '\n'.join([str(target) for target in kwargs['target_beams']])

    template = r'''# setup_mode can be one of Calobs, Calbeam, Preprocessing, Calibration
setup_mode=%(setup_mode)s
number_of_slices=%(number_of_slices)d

packageName=%(package_name)s
packageDescription=%(package_description)s
packageTag=%(package_tag)s

create_calibrator_observations=%(create_calibrator_observations)s
create_target_cal_beam=false
create_extra_ncp_beam=false
antennaMode=%(antenna_mode)s
clock=%(clock_mhz)d MHz
instrumentFilter=%(instrument_filter)s
numberOfBitsPerSample=%(bits_per_sample)d
integrationTime=%(integration_time)d
channelsPerSubband=%(channels_per_subband)d
stationList=%(stations)s
calibratorDuration_s=%(calibrator_duration_s)d
targetDuration_s=%(target_duration_s)d
tbbPiggybackAllowed=true

# Imaging parameters
nrSubbandsPerImage=%(subbands_per_image)d
# the following imaging parameters are optional, if not specified the default value is used for that parameter
maxBaseline_m=
fieldOfView_deg=
weightingScheme=
robustParameter=
nrOfIterations=
cleaningThreshold=
uvMin_klambda=
uvMax_klambda=
stokesToImage=

# startTimeUTC, the start time of the first observation. format: yyyy-MM-dd hh:mm:ss
# un-comment the startTimeUTC to have the observation start times generated
startTimeUTC=%(start_date_utc)s
# timeStep's in seconds
timeStep1=%(cal_target_gap_s)d
timeStep2=%(target_cal_gap_s)d

# calibrator beam and calibrator pipeline
# ra(degrees); dec(degrees); target name; subband list; nrSubbands; create_pipeline;
# optionally followed by its own 'BBS:' and/or 'Demix:' settings
# BBS:SkyModel;BBS_baselines;BBS_correlations;BBS_beamModelEnable;BBS_solveParms;BBS_solveUVRange;BBS_strategyBaselines;BBS_strategyTimeRange;
# Demix:avg freq step; avg time step; demix freq step; demix time step; demix_always; demix_if_needed; ignore_target
calibratorBeam=
%(calibrator_beam_specs)s

# target beams and target pipelines
# ra(degrees) ;dec(degrees); targetname; subbandList; nrSubbands; create_pipeline;
# optionally followed by BBS and/or demixing settings
# BBS:SkyModel;BBS_baselines;BBS_correlations;BBS_beamModelEnable;BBS_solveParms;BBS_solveUVRange;BBS_strategyBaselines;BBS_strategyTimeRange;
# Demixer:avg freq step; avg time step; demix freq step; demix time step; demix_always; demix_if_needed; ignore_target
targetBeams=
%(target_beam_specs)s
'''
    return template % args




def xml_generator_input(project_name,
                        main_folder_name, main_folder_description,
                        xml_input_sets):
    r'''

    **Parameters**

    project_name : string
        Name of the MoM project into which the observations must be
        imported.

    main_folder_name : string
        Name of the MoM folder into which the observations must be
        imported.

    main_folder_description : string
        Description of the root folder.

    xml_input_sets : string or list of strings
        The ascii contents of all individual files.
    '''

    input_list = xml_input_sets
    if type(input_list) == type(''):
        input_list = [input_list]

    return r'''
projectName=%(project_name)s
mainFolderName=%(main_folder_name)s
mainFolderDescription=%(main_folder_description)s

BLOCK

%(inputs)s
''' % {'project_name'    : project_name,
       'main_folder_name': main_folder_name,
       'main_folder_description': main_folder_description,
       'inputs'      : '\n\nBLOCK\n\n'.join(xml_input_sets)}

