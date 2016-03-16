"""Format the data extracted in scrape_forexite.py
NOTE: only currency pairs present in the first data file will be collected"""

import numpy as np
import scipy as sp
from scipy import signal
import h5py

def interpfx(time,fx,time_pre):
    opens = np.zeros(len(time))
    f = sp.interpolate.interp1d(time_pre, fx)
    
    for t in range(len(time)):
        try:
            opens[t] = f(time[t])
        except ValueError:
            if time[t] < min(time_pre):
                opens[t] = f(min(time_pre))
            elif time[t] > max(time_pre):
                opens[t] = f(max(time_pre))
            else:
                raise ValueError('Interpolation error')
    return opens

# User input
D = 311  # User declare # text files (numbered) scraped from forexite
dataname = '2011'
# Default output filepath and name in scrape_forexite.py
fipath = 'C:/gh/data/fx/2011days/'

# Determine number of currency pairs
tempdata = np.loadtxt(fipath + 'd0.txt', dtype=np.str, delimiter=',')
tempt = tempdata[1:, 2].astype(np.int)
tempt[tempt == 0] = 240000
curbound = np.append(0, signal.argrelmax(tempt)[0] + 1)
P = len(curbound)

# Convert data from .txt to arrays

dates = np.zeros((D, 3))
opens = np.zeros((P, D), dtype=object)
highs = np.zeros((P, D), dtype=object)
lows = np.zeros((P, D), dtype=object)
closes = np.zeros((P, D), dtype=object)
times = np.zeros(D, dtype=object)
opens_pre = np.zeros(P, dtype=object)
highs_pre = np.zeros(P, dtype=object)
lows_pre = np.zeros(P, dtype=object)
closes_pre = np.zeros(P, dtype=object)
times_pre = np.zeros(P, dtype=object)
for d in range(D):
    print str(d+1) + '/' + str(D)

    finame = fipath + 'd' + str(d) + '.txt'
    txtdata = np.loadtxt(finame, dtype=np.str, delimiter=',')
    dates[d, 0] = np.int(txtdata[1, 1][6:])  # Date
    dates[d, 1] = np.int(txtdata[1, 1][4:6])  # Month
    dates[d, 2] = np.int(txtdata[1, 1][:4])  # Year
    dopens = txtdata[1:, 3].astype(np.float)
    dhighs = txtdata[1:, 4].astype(np.float)
    dlows = txtdata[1:, 5].astype(np.float)
    dcloses = txtdata[1:, 6].astype(np.float)

    # Split up data by currency
    ts = txtdata[1:, 2].astype(np.int)
    ts[ts == 0] = 240000
    pairbound = np.append(0, sp.signal.argrelmax(ts)[0] + 1)
    tlengths = np.zeros(P)
    if len(pairbound) < P:
        raise IndexError(
            'A later date had fewer currency pairs than the first date')
    for p in range(P):
        t_start = pairbound[p]
        if p == len(pairbound) - 1:
            t_end = len(ts)
        else:
            t_end = pairbound[p + 1]
        times_pre[p] = ts[t_start:t_end]
        opens_pre[p] = dopens[t_start:t_end]
        highs_pre[p] = dhighs[t_start:t_end]
        lows_pre[p] = dlows[t_start:t_end]
        closes_pre[p] = dcloses[t_start:t_end]
        tlengths[p] = len(times_pre[p])

    # Identify the full time array for that day
    # NOTE: There may be a minute or two missing for some days, but I think this is negligible
    # NOTE: Each currency is forced to the same time array. A disadvantage of this
    # is that currencies start and stop being traded at different times weekly
    p4t = np.argmax(tlengths)
    times[d] = times_pre[p4t]

    # Interpolate each currency's data for the main time array
    for p in range(P):
        opens[p, d] = interpfx(times[d],opens_pre[p],times_pre[p])
        highs[p, d] = interpfx(times[d],highs_pre[p],times_pre[p])
        lows[p, d] = interpfx(times[d],lows_pre[p],times_pre[p])
        closes[p, d] = interpfx(times[d],closes_pre[p],times_pre[p])


# Combine data across days
# Calculate how many timepoints there are for all days
cum_time = 0
dates_tstart = np.zeros(D)
dates_tend = np.zeros(D)
for d in range(D):
    dates_tstart[d] = cum_time
    dates_tend[d] = cum_time + len(times[d])
    cum_time += len(times[d])

all_data = {'opens': np.zeros((P, cum_time)),
            'highs': np.zeros((P, cum_time)),
            'lows': np.zeros((P, cum_time)),
            'closes': np.zeros((P, cum_time))}
for d in range(D):
    print str(d+1) + '/' + str(D)
    for p in range(P):
        all_data['opens'][p, dates_tstart[d]:dates_tend[d]] = opens[p, d]
        all_data['highs'][p, dates_tstart[d]:dates_tend[d]] = highs[p, d]
        all_data['lows'][p, dates_tstart[d]:dates_tend[d]] = lows[p, d]
        all_data['closes'][p, dates_tstart[d]:dates_tend[d]] = closes[p, d]

# Save with h5py
finame = fipath + dataname + '.hdf5'
with h5py.File(finame, 'w') as fi:
    fi['opens'] = all_data['opens']
    fi['highs'] = all_data['highs']
    fi['lows'] = all_data['lows']
    fi['closes'] = all_data['closes']
    fi['dates_tstart'] = dates_tstart
    fi['dates_tend'] = dates_tend
    fi['dates'] = dates
