# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 15:05:24 2023

@author: Jesse
"""


import numpy as np
import xarray as xr
from matplotlib import pyplot as plt
import geocat.viz as gv



def open_cesm_atm(file_path):

    #ds = xr.open_dataset(file_path).sel(lat=np.arange(50,65,2),lon=np.arange(240,271,2),method='nearest') # North America winter
    ds = xr.open_dataset(file_path).sel(lat=np.arange(50,65,2),lon=np.arange(90,121,2),method='nearest') # Eurasia winter
    ds.coords['lon']=(ds.coords['lon']+180)%360-180
    ds=ds.sortby(ds.lon)
    
    rsds = ds.FSDS.groupby('time.month').mean('time').mean(('lat','lon'))
    rlds = ds.FLDS.groupby('time.month').mean('time').mean(('lat','lon'))
    NETRAD=ds.FSNS+ds.FLDS
    netRad= NETRAD.groupby('time.month').mean('time').mean(('lat','lon'))
    ts = ds.TS.groupby('time.month').mean('time').mean(('lat','lon'))
 
    return rsds,rlds,netRad,ts
          
SON = open_cesm_atm('D:/data/CESM1/CESM1_SnowRad_atm_1980-2005_masked_2deg.nc')
NOS = open_cesm_atm('D:/data/CESM1/CESM1_NoSnowRad_atm_1980-2005_masked_2deg.nc')

## compute the differences
cesm_rsds_diff   = NOS[0] - SON[0]
cesm_rlds_diff   = NOS[1] - SON[1]
cesm_netrad_diff = NOS[2] - SON[2]
cesm_ts_diff     = NOS[3] - SON[3]



# Define the xarray.open_mfdataset pre-processing function
def assume_noleap_calendar(ds):
    ds.time.attrs['calendar'] = 'noleap'
    return xr.decode_cf(ds)

## rsds
aa = xr.open_mfdataset('D:/data/CMIP5/Amon/rsds_*.nc',
                        concat_dim='case',
                        combine='nested',
                        preprocess=assume_noleap_calendar,
                        decode_times=False).sel(lat=np.arange(50,65,2),lon=np.arange(90,121,2),method='nearest')

#aaa = aa.rsds-aa.rsds.mean('time')
dat_rsds = aa.rsds.groupby('time.month').mean('time').mean(('lat','lon'))
rsds_diff= dat_rsds - SON[0]
rsds_cmip_avg = rsds_diff.mean(dim='case')
rsds_std = rsds_diff.std(dim='case')
rsds_pstd = rsds_cmip_avg+rsds_std
rsds_nstd = rsds_cmip_avg-rsds_std


## rlds
bb = xr.open_mfdataset('D:/data/CMIP5/Amon/rlds_*.nc',
                        concat_dim='case',
                        combine='nested',
                        preprocess=assume_noleap_calendar,
                        decode_times=False).sel(lat=np.arange(50,65,2),lon=np.arange(90,121,2),method='nearest')

dat_rlds = bb.rlds.groupby('time.month').mean('time').mean(('lat','lon'))
rlds_diff= dat_rlds - SON[1]
rlds_cmip_avg = rlds_diff.mean(dim='case')
rlds_std = rlds_diff.std(dim='case')
rlds_pstd = rlds_cmip_avg+rlds_std
rlds_nstd = rlds_cmip_avg-rlds_std


## rsus
cc = xr.open_mfdataset('D:/data/CMIP5/Amon/rsus_*.nc',
                        concat_dim='case',
                        combine='nested',
                        preprocess=assume_noleap_calendar,
                        decode_times=False).sel(lat=np.arange(50,65,2),lon=np.arange(90,121,2),method='nearest')

net = (aa.rsds-cc.rsus)+bb.rlds
dat_net = net.groupby('time.month').mean('time').mean(('lat','lon'))
net_diff= dat_net - SON[2]
net_cmip_avg = net_diff.mean(dim='case')
net_std = net_diff.std(dim='case')
net_pstd = net_cmip_avg+net_std
net_nstd = net_cmip_avg-net_std

## ts
dd = xr.open_mfdataset('D:/data/CMIP5/Amon/ts_*.nc',
                        concat_dim='case',
                        combine='nested',
                        preprocess=assume_noleap_calendar,
                        decode_times=False).sel(lat=np.arange(50,65,2),lon=np.arange(90,121,2),method='nearest')

dat_ts = dd.ts.groupby('time.month').mean('time').mean(('lat','lon'))
ts_diff= dat_ts - SON[3]
ts_cmip_avg = ts_diff.mean(dim='case')
ts_std = ts_diff.std(dim='case')
ts_pstd = ts_cmip_avg+ts_std
ts_nstd = ts_cmip_avg-ts_std



# plot data
# font settings
s = 22
font = {'weight' : 'normal',
        'size'   : s,
        'serif': 'Arial'}

plt.rc('font', **font)
plt.rc('axes', linewidth=2)

# figure set up
fig = plt.figure(figsize=(23,25),dpi=300)
plt.gcf().subplots_adjust(hspace=0.4, wspace=0.2)

ax1 = fig.add_subplot(421)
ax2 = fig.add_subplot(422)
ax3 = fig.add_subplot(423)
ax4 = fig.add_subplot(424)


ax_list = [ax1, ax2, ax3, ax4]

for ax in ax_list:
    ax.set_xticks(range(1, 12+1))
    ax.set_xticklabels(['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'])
    ax.axhline(y = 0, color = 'grey', linestyle = 'dashed')
    ax.set_xlim(1,12)

x = range(1,12+1)

ax1.set_ylim(-140,140)
ax2.set_ylim(-140,140)
ax3.set_ylim(-140,140)
ax4.set_ylim(-20,20)

# Panel 1
#ax1.plot(x, rsds_pstd, color='grey', label='CM5NOS-SON+std')
ax1.plot(x, rsds_cmip_avg, color='black', label='CM5NOS-SON',lw=2, marker = 'o')
ax1.plot(x, cesm_rsds_diff, color='red', label='NOS-SON',lw=2, marker = 'o')
#ax1.plot(x, rsds_nstd, color='grey', label='CM5NOS-SON-std')
ax1.fill_between(x, rsds_pstd, rsds_nstd, color='lightgrey', alpha=0.6)
ax1.legend(loc='lower left', frameon=False, fontsize=22)

ax1.set_ylabel('Radiation Flux (Wm$^{-2}$)', fontsize=20)
gv.set_titles_and_labels(ax1, lefttitle="(a) Surface Downward SW Radiation", lefttitlefontsize=25)


# Panel 2
#ax2.plot(x, rlds_pstd, color='grey', label='CM5NOS - SON+std')
ax2.plot(x, rlds_cmip_avg, color='black', label='CM5NOS - SON',lw=2, marker = 'o')
#ax2.plot(x, rlds_nstd, color='grey', label='CM5NOS - SON-std')
ax2.plot(x, cesm_rlds_diff, color='red', label='NOS - SON',lw=2, marker = 'o')
ax2.fill_between(x, rlds_pstd, rlds_nstd, color='lightgrey', alpha=0.6)
ax2.set_ylabel('Radiation Flux (Wm$^{-2}$)', fontsize=20)
gv.set_titles_and_labels(ax2, lefttitle="(b) Surface Downward LW Radiation", lefttitlefontsize=25)


# Panel 3
#ax3.plot(x, net_pstd, color='grey', label='CM5NOS-SON+std')
ax3.plot(x, net_cmip_avg, color='black', label='CM5NOS-SON',lw=2, marker = 'o')
ax3.plot(x, cesm_netrad_diff, color='red', label='NOS-SON',lw=2, marker = 'o')
#ax3.plot(x, net_nstd, color='grey', label='CM5NOS-SON-std')
ax3.fill_between(x, net_pstd, net_nstd, color='lightgrey', alpha=0.6)
ax3.set_ylabel('Radiation Flux (Wm$^{-2}$)', fontsize=20)
gv.set_titles_and_labels(ax3, lefttitle="(c) Surface Downward Net Radiation", lefttitlefontsize=25)
ax3.set_xlabel('Months', fontsize=20)

# Panel 4
#ax4.plot(x, ts_pstd, color='grey', label='CM5NOS-SON+std')
ax4.plot(x, ts_cmip_avg, color='black', label='CM5NOS-SON',lw=2, marker = 'o')
ax4.plot(x, cesm_ts_diff, color='red', label='NOS-SON',lw=2, marker = 'o')
#ax4.plot(x, ts_nstd, color='grey', label='CM5NOS-SON-std')
ax4.fill_between(x, ts_pstd, ts_nstd, color='lightgrey', alpha=0.6)
ax4.set_ylabel('Temperature (K)', fontsize=20)
gv.set_titles_and_labels(ax4, lefttitle="(d) Land Surface Temperature", lefttitlefontsize=25)
ax4.set_xlabel('Months', fontsize=20)


fig.savefig('C:/Users/Jesse/Dropbox (UFL)/Jesse/Manuscript/figures/figure8.jpeg', bbox_inches='tight', pad_inches = 0.1)
fig.savefig('C:/Users/Jesse/Dropbox (UFL)/Jesse/Manuscript/figures/figure8.pdf', bbox_inches='tight', pad_inches = 0.1)


