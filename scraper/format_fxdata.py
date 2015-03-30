"""Format the data extracted in scrape_forexite.py
NOTE: only currency pairs present in the first data file will be collected"""

import numpy as np
import scipy as sp
import h5py

# User input
D = 5 # User declare # text files (numbered) scraped from forexite
fipath = 'C:\\gh\\fxdata\\' # Default output filepath and name in scrape_forexite.py

# Determine number of currency pairs
tempdata = np.loadtxt(fipath + 'd0.txt',dtype=np.str,delimiter=',')
tempt = tempdata[1:,2].astype(np.int)
tempt[tempt == 0] = 240000
curbound = np.append(0,sp.signal.argrelmax(tempt)[0]+1)
P = len(curbound)

# Convert data from .txt to arrays

dates = np.zeros((D,3))
opens = np.zeros((P,D),dtype=object)
times = np.zeros(D,dtype=object)
opens_pre = np.zeros(P,dtype=object)
times_pre = np.zeros(P,dtype=object)
for d in range(D):
    print str(d) + '/' + str(D)
    
    finame = fipath + 'd' + str(d) + '.txt'
    txtdata = np.loadtxt(finame,dtype=np.str,delimiter=',')
    dates[d,0] = np.int(txtdata[1,1][6:]) # Date
    dates[d,1] = np.int(txtdata[1,1][4:6]) # Month
    dates[d,2] = np.int(txtdata[1,1][:4]) # Year
    dopens = txtdata[1:,3].astype(np.float)
    
    
    # Split up data by currency
    ts = txtdata[1:,2].astype(np.int)
    ts[ts == 0] = 240000
    pairbound = np.append(0,sp.signal.argrelmax(ts)[0]+1)
    tlengths = np.zeros(P)
    if len(pairbound) < P:
        raise IndexError('A later date had fewer currency pairs than the first date')
    for p in range(P):
        t_start = pairbound[p]
        if p == len(pairbound)-1:
            t_end = len(ts)
        else:
            t_end = pairbound[p+1]
        times_pre[p] = ts[t_start:t_end]
        opens_pre[p] = dopens[t_start:t_end]
        tlengths[p] = len(times_pre[p])
    
    # Identify the full time array for that day
    # NOTE: There may be a minute or two missing for some days, but I think this is negligible
    # NOTE: Each currency is forced to the same time array. A disadvantage of this
    #       is that currencies start and stop being traded at different times weekly
    p4t = np.argmax(tlengths)
    times[d] = times_pre[p4t]
    
    # Interpolate each currency's data for the main time array
    for p in range(P):
        opens[p,d] = np.zeros(len(times[d]))
        f = sp.interpolate.interp1d(times_pre[p],opens_pre[p])
        for t in range(len(times[d])):
            try:
                opens[p,d][t] = f(times[d][t])
            except ValueError:
                if times[d][t] < min(times_pre[p]):
                    opens[p,d][t] = f(min(times_pre[p]))
                elif times[d][t] > max(times_pre[p]):
                    opens[p,d][t] = f(max(times_pre[p]))
                else:
                    raise ValueError('Interpolation error')  
    
        
# Combine data across days
# Calculate how many timepoints there are for all days
cum_time = 0
dates_tstart = np.zeros(D)
dates_tend = np.zeros(D)
for d in range(D):
    dates_tstart[d] = cum_time
    dates_tend[d] = cum_time + len(times[d])
    cum_time += len(times[d])

all_data = np.zeros((P,cum_time))
for d in range(D):
    print str(d) + '/' + str(D)
    for p in range(P):
        all_data[p,dates_tstart[d]:dates_tend[d]] = opens[p,d]

# Save with h5py
finame = fipath + 'format_fxdata.hdf5'
with h5py.File(finame, 'w') as fi:
    fi['all_data'] = all_data
    fi['dates_tstart'] = dates_tstart
    fi['dates_tend'] = dates_tend
    fi['dates'] = dates