from targetsource import *
from numpy import exp,pi


class SourceCatalogue:
    def __init__(self):
        self.source_table= [
            [['3C 123', '123'], ( 4, 37,  4.0), ('+', 29, 40, 14.0)],
            [['3C 196', '196'], ( 8, 13, 36.0), ('+', 48, 13,  3.0)],
            [['Vir A', 'vir'] , (12, 30, 49.4), ('+', 12, 23, 28.0)],
            [['Her A', 'her'] , (16, 51, 08.1), ('+',  4, 59, 33.0)],
            [['Cyg A', 'cyg'] , (19, 59, 28.3), ('+', 40, 44,  2.0)],
            [['Cas A', 'cas'] , (23, 23, 24.0), ('+', 58, 48, 54.0)]
            ]
        pass

    def target_source_from_row(self, row):
        return TargetSource(name      = row[0][0],
                            ra_angle  = Angle(shms = ('+',)+row[1]),
                            dec_angle = Angle(sdms = row[2]))


    def find_source(self, source_name):
        selection = filter(lambda row: source_name in row[0], self.source_table)
        if len(selection) != 1:
            raise SourceSpecificationError('"'+str(source_name)+'" is not one of the standard sources; choose one of:\n- '+ '\n- '.join([', '.join(map(lambda s: '"'+s+'"',r[0])) for r in self.source_table]))
        return self.target_source_from_row(selection[0])

    
    def closest_to_meridian(self, lst_rad):
        lst_complex = exp(1j*(lst_rad+0.0))
        min_dist=2.1
        best_source = None
        for source in self.source_table:
            ra = source[1]
            ra_rad = (ra[0]+ra[1]/60.0 + ra[2]/3600.0)*pi/12.0
            ra_complex = exp(1j*ra_rad)
            dist = abs(lst_complex - ra_complex)
            if dist < min_dist:
                best_source = source
                min_dist    = dist
                pass
            pass
        return self.target_source_from_row(best_source)


