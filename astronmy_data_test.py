from astropy.io import fits
fits_image_filename ='/Users/2020shatgiskessell/Downloads/specObj-dr14.fits'
fits_image_filename2 ='/Users/2020shatgiskessell/Downloads/galSpecInfo-dr8.fits'

hdul = fits.open(fits_image_filename)
hdul2 = fits.open(fits_image_filename2)

#https://data.sdss.org/datamodel/files/SPECTRO_REDUX/specObj.html
data = hdul[1].data

#https://dr12.sdss.org/fields/raDec?ra=146.71421&dec=-1.0413043 - to get image of object
print(data[:5]["PLUG_RA"])
print(data[:5]["PLUG_DEC"])
print(data[:5]["VDISP"])

#print (data2["specObjID"])
