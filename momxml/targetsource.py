class SourceSpecificationError (StandardError):
    pass


class TargetSource:
    def __init__(self, name='', ra_hms=(0,0,0), dec_sdms=('+',0,0,0), ra_deg=None, dec_deg=None):
        """
        *name*     : string containing the name of the source
        
        *ra_hms*   : J2000 right ascension as a sequence of at most
                     three numbers (hours, minutes, seconds)

        *dec_sdms* : J2000 declination as a sequence of at most four
                     elements (sign, degrees, minutes, seconds). The
                     sign one of the single element strings '+' or
                     '-'.
        """
        self.name     = name
        self.ra_hms   = ra_hms
        self.ra_deg_val   = ra_deg
        self.dec_sdms = dec_sdms
        self.dec_deg_val  = dec_deg
        self.validate_and_normalize()
        pass


    def validate_and_normalize(self):
        """
        Validates type and contents of data members. Raises a
        SourceSpecificationError in case of problems.  If all is well,
        it returns a reference to self. If necessary, it pads ra_hms
        and dec_sdms with zeroes until their lengths are 3 and 4, respectively.
        """
        if type(self.name) == type(u''):
            raise SourceSpecificationError('Source name may not be a unicode string.')
        if type(self.name) != type(''):
            raise SourceSpecificationError('Source name must be a string. You specified %s' % (str(self.name),))
        
        if len(self.ra_hms) > 3:
            raise SourceSpecificationError('ra_hms must be specified as a sequence of at most three elements (hours, minutes, seconds), instead, you specified '+str(self.ra_hms))

        self.ra_hms = tuple(self.ra_hms) +(0,)*(3-len(self.ra_hms))
        
        
        if len(self.dec_sdms) > 4 or len(self.dec_sdms) == 0:
            raise SourceSpecificationError('dec_sdms must be specified as a sequence of at least one and at most four elements (sign +/-, degrees, minutes, seconds), instead, you specified '+str(self.dec_sdms))
        
        if not self.dec_sdms[0] in ['+', '-']:
            raise SourceSpecificationError('The first element of dec_sdms must be either a ''+'' or a ''-'', instead it is \''+str(self.dec_sdms[0])+'\'.')

        self.dec_sdms = tuple(self.dec_sdms) +(0,)*(4-len(self.dec_sdms))
        return self



    def ra_deg(self):
        """
        Return right ascension in degrees
        """
        if self.ra_deg_val is None:
            return (self.ra_hms[0]+self.ra_hms[1]/60.0 +self.ra_hms[2]/3600.0)*180/12.0
        else:
            return self.ra_deg_val


    def dec_deg(self):
        """
        Return declination in degrees
        """
        if self.dec_deg_val is None:
            abs_deg = (self.dec_sdms[1]+self.dec_sdms[2]/60.0 +self.dec_sdms[3]/3600.0)
            if self.dec_sdms[0] == '-':
                return -abs_deg
            else:
                return abs_deg
        else:
            return self.dec_deg_val
        

    def __repr__(self):
        return 'TargetSource(name='+repr(self.name)+', ra_hms='+repr(self.ra_hms)+', dec_sdms='+repr(self.dec_sdms)+')'

    def __str__(self):
        return repr(self)
