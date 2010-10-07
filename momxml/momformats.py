

def mom_antenna_name_from_mac_name(mac_name):
    """
    Converts 'HBA_ONE' to 'HBA One', 'LBA_SPARSE_EVEN' to 'LBA Sparse
    Even', etc.
    """
    name = mac_name.split('_')
    return ' '.join([name[0]]+[s.capitalize() for s in name[1:]])



def mom_frequency_range(name):
    """
    Obtain a string containing the MoM frequency range for a given
    frequency band. Allowed frequency bands are: 'LBA_LOW',
    'LBA_HIGH', 'HBA_LOW', 'HBA_MID', and 'HBA_HIGH'.
    """
    translation_table= {'LBA_LOW' : '10-90 MHz',
                        'LBA_HIGH': '30-90 MHz',
                        'HBA_LOW' : '110-190 MHz',
                        'HBA_MID' : '170-230 MHz',
                        'HBA_HIGH': '210-250 MHz'}
    return translation_table[name]



def mom_timestamp(year, month, day, hours, minutes, seconds):
    """
    Return the MoM representation of a date
    """
    return '%4d-%02d-%02dT%02d:%02d:%02d'%(year, month, day, hours, minutes, seconds)


def mom_duration(hours=None, minutes=None, seconds=None):
    duration='PT'
    if hours is not None:
        duration+='%02dH'%(int(hours),)
    if minutes is not None:
        duration+='%02dM'%(int(minutes),)
    if seconds is not None:
        duration+='%02dS'%(int(seconds),)
    return duration
