__version__ = '1.8-rc2'

from momxml.angles    import signum, sign_char, int_from_sign_char, Angle

from momxml.utilities import flatten_list, lofar_sidereal_time
from momxml.utilities import station_list, validate_enumeration, next_date_with_lofar_lst
from momxml.utilities import lofar_observer, next_sunrise, next_sunset
from momxml.utilities import exclude_conflicting_eu_stations, exclude_conflicting_nl_stations
from momxml.utilities import InvalidStationSetError
from momxml.utilities import lm_from_radec, radec_from_lm, rotate_lm_CCW
from momxml.utilities import parse_subband_list, lower_case

from momxml.targetsource    import SourceSpecificationError, NoSimbadCoordinatesError
from momxml.targetsource    import TargetSource, simbad
from momxml.sourcecatalogue import SourceCatalogue, NoSuitableSourceError
from momxml.folder          import Folder
from momxml.beam            import Beam
from momxml.backend         import Stokes, BackendProcessing, TiedArrayBeams
from momxml.observation     import Observation, xml

import ephem
