# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 20:28:12 2023

@author: Jesse
"""


import xarray as xr
import numpy as np
from scipy import stats


def open_cesm_atm(file_path):
    
    ds = xr.open_dataset(file_path)
    ds.coords['lon']=(ds.coords['lon']+180)%360-180
    ds=ds.sortby(ds.lon) 
    
    ##-- group data into yearly means from seasons

    RSDS=ds.FSDS.groupby('time.season')['DJF'].groupby('time.year').mean('time') 
    RLDS=ds.FLDS.groupby('time.season')['DJF'].groupby('time.year').mean('time')
    NET=ds.FSNS+ds.FLDS
    NETRAD=NET.groupby('time.season')['DJF'].groupby('time.year').mean('time')
    LST=ds.TS.groupby('time.season')['DJF'].groupby('time.year').mean('time')  
        
    return RSDS,RLDS,NETRAD,LST
        
#open the files   
SON = open_cesm_atm('D:/data/CESM1/CESM1_SnowRad_atm_1980-2005_masked_2deg.nc')
NOS = open_cesm_atm('D:/data/CESM1/CESM1_NoSnowRad_atm_1980-2005_masked_2deg.nc')


 ## perform a student's t-test using the 
diff_val = np.zeros((90, 180))
p_value = np.zeros((90, 180))

for i in np.arange(90):
    for j in np.arange(180):
        
        try:
            diff_val[i,j] = stats.ttest_ind(NOS[2][:,i,j], SON[2][:,i,j], equal_var=True, alternative='two-sided').statistic  
            p_value[i,j]  = stats.ttest_ind(NOS[2][:,i,j], SON[2][:,i,j], equal_var=True, alternative='two-sided').pvalue
        except:
            diff_val[i,j] = np.nan
            p_value[i,j]  = np.nan



## define data as xarray dataset and save as netcdf
lon=NOS[0]['lon'].values
lat=NOS[0]['lat'].values


#var1=xr.DataArray(data=diff_val, dims=('lat', 'lon'), coords={'lat':lat, 'lon':lon}, 
                     #attrs=dict(description="difference b/n NOS and SON", units="W/m2",),).rename('rlds')

var2=xr.DataArray(data=p_value, dims=('lat', 'lon'), coords={'lat':lat, 'lon':lon}, 
                     attrs=dict(description="significance of the difference b/n NOS and SON based on t-test",),).rename('sig')

#ds=xr.merge([var1, var2])

## save data as netcdf
var2.to_netcdf('D:/data/CESM1/seas/diff/netRAD_pvalue_NOS_SON_diff_1980-2005_2deg_DJF.nc', mode='w')
