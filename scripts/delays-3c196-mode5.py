from momxml import *
from momxml.pipelines import *
import ephem

target_source = simbad('3C 196')
subbands='50..460'
antenna_set='HBA_DUAL_INNER'
stations = station_list('nl')
frequency_range='HBA_LOW'
clock_mhz=200
channels_per_subband=64
bit_mode=8

observations = []

start_date = ephem.Date('2015-02-12 19:00:01')

for duration_s in [300, 300, 600, 600, 1200, 1200, 1200, 1200, 600, 600, 300, 300]:
    backend = BackendProcessing(
        integration_time_seconds=2,
        correlated_data=True,
        channels_per_subband=channels_per_subband,
        coherent_stokes_data=None,
        incoherent_stokes_data=None)

    obs = Observation(
        name='3C196 mode 5',
        antenna_set=antenna_set,
        frequency_range=frequency_range,
        start_date=start_date.tuple(),
        duration_seconds=duration_s,
        stations=stations,
        clock_mhz=clock_mhz,
        backend=backend,
        bit_mode=bit_mode,
        beam_list=[Beam(
            target_source=target_source,
            subband_spec=subbands)])
    observations.append(obs)
    
    beams = [child for child in obs.children if type(child) is Beam]
    pipeline = AveragingPipeline(
        name='avg',
        ndppp=NDPPP(64, 1, 64, 10, None, None),
        input_data=beams,
        duration_s=duration_s*2,
        start_date=ephem.Date(start_date+(duration_s+300)*ephem.second))
    observations.append(pipeline)
    start_date= ephem.Date(start_date + (duration_s+61)*ephem.second)

val_obs_folder = Folder(name='2015-02-12',
                        description='Mode 5',
                        children=observations,
                        grouping_parent=True,
                        update_folder=False)

    
print xml([val_obs_folder], project='2015LOFAROBS')
