##########################################################################################
#                                                                                        #
#   This program takes 4 arguments:                                                      #
#   1) A final name for a file containing a list of dark exposure file names             #
#   2) A final name for a file containing a list of the long exposure flats file names   #
#   3) A final name for a file containing a list of science exposure file names          #
#   4) A basename that all files written by this program will start with                 #
#                                                                                        #
#   There are three functions defined below:                                             #
#   1) AverageDark(darkfiles), which creates and returns the master dark image           #
#   2) AverageFlat(flatfiles,masterdark) which creats and returns the master dark        #
#      subtracted flat image                                                             #
#   3) ScienceExposure(rawscidata,masterdark,masterflat), which applied the master       #
#      dark and flat images to a raw science image                                       #
#                                                                                        #
#   Below these functions is the main body of the program, which applies the master      #
#   dark and master flat to all of the science images and writes that clean science      #
#   images to files                                                                      #
#                                                                                        #
#   This code was adapted from code written by the TAs of the Physics 100 course at      #
#   Stanford University (Anna Ogorzalek et al.).                                         #
#   Modified for PHY 517 / AST 443 at Stony Brook University by Drew Jamieson and        #
#   Anja von der Linden                                                                  #
#                                                                                        #
##########################################################################################

# This is the incomplete version of the calibration script that you will be
# using to process all of your observatory data. You will need to finish 
# this script to complete the data reduction. Remember at any point
# during development you can try running the script on a real data and see
# if the output products make sense.

# Here are the libraries we need. Note that wherever you see np, that
# stands for Numpy. 'import' loads an external library.

import pyfits
import numpy as np

# Python is an interpreted programming language, so we have to put all of our functions BEFORE
# the main body of the code!

# This function does the combining of dark currents
def AverageDark(darkfiles):

    # opens each dark image file and stores the 2d images in a numpy array
    darkdata=np.array([pyfits.open(i.rstrip('\n'))[0].data for i in darkfiles],'f')
    
    ### !!! TODO FINISH THIS FUNCTION !!!
    
    masterdark=np.median(darkdata, axis=0)        # What goes in here? np.mean(darkdata, axis=0) or np.median(darkdata, axis=0)?
    return masterdark


# This function creates a combined flat field image
def AverageFlat(flatfiles):
    
    # opens each flat image file and stores the 2d images in a numpy array
    flatdata=np.array([pyfits.open(i.rstrip('\n'))[0].data for i in flatfiles],'f')
    # normalizes each image by its median (useful especially if the flats have very different count level):
    for i in range(0,flatdata.shape[0]):
        flatdata[i]=flatdata[i]/np.median(flatdata[i])
    masterflat=np.median(flatdata,axis=0) # Median combines flat images
    masterflat = 1.0*masterflat/np.mean(masterflat) # Normalizes to the mean of the flats
    return masterflat

# This function creates the processed science image after combined dark, and flat images have been created.  
def ScienceExposure(rawscidata,masterdark,masterflat):
    
    rawimage=rawscidata.data #Gets the data from the header of the science image file
    
        ### !!! TODO FINISH THIS FUNCTION !!!
    
    scienceimage=scienceimage=(rawimage-masterdark)/masterflat # How should you combine the rawimage data with the masterdark and masterflat data?
    return scienceimage

# This is the end of the functions. The main body of the code begins below.

# Each of these is an argument that needs to be on the calling of the script. 
# Make sure you run with all arguments provided or you will run into errors!

darkfilelist=list()
flatfilelist=list()
sciencefilelist=list()
basename='processed'
beginnum=0
num=18
for i in range(num):
    if(i+beginnum<10):
        darkfilelist.append('dark_30s.0000000'+str(beginnum+i)+'.DARK.FIT')
    if(i+beginnum>=10):
        darkfilelist.append('dark_30s.000000'+str(beginnum+i)+'.DARK.FIT')
beginnum=476
num=20
for i in range(num):
    darkfilelist.append('flatafter.00000'+str(beginnum+i)+'.DARK.FIT')
    
beginnum=20
num=10
for i in range(num):
    flatfilelist.append('flat.000000'+str(beginnum+i)+'.FIT')
    
beginnum=33
num=408
for i in range(num):
    if(i+beginnum<100):
        sciencefilelist.append('flat.000000'+str(beginnum+i)+'.FIT')
    if(i+beginnum>=100):
        sciencefilelist.append('flat.00000'+str(beginnum+i)+'.FIT')


finaldark=AverageDark(darkfilelist) # Find function aboved

finalflat=AverageFlat(flatfilelist) # Find function aboved

for sciencefile in sciencefilelist: # Loops though all science files to apply finaldark and finalflat corrections

    sciencefile = sciencefile.rstrip('\n')

    rawdata=pyfits.open(sciencefile)[0] # This gets the 1st extension (starts with 0!), this is an example of 
                                        # using pyfits.open, this is a FITS file object
    finalimage=ScienceExposure(rawdata,finaldark,finalflat) # Find function above
    sciheader=rawdata.header # This grabs the header object from the FITS object rawdata
    newscience=basename+'_'+sciencefile+'_clean.fits'  # Appending filenames onto the base
    sciencehdu=pyfits.PrimaryHDU(finalimage,header=sciheader)  # This converts a numpy array into a FITS object with a 
                                                               # data block (finalimage) and a header (sciheader)
    sciencehdu.writeto(newscience, clobber=True) # This writes the fits object to the file name newscience, which is 
                                                 # defined above The clobber means to overwrite the file if it already exists.

newdark=basename+'_Master_Dark.fits'
newflat=basename+'_Master_Flat.fits'

darkhdu=pyfits.PrimaryHDU(finaldark)
darkhdu.writeto(newdark, clobber=True)

flathdu=pyfits.PrimaryHDU(finalflat)
flathdu.writeto(newflat, clobber=True)
# Given the names and conventions, how do we write our final flat field image to the disk?



###################################### End of Program ##########################################
