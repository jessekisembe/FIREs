# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 18:31:32 2023

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



def open_cesm_land(file_path):
    
    ds = xr.open_dataset(file_path)
    ds.coords['lon']=(ds.coords['lon']+180)%360-180
    ds=ds.sortby(ds.lon) 
    
    ##-- group data into yearly means from seasons

    GRTM=ds.TG.groupby('time.season').mean('time').sel(season='DJF') #ground temperature
    TEMP=ds.TSA.groupby('time.season').mean('time').sel(season='DJF') #2m air temperature
    GEVP=ds.QSOIL.groupby('time.season').mean('time').sel(season='DJF') #ground evaporation
    GEVP=GEVP*86400
    SPHM=ds.Q2M.groupby('time.season').mean('time').sel(season='DJF') # 2m specific humidity
    SPHM=SPHM*1000
    SOM=ds.SOILLIQ.sel(levgrnd=slice('0.007101')).groupby('time.season').mean('time').sel(season='DJF') # soil liquid water
    SOM = np.squeeze(SOM, axis=0)
    SOI=ds.SOILICE.sel(levgrnd=slice('0.007101')).groupby('time.season').mean('time').sel(season='DJF') # soil ice
    SOI = np.squeeze(SOI, axis=0)
    SNC=ds.FSNO.groupby('time.season').mean('time').sel(season='DJF') # snow cover
    SNC=SNC*100
    SND=ds.H2OSNO.groupby('time.season').mean('time').sel(season='DJF') # snow depth
    SND=SND*0.1 #conversion from mm to cm
        
    return GRTM,TEMP,GEVP,SPHM,SOM,SOI,SNC,SND
        
#open the files   
SON = open_cesm_land('D:/data/CESM1/Lmon/f09.B-hist.SON.land-CDO_2X2_1980_2005.nc')
NOS = open_cesm_land('D:/data/CESM1/Lmon/f09.B-hist.NOS.land-CDO_2X2_1980_2005.nc')

#compute for the difference in the variables
GRTM_diff = NOS[0] - SON[0]
TEMP_diff = NOS[1] - SON[1]
GEVP_diff = NOS[2] - SON[2]
SPHM_diff = NOS[3] - SON[3]
SOM_diff  = NOS[4] - SON[4]
SOI_diff  = NOS[5] - SON[5]
SNC_diff  = NOS[6] - SON[6]
SND_diff  = NOS[7] - SON[7]



def open_cesm_diff_sig(file_path):

    ds = xr.open_dataset(file_path)
    ds.coords['lon']=(ds.coords['lon']+180)%360-180
    ds=ds.sortby(ds.lon)

    diff_sig=ds.sig
        
    return diff_sig
        
#open the siginificance files    
Path = "D:/data/CESM1/seas/diff/land/"

GRTM_diff_sig = open_cesm_diff_sig(Path+"GroundTemp_pvalue_NOS_SON_diff_1980-2005_2deg_DJF.nc")
TEMP_diff_sig = open_cesm_diff_sig(Path+"AirTemp_pvalue_NOS_SON_diff_1980-2005_2deg_DJF.nc")
GEVP_diff_sig = open_cesm_diff_sig(Path+"GroundEvap_pvalue_NOS_SON_diff_1980-2005_2deg_DJF.nc")
SPHM_diff_sig = open_cesm_diff_sig(Path+"Sphumid_pvalue_NOS_SON_diff_1980-2005_2deg_DJF.nc")
SOM_diff_sig  = open_cesm_diff_sig(Path+"Soilliq_pvalue_NOS_SON_diff_1980-2005_2deg_DJF.nc")
SOI_diff_sig  = open_cesm_diff_sig(Path+"Soilice_pvalue_NOS_SON_diff_1980-2005_2deg_DJF.nc")
SNC_diff_sig  = open_cesm_diff_sig(Path+"Snowcover_pvalue_NOS_SON_diff_1980-2005_2deg_DJF.nc")
SND_diff_sig  = open_cesm_diff_sig(Path+"Snowdepth_pvalue_NOS_SON_diff_1980-2005_2deg_DJF.nc")


##----------------------------------------------------------------------------------------------------------------------------

def open_cesm_veg(file_path):

    ds = xr.open_dataset(file_path)
    ds.coords['lon']=(ds.coords['lon']+180)%360-180
    ds=ds.sortby(ds.lon)

    LAI = ds.TLAI
    
    return LAI
        
#open the files   
SONN = open_cesm_veg('D:/data/CESM1/CESM1_SnowRad_land_1970-2005_DJF_2deg.nc')
NOSS = open_cesm_veg('D:/data/CESM1/CESM1_NoSnowRad_land_1970-2005_DJF_2deg.nc')

#compute for the difference in the variables
LAI_diff  = NOSS[0] - SONN[0]




def open_cesm_vegg(file_path):
    
    ds = xr.open_dataset(file_path)
    ds.coords['lon']=(ds.coords['lon']+180)%360-180
    ds=ds.sortby(ds.lon) 
    
    ##-- group data into  seasons
    ETT= abs(ds.QVEGE)+abs(ds.QVEGT) # canopy ET
    ET = ETT.groupby('time.season').mean('time').sel(season='DJF')
    PHT=ds.FPSN.groupby('time.season').mean('time').sel(season='DJF') #photosynthesis
    GPP=ds.GPP.groupby('time.season').mean('time').sel(season='DJF') #gross primary production
    NPPP=abs(ds.NPP) #net primary production
    NPP=NPPP.groupby('time.season').mean('time').sel(season='DJF')
    
    RP= ds.GPP-ds.NPP # Autrophic respiration
    REP=RP.groupby('time.season').mean('time').sel(season='DJF')
    
    
    ET  = ET*86400
    GPP = GPP*86400
    NPP = NPP*86400
    REP = REP*86400
    
    return ET,PHT,GPP,REP,NPP
        
#open the files   
SONN = open_cesm_vegg('D:/data/CESM1/Lmon/f09.B-hist.SON.land-CDO_2X2_1980_2005.nc')
NOSS = open_cesm_vegg('D:/data/CESM1/Lmon/f09.B-hist.NOS.land-CDO_2X2_1980_2005.nc')

#compute for the difference in the variables
ET_diff  = NOSS[0] - SONN[0]
PHT_diff = NOSS[1] - SONN[1]
GPP_diff = NOSS[2] - SONN[2]
REP_diff = NOSS[3] - SONN[3]
NPP_diff = NOSS[4] - SONN[4]


def open_cesm_diff_sig(file_path):

    ds = xr.open_dataset(file_path)
    ds.coords['lon']=(ds.coords['lon']+180)%360-180
    ds=ds.sortby(ds.lon)

    diff_sig=ds.sig
        
    return diff_sig
        
#open the siginificance files    
Pathh = "D:/data/CESM1/seas/diff/land/"

LAI_diff_sig = open_cesm_diff_sig(Pathh+"LAI_pvalue_NOS_SON_diff_1980-2005_2deg_DJF.nc")
ET_diff_sig  = open_cesm_diff_sig(Pathh+"CanopyET_pvalue_NOS_SON_diff_1980-2005_2deg_DJF.nc")
PHT_diff_sig = open_cesm_diff_sig(Pathh+"Photosynthesis_pvalue_NOS_SON_diff_1980-2005_2deg_DJF.nc")
GPP_diff_sig = open_cesm_diff_sig(Pathh+"GPP_pvalue_NOS_SON_diff_1980-2005_2deg_DJF.nc")
REP_diff_sig  = open_cesm_diff_sig(Pathh+"AutrophicRespiration_pvalue_NOS_SON_diff_1980-2005_2deg_DJF.nc")
NPP_diff_sig  = open_cesm_diff_sig(Pathh+"NPP_pvalue_NOS_SON_diff_1980-2005_2deg_DJF.nc")



##----------------------------------------------------------------------------------------------------------------------------
## plotting
# Create a wider than normal figure to support our many plots
fig = plt.figure(figsize=(22,27),dpi=300)
plt.gcf().subplots_adjust(hspace=0.4, wspace=0.0)
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
       
    # Add color bar
    cbar = plt.colorbar(temp,
                        orientation='vertical',
                        shrink=1,
                        extendfrac='auto', 
                        extendrect=True, 
                        drawedges=True)

    cbar.ax.tick_params(labelsize=18)
    cbar.set_ticks(clevs)
    cbar.ax.set_title(cbar_label, size=18)
    
    
    # Define a custom formatter function
    def custom_formatter(x, pos):
        if x in [-10, -5, -4, -2, -1, 1, 2, 4, 5, 10]:
            return f'{int(x)}'  # Format -1 and 1 without decimal places
        elif x in [-0.5, -0.3, -0.2, -0.1, 0.1, 0.2, 0.3, 0.5]:
            return f'{x:.1f}'  # Format these values with one decimal place
        elif x in [-0.25, -0.01, -0.05, 0.05, 0.01, 0.25]:
            return f'{x:.2f}'  # Format these values with two decimal places
        elif x in [-0.001, 0.001]:
            return f'{x:.3f}'  # Format these values with three decimal places
        else:
            return f'{x}'  # Default case (if any)
    cbar.ax.yaxis.set_major_formatter(ticker.FuncFormatter(custom_formatter))

    # Use geocat.viz.util convenience function to set titles and labels without calling several matplotlib functions
    gv.set_titles_and_labels(ax,
                            maintitle="",
                            lefttitle=title,
                            lefttitlefontsize=24,
                            righttitle="",
                            righttitlefontsize=19,
                            xlabel="",
                            ylabel="")


# define the levels for each variable
clevs_temp  = [-4, -2, -1, -0.5, -0.1, 0.1, 0.5, 1, 2, 4]
clevs_som = [-1, -0.5, -0.1, -0.05, -0.01, 0.01, 0.05, 0.1, 0.5, 1]
clevs_snc = [-10, -5, -2, -1, -0.01, 0.01, 1, 2, 5, 10]
clevs_lai = [-1, -0.5, -0.1, -0.05, -0.01, 0.01, 0.05, 0.1, 0.5, 1]
clevs_npp = [-0.3, -0.2, -0.1, -0.05, -0.001, 0.001, 0.05, 0.1, 0.2, 0.3]
clevs_et  = [-0.25, -0.1, -0.05, -0.01, -0.001, 0.001, 0.01, 0.05, 0.1, 0.25]


### Plotting....

Plot(5, 2, 1, TEMP_diff, TEMP_diff_sig, clevs_temp, '(K)', "(a) Air Temperature   NOS-SON")
Plot(5, 2, 2, ET_diff,  ET_diff_sig, clevs_et, '(mm day$^{-1}$)', "(f) Canopy Evapotranspiration  NOS-SON")
Plot(5, 2, 3, SOM_diff, SOM_diff_sig, clevs_som, '(kg m$^{-2}$)', "(b) Soil Liquid   NOS-SON")
Plot(5, 2, 4, GPP_diff, GPP_diff_sig, clevs_npp, '(g C m$^{-2} day^{-1}$)', "(g) Gross Primary Production  NOS-SON")
Plot(5, 2, 5, SOI_diff, SOI_diff_sig, clevs_som, '(kg m$^{-2}$)', "(c) Soil Ice   NOS-SON")
Plot(5, 2, 6, REP_diff, REP_diff_sig, clevs_npp, '(g C m$^{-2} day^{-1}$)', "(h) Autotrophic Respiration  NOS-SON")
Plot(5, 2, 7, SNC_diff, SNC_diff_sig, clevs_snc, '(%)', "(d) Snow Cover   NOS-SON")
Plot(5, 2, 8, NPP_diff, NPP_diff_sig, clevs_npp, '(g C m$^{-2} day^{-1}$)', "(i) Net Primary Production  NOS-SON")
Plot(5, 2, 9, LAI_diff, LAI_diff_sig, clevs_lai, '', "(e) Total Leaf Area Index  NOS-SON")



fig.savefig('C:/Users/Jesse/Dropbox (UFL)/Jesse/Manuscript/figures/figure2.jpg', bbox_inches='tight', pad_inches = 0.1)
fig.savefig('C:/Users/Jesse/Dropbox (UFL)/Jesse/Manuscript/figures/figure2.pdf', bbox_inches='tight', pad_inches = 0.1)