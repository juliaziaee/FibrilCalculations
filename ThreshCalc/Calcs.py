'''
Created on Jan 6, 2020

@author: juliaziaee
'''

import csv
from numpy import double


'''
reads in csv file to get rates
'''
def filereadrates(filename):
    rates = []
    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        fields = next(csvreader)
        for row in csvreader:
            if row[0] != '':
                rates.append(row)

    return rates


'''
reads in csv file to get time points
'''
def filereadtimes(filename):
    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        fields = next(csvreader)
        times = (fields)
    times[0] = '0'

    return times

'''
sets up output using the other functions in the program
'''
def calc(filename):
    times = filereadtimes(filename)
    rates = filereadrates(filename)

    cutoff = ratechecker(rates)
    opt = optimalRate(rates)
    ct = ctvals(rates, cutoff, times)
    maxtime = times[opt]
    return "Threshold Value is " + str(cutoff) + " and optimal linearity is at time " + str(maxtime) + " \n ct vals in order: " + str(ct)


'''
Finds threshold value used to get Ct values
'''
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
            while n < len(comps) - 1 and checker == 0:
                percentchange = comps[n] - comps[n-1]
                if percentchange >= 0.20 and comps[n] > 1 and comps[n+1] > 1:
                    avgs.append(double(t[n+1]))
                    checker += 1
                n += 1
        look = sorted(avgs)
        if len(look) == 3: 
            group_ct.append(look[1])
        if len(look) == 2:
            group_ct.append((look[0] + look[1])/2) 
        if len(look) == 1:
            group_ct.append(look[0])
    
    helpersum = 0
    if len(group_ct) != 0:                      
        for num in group_ct:
            helpersum += num
        return helpersum/len(group_ct)
    
    else:
        return "NA"
    
    
    
    
'''
Finds time of optimal linearity
'''    
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
 
 
 
'''
Finds ct values for each triplicate in the csv
'''           
def ctvals(rates, thresh, times):
    siind = 0
    t = []
    while siind < len(rates) - 2:
        rep1 = rates[siind]
        rep2 = rates[siind +1]
        rep3 = rates[siind + 2]
        done = 0
        for i in range(len(rep1)):
            avgval = (double(rep1[i]) + double(rep2[i]) + double(rep3[i]))/3
            if avgval >= thresh and done == 0:
                t.append(times[i])
                done += 1
            else:
                if i == len(rep1) - 1 and done == 0:
                    t.append(0)
        siind += 3
    
    return t        
            
            
            




filename = "CSFs.csv"
print(calc(filename))