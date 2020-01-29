'''
Created on Jan 6, 2020

@author: juliaziaee
'''

import csv
from __builtin__ import int
from numpy import double
from matplotlib.sankey import DOWN


def filereadrates(filename):
    rates = []
    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        fields = next(csvreader)
        for row in csvreader:
            if row[0] != '':
                rates.append(row)

    return rates


def filereadtimes(filename):
    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        fields = next(csvreader)
        times = (fields)
    times[0] = '0'

    return times


def calc(filename):
    times = filereadtimes(filename)
    rates = filereadrates(filename)

    cutoff = ratechecker(rates)
    opt = optimalRate(rates)
    maxtime = times[opt]
    return "Ct Value is " + str(cutoff) + " and optimal linearity is at time " + str(maxtime)



def ratechecker(rates):
    triplets = []
    strtind = 0
    builder = []
    for rate in rates:
        if strtind%3 != 0 or strtind == 0:
            builder.append(rate)
            strtind += 1
        else:
            triplets.append(builder)
            builder = []
            builder.append(rate)
            strtind += 1
    
    group_ct = []
    for trip in triplets:
        avgs = []
        for t in trip:
            i = 1
            comps = []
            while i < len(t):
                top = double(t[i])
                bottom = double(t[i-1])
                rtchange = top/bottom
                comps.append(rtchange)
                i += 1
            n = 1
            checker = 0
            while n < len(comps) and checker == 0:
                percentchange = comps[n] - comps[n-1]
                if percentchange >= 0.25:
                    avgs.append(double(t[n+1]))
                    checker += 1
                n += 1
        for num in avgs:
            numflags = 0
            for c in avgs:
                if num/c > 1.25 or num/c < 0.75:
                    numflags += 1
            if numflags == 2:
                avgs.remove(num)
                
        addup = 0
        if len(avgs) != 0:
            for num in avgs:
                addup += num
            ctavg = addup/len(avgs)
            group_ct.append(ctavg)
    
    helpersum = 0
    if len(group_ct) != 0:                      
        for num in group_ct:
            helpersum += num
        return helpersum/len(group_ct)
    
    else:
        return "NA"
    
    
    
    
    
def optimalRate (rates):
    wininds = []
    for rate in rates:
        rtchanges = []
        correspond_ind = []
        strtind = 1
        while strtind < len(rate):
            change = double(rate[strtind]) - double(rate[strtind - 1])
            rtchanges.append(change)
            correspond_ind.append(strtind)
            strtind +=1
        winnerind = 0
        winnerrt = 0 
        for i in range(len(rtchanges)):
            if rtchanges[i] > winnerrt:
                winnerrt = rtchanges[i]
                winnerind = correspond_ind[i]
        wininds.append(winnerind)
    result = sorted(wininds, key = wininds.count, reverse = True) 
    return result[0]    
            
            
            
            
            




filename = "Trial2Data.csv"
print(calc(filename))