#! /home/krueger/python/bin/python3

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
from scipy import interpolate

#takes in data file name, trims lines starting with #, returns numpy matrix
#transposes data. if you do returnedArray[0], you get column zero of data file
def loadFileLabels(fileName): 
    pandaFrame = pd.read_table(fileName, header=None, delim_whitespace=True, comment='#')
    npArray = pandaFrame.values
    labels = npArray[0]
    npArray = npArray[1:]
    npArray = np.transpose(npArray)
    npArray = npArray.astype(float)
    return (npArray, labels)

def loadFile(fileName): 
    pandaFrame = pd.read_table(fileName, header=None, delim_whitespace=True, comment='#')
    return pandaFrame

#sorts all rows so that the right column is sorted smallest to largest. if normLast = 1, normalize righthand
#columns by last row value
def sortAllLeft(npArray, normLast = 0, normCol = 0): 
    nCol = npArray.shape[0] 
    for i in range(1, nCol - 1): 
        col0new, npArray[i] = zip(*sorted(zip(npArray[0], npArray[i])))
    npArray[0], npArray[nCol-1] = zip(*sorted(zip(npArray[0], npArray[nCol-1])))
    if normLast == 1: 
        for i in range(1, nCol): 
            npArray[i] -= npArray[i, len(npArray[i])-1]
    if normCol != 0: 
        normVal = npArray[normCol, len(npArray[normCol])-1]
        for i in range(1, nCol):
            npArray[i] -= normVal
    return npArray

#sort so that the rows go largest to smallest based on avg. of points between 3 and 5
#ensuring that the top->bottom order in the legend will be right if we plot
#row 1, then, row 2, etc.  
def sortForLegend(npArray, labels, minVal = 3.0, maxVal = 5.0): 
    nCol = npArray.shape[0]
    avgs = np.zeros(nCol - 1) 
    greater = np.where(npArray[0] >= minVal)[0]
    less = np.where(npArray[0] <= maxVal)[0]
    goodIndex = np.intersect1d(greater, less)
    nIndices = len(goodIndex)
    for i in range(1, nCol): 
        avg = np.sum(npArray[i][goodIndex]) / nIndices
        avgs[i-1] = avg
    rightCols = npArray[1:]
    labels = labels[1:]
    tempAvgs, rightCols = zip(*sorted(zip(avgs, rightCols)))    
    avgs, labels = zip(*sorted(zip(avgs, labels)))
    rightCols = np.flip(rightCols, 0)
    npArray = np.insert(rightCols, 0, npArray[0], axis=0)
    labels = np.insert(labels, 0, 'dummy')
    return npArray, labels

#convert all righthand columns from hartree to kJ/mol
def hartreeToKJ(npArray): 
    nCol = npArray.shape[0]
    for i in range(1, nCol):
        npArray[i] *= 2625.5
    return npArray    
    
#keeps track of colors & markers used. provides either a new one or the last one used
class formatObj(object): 
    def __init__(self, grayscale = 0, colorCounter = 0, markerCounter = 0): 
        #self.markers = ['o', 'v', 'd', 'X', 's', '<', '>', 'p', '8']
        self.markers = ['o', 'v', 's', 'd','>', 'p', '8', '^', 'P', '<', '*']
        self.grayscale = ['#f7f7f7', '#cccccc', '#969696', '#636363', '#252525']
        # red is '#e41a1c'
        self.colors = ['#e41a1c','#377eb8','#4daf4a','#984ea3','#ff7f00', '#515A5A']
        if grayscale == 1: 
            self.colors = self.grayscale
        self.markerCounter = markerCounter
        self.colorCounter = colorCounter
    def nowColor(self): 
        return self.colors[self.colorCounter]
    def newColor(self): 
        if self.colorCounter < 4: 
            self.colorCounter += 1
            return self.colors[self.colorCounter]
        else: 
            self.colorCounter = 0
            return self.colors[self.colorCounter]
    def newMarker(self): 
        if self.markerCounter < 4:
            self.markerCounter += 1
            return self.markers[self.markerCounter]
        else:
            self.makerCounter = 0
            return self.markers[self.markerCounter]
    def getColor(self, index): 
        if index >= len(self.colors): 
            print('requested color index '+str(index)+' does not exist. Max color index is '+str(len(self.colors)-1))
            exit()
        else: 
            return self.colors[index]
    def getMarker(self, index): 
        if index >= len(self.markers): 
            print('requested marker index '+str(index)+' does not exist. Max marker index is '+str(len(self.markers)-1))
        else: 
            return self.markers[index]


#takes numpy arrays for x and y, an optional label, and a formatObj
def plotCol(x, y, formatter, curveColor, spline = 0,  plotLabel=''):
    plt.plot(x, y, formatter.newMarker(), color = curveColor, markersize = 5, label = plotLabel)
    if spline == 1: #fails if data are not in order!  
        xNew = np.linspace(np.amin(x), np.amax(x), 350)
        tck = interpolate.splrep(x, y, s=0, k=3)
        yNew = interpolate.splev(xNew, tck, der=0)
        plt.plot(xNew, yNew, '-', color = curveColor)

def plotSpline(x, y, curveColor): 
    xNew = np.linspace(np.amin(x)-1, np.amax(x), 350)
    tck = interpolate.splrep(x, y, s=0, k=2)
    yNew = interpolate.splev(xNew, tck, der=0)
    plt.plot(xNew, yNew, '-', lw=1, color = curveColor)
    print('eBind y = '+str(np.amin(yNew)))
    print('r0 = '+str(xNew[np.argmin(yNew)]))
    #print('E at 3.15 = '+str(interpolate.splev([3.15], tck, der=0)))
    

#set takes two labels, sets them both + font sizes
def axisLabels(xLabel, yLabel): 
    plt.xlabel(xLabel, fontsize=15)
    plt.ylabel(yLabel, fontsize=15)
    #adjust auxiliarly font size here b/c it basically only affects labels
    #plus we usually have labels
    plt.rcParams.update({'font.size': 15})
    
#set legend location
def setLegend(legendLoc): 
    #legend = plt.legend(loc=legendLoc)
    legend = plt.legend(loc='best')


