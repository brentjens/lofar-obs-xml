__version__ = '1.1-rc1'

from momxml.angles    import signum, sign_char, int_from_sign_char, Angle

from momxml.utilities import unique, flatten_list, lofar_sidereal_time
from momxml.utilities import station_list, validate_enumeration, next_date_with_lofar_lst
from momxml.utilities import lofar_observer, next_sunrise, next_sunset
from momxml.utilities import exclude_conflicting_eu_stations, exclude_conflicting_nl_stations
from momxml.utilities import InvalidStationSetError

from momxml.targetsource    import SourceSpecificationError, NoSimbadCoordinatesError
from momxml.targetsource    import TargetSource, simbad
from momxml.sourcecatalogue import SourceCatalogue, NoSuitableSourceError
from momxml.observation     import Folder, Beam, Stokes, BackendProcessing, TiedArrayBeams
from momxml.observation     import Observation, as_xml_mom_project

import ephem
