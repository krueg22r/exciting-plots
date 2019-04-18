#! /home/krueger/python/bin/python3

import matplotlib.pyplot as plt
import rplot as rp
import pandas as pd

def procArray(npArray): 
    npArray = rp.sortAllLeft(npArray, 1)
    npArray = rp.hartreeToKJ(npArray)
    return npArray

def main(): 

    naB2 = rp.loadFile('naB2.dat')
    naB2 = procArray(naB2)
    naB3 = rp.loadFile('naB3.dat')
    naB3 = procArray(naB3)
    naADC = rp.loadFile('naADC.dat')
    naADC = procArray(naADC)


    baB2 = rp.loadFile('baB2.dat')
    baB2 = procArray(baB2)
    baB3 = rp.loadFile('baB3.dat')
    baB3 = procArray(baB3)
    baADC = rp.loadFile('baADC.dat')
    baADC = procArray(baADC)


    bnB2 = rp.loadFile('bnB2.dat')
    bnB2 = procArray(bnB2)
    bnB3 = rp.loadFile('bnB3.dat')
    bnB3 = procArray(bnB3)
    bnADC = rp.loadFile('bnADC.dat')
    bnADC = procArray(bnADC)
    
    fontSize = 9
    padding = 22
    plt.rcParams.update({'font.size': fontSize})
    fo = rp.formatObj()
    
    xMin = 2.6
    yMin = -95
    xMax = 7.25
    yMax = 15
    aspect = (xMax-xMin) / (yMax - yMin)    
    plt.figure(1, figsize=(8,2))
    ax1 = plt.subplot(131)
    ax1.set_aspect(aspect)
    plt.title('ADC(2)')
    plt.plot(bnADC[0], bnADC[1], fo.getMarker(0), markersize=2, color = fo.getColor(0), label = '(BN)$^*$')
    rp.plotSpline(bnADC[0], bnADC[1], fo.getColor(0))
    plt.plot(baADC[0], baADC[1], fo.getMarker(0), markersize=2, color = fo.getColor(2), label = '(BA)$^*$')
    rp.plotSpline(baADC[0], baADC[1], fo.getColor(2))
    plt.plot(naADC[0], naADC[1], fo.getMarker(0), markersize=2, color = fo.getColor(1), label = '(NA)$^*$')
    rp.plotSpline(naADC[0], naADC[1], fo.getColor(1))
    axes = plt.gca()
    axes.set_xlim([xMin,xMax])
    axes.set_ylim([yMin,yMax])
    plt.ylabel('$E$\n (kJ/mol)', fontsize=fontSize, rotation='horizontal', labelpad=padding)
    plt.xlabel('$r_{z}$ $\mathrm{(\AA)}$', fontsize=fontSize)

    ax2 = plt.subplot(132)
    ax2.set_aspect(aspect)
    plt.title('B2PLYP')
    plt.plot(bnB2[0], bnB2[1], fo.getMarker(0), markersize=2, color = fo.getColor(0), label = '(BN)$^*$')
    rp.plotSpline(bnB2[0], bnB2[1], fo.getColor(0))
    plt.plot(baB2[0], baB2[1], fo.getMarker(0), markersize=2, color = fo.getColor(2), label = '(BA)$^*$')
    rp.plotSpline(baB2[0], baB2[1], fo.getColor(2))
    plt.plot(naB2[0], naB2[1], fo.getMarker(0), markersize=2, color = fo.getColor(1), label = '(NA)$^*$')
    rp.plotSpline(naB2[0], naB2[1], fo.getColor(1))
    #plt.legend(loc='lower right')
    axes = plt.gca()
    axes.set_xlim([xMin,xMax])
    axes.set_ylim([yMin,yMax])
    plt.xlabel('$r_{z}$ $\mathrm{(\AA)}$', fontsize=fontSize)
    
    ax3 = plt.subplot(133)
    ax3.set_aspect(aspect)
    plt.title('B3LYP') 
    plt.plot(bnB3[0], bnB3[1], fo.getMarker(0), markersize=2, color = fo.getColor(0), label = '(BN)$^*$')
    rp.plotSpline(bnB3[0], bnB3[1], fo.getColor(0))
    plt.plot(baB3[0], baB3[1], fo.getMarker(0), markersize=2, color = fo.getColor(2), label = '(BA)$^*$')
    rp.plotSpline(baB3[0], baB3[1], fo.getColor(2))
    plt.plot(naB3[0], naB3[1], fo.getMarker(0), markersize=2, color = fo.getColor(1), label = '(NA)$^*$')
    rp.plotSpline(naB3[0], naB3[1], fo.getColor(1))
    axes = plt.gca()
    axes.set_xlim([xMin,xMax])
    axes.set_ylim([yMin,yMax])
    #plt.legend(loc='best')
    plt.xlabel('$r_{z}$ $\mathrm{(\AA)}$', fontsize=fontSize)


    plt.subplots_adjust(hspace=0)
    plt.subplots_adjust(wspace=0)
    
    plt.savefig('allBindNew.pdf', format='pdf', bbox_inches='tight')


main()
