from momxml import TargetSource, Angle, simbad
from numpy import exp,pi
from momxml import lofar_sidereal_time

def target_source_from_row(row):
    return TargetSource(name      = row[0][0],
                        ra_angle  = Angle(shms = ('+',)+row[1]),
                        dec_angle = Angle(sdms = row[2]))


class SourceCatalogue:
    def __init__(self):
        self.source_table= {'HBA': [
                [['3C 48', '48']  ,  ( 1, 37, 41.2994), ('+', 33, 9, 35.134)],
                [['3C 147', '147'],  ( 5, 42, 36.1379), ('+', 49, 51, 07.234)],
                #[['3C 123', '123'], ( 4, 37,  4.0), ('+', 29, 40, 14.0)],
                [['3C 196', '196'], ( 8, 13, 36.0), ('+', 48, 13,  3.0)],
                #[['Vir A', 'vir'] , (12, 30, 49.4), ('+', 12, 23, 28.0)],
                [['3C 295', '295'], (14, 11, 20.6), ('+', 52, 12,  9.0)],
                #[['Her A', 'her'] , (16, 51, 08.1), ('+',  4, 59, 33.0)],
                #[['Cyg A', 'cyg'] , (19, 59, 28.3), ('+', 40, 44,  2.0)],
                [['3C 380', '380'] , (18, 29, 31.7248), ('+', 48, 44, 46.9515)]
                #[['Cas A', 'cas'] , (23, 23, 24.0), ('+', 58, 48, 54.0)]
                ],
                            'LBA': [
                [['3C 196', '196'], ( 8, 13, 36.0), ('+', 48, 13,  3.0)],
                [['Cyg A', 'cyg'] , (19, 59, 28.3), ('+', 40, 44,  2.0)]
                
                ]}


    def find_source(self, source_name):
        selection = filter(lambda row: source_name in row[0], self.source_table)
        if len(selection) != 1:
            return simbad(source_name)
            # raise SourceSpecificationError('"'+str(source_name)+'" is not one of the standard sources; choose one of:\n- '+ '\n- '.join([', '.join(map(lambda s: '"'+s+'"',r[0])) for r in self.source_table]))
        return target_source_from_row(selection[0])

        
        
    def closest_to_meridian(self, lst_rad, lba_or_hba):
        r'''
        '''
        lst_rad = float(lst_rad)
        lst_complex = exp(1j*(lst_rad+0.0))
        min_dist=2.1
        best_source = None
        for source in self.source_table[lba_or_hba]:
            ra = source[1]
            ra_rad = (ra[0]+ra[1]/60.0 + ra[2]/3600.0)*pi/12.0
            ra_complex = exp(1j*ra_rad)
            dist = abs(lst_complex - ra_complex)
            if dist < min_dist:
                best_source = source
                min_dist    = dist
                pass
            pass
        return target_source_from_row(best_source)

    
    def cal_source(self, obs_date, lba_or_hba):
        return self.closest_to_meridian(lofar_sidereal_time(obs_date), lba_or_hba)
