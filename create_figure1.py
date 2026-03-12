# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 20:40:40 2023

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
        
#open the files   
SON = open_cesm_atm('D:/data/CESM1/CESM1_SnowRad_atm_1980-2005_masked_2deg.nc')
NOS = open_cesm_atm('D:/data/CESM1/CESM1_NoSnowRad_atm_1980-2005_masked_2deg.nc')


#compute for the difference in the variables
RSDS_diff   = NOS[0] - SON[0]
RLDS_diff   = NOS[1] - SON[1]
NETRAD_diff = NOS[2] - SON[2]
LST_diff    = NOS[3] - SON[3]


def open_cesm_diff_sig(file_path):

    ds = xr.open_dataset(file_path)
    ds.coords['lon']=(ds.coords['lon']+180)%360-180
    ds=ds.sortby(ds.lon)

    diff_sig=ds.sig
        
    return diff_sig
        
#open the siginificance files    
Path = "D:/data/CESM1/seas/diff/"

RSDS_diff_sig = open_cesm_diff_sig(Path+"rsds_pvalue_NOS_SON_diff_1980-2005_2deg_DJF.nc")
RLDS_diff_sig = open_cesm_diff_sig(Path+"rlds_pvalue_NOS_SON_diff_1980-2005_2deg_DJF.nc")
NETRAD_diff_sig = open_cesm_diff_sig(Path+"netRAD_pvalue_NOS_SON_diff_1980-2005_2deg_DJF.nc")
LST_diff_sig = open_cesm_diff_sig(Path+"lst_pvalue_NOS_SON_diff_1980-2005_2deg_DJF.nc")



## plotting
# Create a wider than normal figure to support our many plots
fig = plt.figure(figsize=(24,12),dpi=300)
plt.gcf().subplots_adjust(hspace=0.1, wspace=0.1)
plt.rcParams["font.family"] = "Arial"


def Plot(row, col, pos, diff, diff_sig, clevs, cbar_label, title):

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
    
    # Plot Hatch
    pval = diff_sig
    cond = (pval <= 0.05)
    ## Mask out the areas that do not satisfy the conditions
    sig = pval.where(cond)
    
    ## make a hatch of significance
    plt.contourf(sig.lon,sig.lat,sig,hatches=['xxx'],alpha=0,
                 transform=ccrs.PlateCarree()) 
    
    ### -- draw rectangle
    #ax.add_patch(plt.Rectangle(((60),(30)),30,15,edgecolor='k',fill=False, lw=2.5)) ### North America summer
    #ax.add_patch(plt.Rectangle(((-120),(40)),30,15,edgecolor='k',fill=False, lw=2.5)) ### Eurasia summer
    #ax.add_patch(plt.Rectangle(((105),(-5)),15,10,edgecolor='k',fill=False, lw=2.5)) ### South America summer
    #ax.add_patch(plt.Rectangle(((-165),(-5)),15,10,edgecolor='k',fill=False, lw=2.5)) ### Central Africa  summer
    
    #ax.add_patch(plt.Rectangle(((60),(50)),30,15,edgecolor='r',fill=False, lw=3)) ### North America winter
    #ax.add_patch(plt.Rectangle(((-90),(50)),30,15,edgecolor='r',fill=False, lw=3)) ### Eurasia  winter
    #ax.add_patch(plt.Rectangle(((105),(-5)),15,10,edgecolor='r',fill=False, lw=3)) ### South America winter
    #ax.add_patch(plt.Rectangle(((-165),(-5)),15,10,edgecolor='r',fill=False, lw=3)) ### Central Africa  winter

    
    
    # Add color bar
    cbar = plt.colorbar(temp,
                        orientation='vertical',
                        shrink=0.8,
                        extendfrac='auto', 
                        extendrect=True, 
                        drawedges=True)

    cbar.ax.tick_params(labelsize=18)
    cbar.set_ticks(clevs)
    cbar.ax.set_title(cbar_label, size=19)
    
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
                            lefttitlefontsize=25,
                            righttitle="",
                            righttitlefontsize=22,
                            xlabel="",
                            ylabel="")


# define the levels for each variable
clevs_rad  = [-15, -10, -5, -2, -0.5, 0.5, 2, 5, 10, 15]
clevs_lst  = [-4, -2, -1, -0.5, -0.1, 0.1, 0.5, 1, 2, 4]

Plot(2, 2, 1, RSDS_diff, RSDS_diff_sig, clevs_rad, '(Wm$^{-2}$)', "(a) Downward SW Radiation   NOS-SON")
Plot(2, 2, 2, NETRAD_diff, NETRAD_diff_sig, clevs_rad, '(Wm$^{-2}$)', "(c) Downward Net Radiation   NOS-SON")
Plot(2, 2, 3, RLDS_diff, RLDS_diff_sig, clevs_rad, '(Wm$^{-2}$)', "(b) Downward LW Radiation  NOS-SON")
Plot(2, 2, 4, LST_diff, LST_diff_sig, clevs_lst, '(K)', "(d) Land Surface Temperature  NOS-SON")


fig.savefig('C:/Users/Jesse/Dropbox (UFL)/Jesse/Manuscript/figures/figure1.jpg', bbox_inches='tight', pad_inches = 0.1)
fig.savefig('C:/Users/Jesse/Dropbox (UFL)/Jesse/Manuscript/figures/figure1.pdf', bbox_inches='tight', pad_inches = 0.1)