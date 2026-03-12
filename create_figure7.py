# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 17:54:56 2023

@author: Jesse
"""



import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import cmaps
import geocat.viz as gv



def open_cesm_atm(file_path):

    ds = xr.open_dataset(file_path)
    ds.coords['lon']=(ds.coords['lon']+180)%360-180
    ds=ds.sortby(ds.lon)

    rsds=ds.FSDS.groupby('time.season').mean('time').sel(season='DJF')
    rlds=ds.FLDS.groupby('time.season').mean('time').sel(season='DJF')
   
    NETRAD=ds.FSNS+ds.FLDS
    netRad=NETRAD.groupby('time.season').mean('time').sel(season='DJF')
    ts=ds.TS.groupby('time.season').mean('time').sel(season='DJF')
           
    return rsds,rlds,netRad,ts
        

def open_cmip5_atm(file_path):
    
    '''
    This function opens CMIP5 data
    returns a 2d array of radiation fluxes under all sky conditions for a particular season
    Data is of the format lon, lat, time
    it uses the xarray library
    
    '''

    ds = xr.open_mfdataset(file_path)
    #print(ds)
    ds.coords['lon']=(ds.coords['lon']+180)%360-180
    ds=ds.sortby(ds.lon)

    RSDS=ds.rsds.groupby('time.season').mean('time').sel(season='DJF')
    RLDS=ds.rlds.groupby('time.season').mean('time').sel(season='DJF')
    NET=ds.rsds-ds.rsus+ds.rlds
    NETRAD=NET.groupby('time.season').mean('time').sel(season='DJF')
    LST=ds.ts.groupby('time.season').mean('time').sel(season='DJF')
        
    return RSDS,RLDS,NETRAD,LST


#open the files   
SON = open_cesm_atm('D:/data/CESM1/CESM1_SnowRad_atm_1980-2005_masked_2deg.nc')
NOS = open_cmip5_atm('D:/data/CMIP5/Amon/MMM/*.nc') 



#compute for the difference in the variables
RSDS_diff   = NOS[0] - SON[0]
RLDS_diff   = NOS[1] - SON[1]
NETRAD_diff = NOS[2] - SON[2]
LST_diff    = NOS[3] - SON[3]



## plotting
# Create a wider than normal figure to support our many plots
fig = plt.figure(figsize=(24,12),dpi=300)
plt.gcf().subplots_adjust(hspace=0.1, wspace=0.1)
plt.rcParams["font.family"] = "Arial"


def Plot(row, col, pos, diff, clevs, cbar_label, title):

    # Generate axes, using cartopy, drawing coastlines, and adding features
    projection = ccrs.PlateCarree(central_longitude=-180)
    ax = fig.add_subplot(row, col, pos, projection=projection)
   
    plt.gca().set_yticks(np.arange(-60,90,30),crs=ccrs.PlateCarree())
    plt.gca().set_xticks(np.arange(-120,240,60),crs=ccrs.PlateCarree())
    lon_formatter=LongitudeFormatter(degree_symbol=''); lat_formatter=LatitudeFormatter(degree_symbol='')
    ax.xaxis.set_major_formatter(lon_formatter); ax.yaxis.set_major_formatter(lat_formatter);ax.tick_params(labelsize=20)
    xticks = ax.xaxis.get_major_ticks(); xticks[2].set_visible(False)
    
    ax.coastlines(linewidth=1.8)
    ax.set_xlabel("")
    ax.set_ylabel("")


    # Import an NCL colormap
    newcmp = cmaps.grads_rainbow

    index = [1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12]
    color_list = [newcmp[i].colors for i in index]

    #-- Change to white
    color_list[5] = [ 1., 1., 1.]
    

    # Contourf-plot data
    temp = diff.plot.contourf(ax=ax,
                           transform=ccrs.PlateCarree(),
                           levels=clevs,
                           colors=color_list,
                           add_colorbar=False,
                           extend='both')
    
    
    # Add color bar
    cbar = plt.colorbar(temp,
                        orientation='vertical',
                        shrink=0.8,
                        extendfrac='auto', 
                        extendrect=True, 
                        drawedges=True)

    cbar.ax.tick_params(labelsize=18)
    cbar.set_ticks(clevs)
    cbar.ax.set_title(cbar_label, size=18)
    
    def custom_formatter(x, pos):
        if x in [-0.5, -0.1, 0.1, 0.5]:
            return f'{x:.1f}'  # Format with 1 decimal place
        else:
            return f'{int(x)}'  # Format as an integer
    cbar.ax.yaxis.set_major_formatter(ticker.FuncFormatter(custom_formatter))

    # Use geocat.viz.util convenience function to set titles and labels without calling several matplotlib functions
    gv.set_titles_and_labels(ax,
                            maintitle="",
                            lefttitle=title,
                            lefttitlefontsize=22,
                            righttitle="",
                            righttitlefontsize=22,
                            xlabel="",
                            ylabel="")


# define the levels for each variable
#clevs_rad  = [-15, -10, -5, -2, -0.5, 0.5, 2, 5, 10, 15]
#clevs_lst  = [-4, -2, -1, -0.5, -0.1, 0.1, 0.5, 1, 2, 4]

clevs_rad = [-20, -15, -10, -5, -2, 2, 5, 10, 15, 20]
clevs_lst = [-5, -3, -1, -0.5, -0.1, 0.1, 0.5, 1, 3, 5]


#Plot(2, 2, 1, RSDS_diff, clevs_rad, '(Wm$^{-2}$)', "(a) Downward SW Radiation   CM5NOS-NOS")
#Plot(2, 2, 2, NETRAD_diff, clevs_rad, '(Wm$^{-2}$)', "(c) Downward Net Radiation   CM5NOS-NOS")
#Plot(2, 2, 3, RLDS_diff, clevs_rad, '(Wm$^{-2}$)', "(b) Downward LW Radiation  CM5NOS-NOS")
#Plot(2, 2, 4, LST_diff, clevs_lst, '(K)', "(d) Land Surface Temperature  CM5NOS-NOS")

Plot(2, 2, 1, RSDS_diff, clevs_rad, '(Wm$^{-2}$)', "(a) Downward SW Radiation   CM5NOS-SON")
Plot(2, 2, 2, NETRAD_diff, clevs_rad, '(Wm$^{-2}$)', "(c) Downward Net Radiation   CM5NOS-SON")
Plot(2, 2, 3, RLDS_diff, clevs_rad, '(Wm$^{-2}$)', "(b) Downward LW Radiation  CM5NOS-SON")
Plot(2, 2, 4, LST_diff, clevs_lst, '(K)', "(d) Land Surface Temperature  CM5NOS-SON")


fig.savefig('C:/Users/Jesse/Dropbox (UFL)/Jesse/Manuscript/figures/figure7.jpg', bbox_inches='tight', pad_inches = 0.1)
fig.savefig('C:/Users/Jesse/Dropbox (UFL)/Jesse/Manuscript/figures/figure7.pdf', bbox_inches='tight', pad_inches = 0.1)