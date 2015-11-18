#!/usr/bin/env python

import numpy

station_width = 30. # 30. = LBA_INNER, 87. = LBA_OUTER

rac = 299.8681525
decc = 40.7339156
freq = 60.e6
fwhm = 1.3*(299792458./freq)/station_width*180./numpy.pi
dra = fwhm/4.
ddec = fwhm/4.

outfile = open('radeclist.txt','w')

for dx in numpy.arange(-7.,8.):
	for dy in numpy.arange(-7.,8.):
		ra = rac + dx*dra
		dec = decc + dy*ddec
		print >>outfile, '%f\t%f'%(ra,dec)

