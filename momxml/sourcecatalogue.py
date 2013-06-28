from momxml import TargetSource, Angle, simbad
from numpy import exp,pi
from momxml import lofar_sidereal_time, lofar_observer
import ephem


def target_source_from_row(row):
    return TargetSource(name      = row[0][0],
                        ra_angle  = Angle(shms = ('+',)+row[1]),
                        dec_angle = Angle(sdms = row[2]))

class NoSuitableSourceError(RuntimeError):
    pass



class SourceCatalogue:
    def __init__(self):
        self.source_table= {'HBA': [
                [['3C 48', '48']  ,  ( 1, 37, 41.2994), ('+', 33, 9, 35.134)],
                [['3C 147', '147'],  ( 5, 42, 36.1379), ('+', 49, 51, 07.234)],
                [['3C 196', '196'], ( 8, 13, 36.0), ('+', 48, 13,  3.0)],
                [['3C 295', '295'], (14, 11, 20.5), ('+', 52, 12,  10.0)],
                [['3C 380', '380'] , (18, 29, 31.7248), ('+', 48, 44, 46.9515)]
                ],
                            'LBA': [
                [['3C 196', '196'], ( 8, 13, 36.0), ('+', 48, 13,  3.0)],
                [['Cyg A', 'cyg'] , (19, 59, 28.3), ('+', 40, 44,  2.0)]
                
                ]}



        self.pulsar_table = {'HBA': [
            [['PSR B0329+54'], ( 3, 32, 59.368) , ('+', 54, 34, 43.57)],
            [['PSR B0809+74'], ( 8, 14, 59.50)  , ('+', 74, 29,  5.70)],
            [['PSR B1508+55'], (15,  9, 25.6298), ('+', 55, 31, 32.394)],
            [['PSR B2217+47'], (22, 19, 48.139) , ('+', 47, 54, 53.93)]
            ],
                             'LBA': [
            [['PSR B0809+74'], ( 8, 14, 59.50)  , ('+', 74, 29,  5.70)],
            [['PSR B1133+16'], (11, 36,  3.2477), ('+', 15, 51,  4.48)],
            [['PSR B1919+21'], (19, 21, 44.815) , ('+', 21, 53,  2.25)]
                             ]}




    def find_source(self, source_name):
        selection = filter(lambda row: source_name in row[0], self.source_table)
        if len(selection) != 1:
            return simbad(source_name)
            # raise SourceSpecificationError('"'+str(source_name)+'" is not one of the standard sources; choose one of:\n- '+ '\n- '.join([', '.join(map(lambda s: '"'+s+'"',r[0])) for r in self.source_table]))
        return target_source_from_row(selection[0])

        
        
    def closest_to_meridian(self, lst_rad, lba_or_hba, source_table,
                            observer,
                            min_elevation_deg = None,
                            max_elevation_deg = None):
        r'''
        '''
        lst_rad = float(lst_rad)
        lst_complex = exp(1j*(lst_rad+0.0))
        min_dist=2.1
        best_source = None

        elevations = []
        sources    =  source_table[lba_or_hba]
        for source in sources:
            src = ephem.FixedBody()
            src.name = source[0][0]
            src._ra  = Angle(hms  = source[1]).as_rad()
            src._dec = Angle(sdms = source[2]).as_rad()
            src.compute(observer)
            elevations.append(Angle(rad = float(src.alt)).as_deg())

        source_elevation_pairs = sorted(zip(sources, elevations), key=lambda x: x[1])[::-1]
        #print source_elevation_pairs

        min_el = 0.0
        if min_elevation_deg:
            min_el = min_elevation_deg

        max_el = 90.00001
        if max_elevation_deg:
            max_el = max_elevation_deg

        # Select highest source below max elevation and above min elevation
        for source, elevation  in source_elevation_pairs:
            if elevation > min_el and elevation < max_el:
                return target_source_from_row(source)

        raise NoSuitableSourceError('No source between elevations %6.2f deg and %6.2f deg:\n%s' % (min_el, max_el, '\n'.join(['- %12s: %6.2f deg' % (source[0][0], el) for source, el in source_elevation_pairs])))



    
    def cal_source(self, obs_date, lba_or_hba,
                   min_elevation_deg = None,
                   max_elevation_deg = None):
        return self.closest_to_meridian(lofar_sidereal_time(obs_date),
                                        lba_or_hba,
                                        source_table = self.source_table,
                                        min_elevation_deg = min_elevation_deg,
                                        max_elevation_deg = max_elevation_deg,
                                        observer          = lofar_observer(obs_date))


    def psr_source(self, obs_date, lba_or_hba,
                   min_elevation_deg = None,
                   max_elevation_deg = None):
        return self.closest_to_meridian(lofar_sidereal_time(obs_date),
                                        lba_or_hba,
                                        source_table = self.pulsar_table,
                                        min_elevation_deg = min_elevation_deg,
                                        max_elevation_deg = max_elevation_deg,
                                        observer          = lofar_observer(obs_date))
        
