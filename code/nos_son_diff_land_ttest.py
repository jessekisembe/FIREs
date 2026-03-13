# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 22:30:21 2023

@author: Jesse
"""

import xarray as xr
import numpy as np
from scipy import stats


def open_cesm_land(file_path):
    
    ds = xr.open_dataset(file_path)
    ds.coords['lon']=(ds.coords['lon']+180)%360-180
    ds=ds.sortby(ds.lon) 
    
    ##-- group data into yearly means from seasons

    GRTM=ds.TG.groupby('time.season')['JJA'].groupby('time.year').mean('time') #ground temperature
    TEMP=ds.TSA.groupby('time.season')['JJA'].groupby('time.year').mean('time') #2m air temperature
    GEVP=ds.QSOIL.groupby('time.season')['JJA'].groupby('time.year').mean('time') #ground evaporation
    SPHM=ds.Q2M.groupby('time.season')['JJA'].groupby('time.year').mean('time') # 2m specific humidity
    SOM=ds.SOILLIQ.sel(levgrnd=slice('0.007101')).groupby('time.season')['JJA'].groupby('time.year').mean('time') # soil liquid water
    SOM = np.squeeze(SOM, axis=1)
    SOI=ds.SOILICE.sel(levgrnd=slice('0.007101')).groupby('time.season')['JJA'].groupby('time.year').mean('time') # soil ice
    SOI = np.squeeze(SOI, axis=1)
    SNC=ds.FSNO.groupby('time.season')['JJA'].groupby('time.year').mean('time') # snow cover
    SND=ds.H2OSNO.groupby('time.season')['JJA'].groupby('time.year').mean('time') # snow depth
        
    return GRTM,TEMP,GEVP,SPHM,SOM,SOI,SNC,SND
        
#open the files   
SON = open_cesm_land('D:/data/CESM1/Lmon/f09.B-hist.SON.land-CDO_2X2_1980_2005.nc')
NOS = open_cesm_land('D:/data/CESM1/Lmon/f09.B-hist.NOS.land-CDO_2X2_1980_2005.nc')


 ## perform a student's t-test using the 
diff_val = np.zeros((90, 180))
p_value = np.zeros((90, 180))

for i in np.arange(90):
    for j in np.arange(180):
        
        try:
            diff_val[i,j] = stats.ttest_ind(NOS[7][:,i,j], SON[7][:,i,j], equal_var=True, alternative='two-sided').statistic  
            p_value[i,j]  = stats.ttest_ind(NOS[7][:,i,j], SON[7][:,i,j], equal_var=True, alternative='two-sided').pvalue
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
var2.to_netcdf('D:/data/CESM1/seas/diff/land/Snowdepth_pvalue_NOS_SON_diff_1980-2005_2deg_JJA.nc', mode='w')
