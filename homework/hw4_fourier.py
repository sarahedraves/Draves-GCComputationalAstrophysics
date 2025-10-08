import sys
import os
import argparse
import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt

def fits_file(value): #claude recommended this as a way of checking that the file name ends with .fits, instead of just checking after the input process
    if not value.endswith('.fits'):
        raise argparse.ArgumentTypeError(f"'{value}' must end with .fits")
    return value

def read_fits(filename):
    hdul = fits.open(filename)
    times = hdul[1].data['times']
    fluxes = hdul[1].data['fluxes']
    ferrs = hdul[1].data['ferrs']
    return times,fluxes,ferrs

def filt_dates(times,fluxes,mintime=2400,maxtime=2600): #picked default max and min by looking at plot in playground file
    datemask=(times>mintime) & (times<maxtime)
    filttimes=times[datemask]
    filtfluxes=fluxes[datemask]
    return filttimes,filtfluxes

def plot_fluxes(filttimes,filtfluxes):
    plt.figure(1)
    plt.scatter(filttimes,filtfluxes,marker='.')
    plt.xlabel('BJD')
    plt.ylabel('Normalized Flux')
    plt.title('Light Curve')

def plot_coeffs(C2):
    plt.figure(2)
    plt.scatter(np.arange(1,C2.size),C2[1:],marker='.')
    plt.xlabel('k')
    plt.ylabel(r'$|c_k|^2$')
    plt.title('Power Spectrum \n (zero frequency filtered out)')

def filter_coeffs(Cs,C2,filtermethod,XpercentortopN):
    if filtermethod=='xpercentofmaxcoeff':
        maxC2=np.max(C2[1:])
        freqmask=C2>(XpercentortopN*maxC2)
    elif filtermethod=='topncoeffs':
        XpercentortopN=int(XpercentortopN)
        # Get exactly N largest (breaks ties arbitrarily) - from Claude
        indices = np.argpartition(C2, -XpercentortopN)[-XpercentortopN:]
        freqmask = np.zeros(C2.shape, dtype=bool)
        freqmask[indices] = True
    Cfilt=np.where(freqmask, Cs, 0)
    return Cfilt

def plot_inverse(filttimes,inverted):
    plt.figure(3)
    plt.plot(filttimes,inverted)
    plt.xlabel('BJD')
    plt.ylabel('Smoothed Fluxes')
    plt.title('Smoothed Light Curve')

def main():
    #create parser and add arguments 
    parser=argparse.ArgumentParser()
    # parser.add_argument('--filename', - will uncomment this if i figure out how to automatically narrow the fits file to the best range
    #                     default='tic0002236015.fits',
    #                     type=fits_file,
    #                     help='Name of the fits file with a light curve.') 
    parser.add_argument('--plotfluxes',
                        default=False,
                        action='store_true',
                        help='When this flag is used, a plot will be shown of the light curve filtered to the dates used in the Fourier analysis.')
    parser.add_argument('--plotcoeffs',
                        default=False,
                        action='store_true',
                        help='When this flag is used, a plot will be shown of the power spectrum.')
    parser.add_argument('--filtermethod',
                        choices=['xpercentofmaxcoeff','topncoeffs'],
                        default='xpercentofmaxcoeff',
                        type=str.lower,
                        help='Method of choosing which coefficients are used in the inverse fourier transformation. Both methods filter out the coefficient of the zero frequency. Default: xpercentofmaxcoeff.')
    parser.add_argument('XpercentortopN',
                        type=float,
                        help='If filtermethod is xpercentofmaxcoeff, then a percentage from 0 to 1. Coefficients greater than X% of the maximum coefficient (when they are all squared) are kept. If filtermethod is topncoeffs, then an integer 1 or greater. The N largest coefficients are kept.')

    #parse arguments
    args=parser.parse_args()
    #filename=args.filename
    filename='tic0002236015.fits'
    plotfluxes=args.plotfluxes
    plotcoeffs=args.plotcoeffs
    filtermethod=args.filtermethod
    XpercentortopN=args.XpercentortopN

    if filtermethod=='xpercentofmaxcoeff' and (XpercentortopN<0 or XpercentortopN>1):
        print('When filtermethod is Xpercentofmaxcoeff, XpercentortopN must be a float between 0 and 1.')
        return
    if filtermethod=='topncoeffs' and not (XpercentortopN.is_integer() and XpercentortopN>=1):
        print('When filtermethod is topNcoeffs, XpercentortopN must be an integer 1 or greater.')
        return

    times,fluxes,ferrs=read_fits(filename)
    filttimes,filtfluxes=filt_dates(times,fluxes)

    if plotfluxes:
        plot_fluxes(filttimes,filtfluxes)

    Cs=np.fft.rfft(filtfluxes)
    C2=abs(Cs)**2

    if plotcoeffs:
        plot_coeffs(C2)

    Cfilt=filter_coeffs(Cs,C2,filtermethod,XpercentortopN)
    inverted=np.fft.irfft(Cfilt,n=filttimes.size)
    plot_inverse(filttimes,inverted)

    plt.show()

if __name__=="__main__":
    main()