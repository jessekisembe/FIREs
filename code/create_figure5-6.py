# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 06:49:45 2023

@author: Jesse
"""

import numpy as np
import pandas as pd
import xarray as xr
from matplotlib import pyplot as plt
import geocat.viz as gv


### function computes the seasonal cycle for the radiation fluxes and LST
def open_cesm_rad_cyc(file_path):

    #ds = xr.open_dataset(file_path).sel(lat=np.arange(-5,7,2),lon=np.arange(286,302,2),method='nearest') # South America winter
    ds = xr.open_dataset(file_path).sel(lat=np.arange(-5,7,2),lon=np.arange(15,31,2),method='nearest') # Central Africa winter
    ds.coords['lon']=(ds.coords['lon']+180)%360-180
    ds=ds.sortby(ds.lon)

    RSDS=ds.FSDS.groupby('time.month').mean('time').mean(('lat','lon'))
    RLDS=ds.FLDS.groupby('time.month').mean('time').mean(('lat','lon'))
   
    NETRAD=ds.FSNS+ds.FLDS
    NETRD=NETRAD.groupby('time.month').mean('time').mean(('lat','lon'))
    LST=ds.TS.groupby('time.month').mean('time').mean(('lat','lon'))
    
       
    return RSDS,RLDS,NETRD,LST
        
#open the files   
SON_RAD = open_cesm_rad_cyc('D:/data/CESM1/CESM1_SnowRad_atm_1980-2005_masked_2deg.nc')
NOS_RAD = open_cesm_rad_cyc('D:/data/CESM1/CESM1_NoSnowRad_atm_1980-2005_masked_2deg.nc')


## take the monthly differences 
RSDS   = NOS_RAD[0]-SON_RAD[0]
RLDS   = NOS_RAD[1]-SON_RAD[1]
NETRAD = NOS_RAD[2]-SON_RAD[2]
LST    = NOS_RAD[3]-SON_RAD[3]



### function computes the seasonal cycle for the radiation fluxes and LST
def open_cesm_rad_cyc_sd(file_path):

    #ds = xr.open_dataset(file_path).sel(lat=np.arange(-5,7,2),lon=np.arange(286,302,2),method='nearest') # South America winter
    ds = xr.open_dataset(file_path).sel(lat=np.arange(-5,7,2),lon=np.arange(15,31,2),method='nearest') # Central Africa winter
    ds.coords['lon']=(ds.coords['lon']+180)%360-180
    ds=ds.sortby(ds.lon)

    RSDS=ds.FSDS.groupby('time.month').std('time').mean(('lat','lon'))
    RLDS=ds.FLDS.groupby('time.month').std('time').mean(('lat','lon'))
   
    NETRAD=ds.FSNS+ds.FLDS
    NETRD=NETRAD.groupby('time.month').std('time').mean(('lat','lon'))
    LST=ds.TS.groupby('time.month').std('time').mean(('lat','lon'))
    
       
    return RSDS,RLDS,NETRD,LST

#open the files   
SON_RAD_SD = open_cesm_rad_cyc_sd('D:/data/CESM1/CESM1_SnowRad_atm_1980-2005_masked_2deg.nc')
NOS_RAD_SD = open_cesm_rad_cyc_sd('D:/data/CESM1/CESM1_NoSnowRad_atm_1980-2005_masked_2deg.nc')


## take the monthly differences 
RSDS_SD   = NOS_RAD_SD[0]-SON_RAD_SD[0]
RLDS_SD   = NOS_RAD_SD[1]-SON_RAD_SD[1]
NETRAD_SD = NOS_RAD_SD[2]-SON_RAD_SD[2]
LST_SD    = NOS_RAD_SD[3]-SON_RAD_SD[3]


####
data_RAD = {'Downward SW Radiation': RSDS.values,
            'Downward LW Radiation': RLDS.values,
            'Downward Net Radiation': NETRAD.values}

df_data_RAD = pd.DataFrame(data_RAD)


data_RAD_SD = {'Downward SW Radiation': RSDS_SD.values,
            'Downward LW Radiation': RLDS_SD.values,
            'Downward Net Radiation': NETRAD_SD.values}

df_data_RAD_SD = pd.DataFrame(data_RAD_SD)



### function computes the seasonal cycle for the properties relating to vegetation

def open_cesm_veg(file_path):

    #ds = xr.open_dataset(file_path).sel(lat=np.arange(-5,7,2),lon=np.arange(286,302,2),method='nearest') # South America winter
    ds = xr.open_dataset(file_path).sel(lat=np.arange(-5,7,2),lon=np.arange(15,31,2),method='nearest') # Central Africa winter
    ds.coords['lon']=(ds.coords['lon']+180)%360-180
    ds=ds.sortby(ds.lon)

    LAI = ds.TLAI.groupby('time.month').mean('time').mean(('lat','lon'))
    
    return LAI
        
#open the files   
SONN = open_cesm_veg('D:/data/CESM1/f09.CAM5.B-hist.land.mon.SON-CDO_2x2_1980_2005.nc')
NOSS = open_cesm_veg('D:/data/CESM1/f09.CAM5.B-hist.land.mon.NOS-CDO_2x2_1980_2005.nc')


def open_cesm_veg_sd(file_path):

    #ds = xr.open_dataset(file_path).sel(lat=np.arange(-5,7,2),lon=np.arange(286,302,2),method='nearest') # South America winter
    ds = xr.open_dataset(file_path).sel(lat=np.arange(-5,7,2),lon=np.arange(15,31,2),method='nearest') # Central Africa winter
    ds.coords['lon']=(ds.coords['lon']+180)%360-180
    ds=ds.sortby(ds.lon)

    LAI = ds.TLAI.groupby('time.month').std('time').mean(('lat','lon'))
    
    return LAI
        
#open the files   
SONN_SD = open_cesm_veg_sd('D:/data/CESM1/f09.CAM5.B-hist.land.mon.SON-CDO_2x2_1980_2005.nc')
NOSS_SD = open_cesm_veg_sd('D:/data/CESM1/f09.CAM5.B-hist.land.mon.NOS-CDO_2x2_1980_2005.nc')



def open_cesm_vegg_cyc(file_path):
    
    #ds = xr.open_dataset(file_path).sel(lat=np.arange(-5,7,2),lon=np.arange(286,302,2),method='nearest') # South America winter
    ds = xr.open_dataset(file_path).sel(lat=np.arange(-5,7,2),lon=np.arange(15,31,2),method='nearest') # Central Africa winter
    ds.coords['lon']=(ds.coords['lon']+180)%360-180
    ds=ds.sortby(ds.lon) 
    
    ETT= (abs(ds.QVEGE)+abs(ds.QVEGT))*86400 # canopy ET
    GPP = ds.GPP*86400
    NPP = abs(ds.NPP)*86400
    RP= (ds.GPP-ds.NPP)*86400 # Autrophic respiration
    
    
    ET = ETT.groupby('time.month').mean('time').mean(('lat','lon'))
    PHT=ds.FPSN.groupby('time.month').mean('time').mean(('lat','lon')) #photosynthesis
    GPP=GPP.groupby('time.month').mean('time').mean(('lat','lon')) #gross primary production
    NPP=NPP.groupby('time.month').mean('time').mean(('lat','lon'))
    REP=RP.groupby('time.month').mean('time').mean(('lat','lon'))
    
    return ET,PHT,GPP,REP,NPP
        
#open the files   
SON = open_cesm_vegg_cyc('D:/data/CESM1/Lmon/f09.B-hist.SON.land-CDO_2X2_1980_2005.nc')
NOS = open_cesm_vegg_cyc('D:/data/CESM1/Lmon/f09.B-hist.NOS.land-CDO_2X2_1980_2005.nc')


def open_cesm_vegg_cyc_sd(file_path):
    
    #ds = xr.open_dataset(file_path).sel(lat=np.arange(-5,7,2),lon=np.arange(286,302,2),method='nearest') # South America winter
    ds = xr.open_dataset(file_path).sel(lat=np.arange(-5,7,2),lon=np.arange(15,31,2),method='nearest') # Central Africa winter
    ds.coords['lon']=(ds.coords['lon']+180)%360-180
    ds=ds.sortby(ds.lon) 
    
    ETT= (abs(ds.QVEGE)+abs(ds.QVEGT))*86400 # canopy ET
    GPP = ds.GPP*86400
    NPP = abs(ds.NPP)*86400
    RP= (ds.GPP-ds.NPP)*86400 # Autrophic respiration
    
    
    ET = ETT.groupby('time.month').std('time').mean(('lat','lon'))
    PHT=ds.FPSN.groupby('time.month').std('time').mean(('lat','lon')) #photosynthesis
    GPP=GPP.groupby('time.month').std('time').mean(('lat','lon')) #gross primary production
    NPP=NPP.groupby('time.month').std('time').mean(('lat','lon'))
    REP=RP.groupby('time.month').std('time').mean(('lat','lon'))
    
    return ET,PHT,GPP,REP,NPP
        
#open the files   
SON_SD = open_cesm_vegg_cyc_sd('D:/data/CESM1/Lmon/f09.B-hist.SON.land-CDO_2X2_1980_2005.nc')
NOS_SD = open_cesm_vegg_cyc_sd('D:/data/CESM1/Lmon/f09.B-hist.NOS.land-CDO_2X2_1980_2005.nc')


#compute for the difference in the variables
LAI = NOSS-SONN
ET  = NOS[0] - SON[0]
PHT = NOS[1] - SON[1]
GPP = NOS[2] - SON[2]
REP = NOS[3] - SON[3]
NPP = NOS[4] - SON[4]

####
data_VEG = {'Gross Primary Production': GPP.values,
            'Autotrophic Respiration': REP.values,
            'Net Primary Production': NPP.values,
            'Total Leaf Area Index': LAI.values}

df_data_VEG = pd.DataFrame(data_VEG)

#standard deviation differences...
LAI_SD = NOSS_SD-SONN_SD
ET_SD  = NOS_SD[0] - SON_SD[0]
PHT_SD = NOS_SD[1] - SON_SD[1]
GPP_SD = NOS_SD[2] - SON_SD[2]
REP_SD = NOS_SD[3] - SON_SD[3]
NPP_SD = NOS_SD[4] - SON_SD[4]

####
data_VEG_SD = {'Gross Primary Production': GPP_SD.values,
            'Autotrophic Respiration': REP_SD.values,
            'Net Primary Production': NPP_SD.values,
            'Total Leaf Area Index': LAI_SD.values}

df_data_VEG_SD = pd.DataFrame(data_VEG_SD)



def open_cesm_land(file_path):
    
    #ds = xr.open_dataset(file_path).sel(lat=np.arange(-5,7,2),lon=np.arange(286,302,2),method='nearest') # South America winter
    ds = xr.open_dataset(file_path).sel(lat=np.arange(-5,7,2),lon=np.arange(15,31,2),method='nearest') # Central Africa winter
    ds.coords['lon']=(ds.coords['lon']+180)%360-180
    ds=ds.sortby(ds.lon) 
    
    ##-- group data into yearly means from seasons

    GRTM=ds.TG.groupby('time.month').mean('time').mean(('lat','lon')) #ground temperature
    TEMP=ds.TSA.groupby('time.month').mean('time').mean(('lat','lon')) #2m air temperature
    GEVP=ds.QSOIL.groupby('time.month').mean('time').mean(('lat','lon')) #ground evaporation
    GEVP=GEVP*86400
    SPHM=ds.Q2M.groupby('time.month').mean('time').mean(('lat','lon')) # 2m specific humidity
    SPHM=SPHM*1000
    SOM=ds.SOILLIQ.sel(levgrnd=slice('0.007101')).groupby('time.month').mean('time').mean(('lat','lon')) # soil liquid water
    SOM = np.squeeze(SOM)
    
    return GRTM,TEMP,GEVP,SPHM,SOM
        
#open the files   
SONL = open_cesm_land('D:/data/CESM1/Lmon/f09.B-hist.SON.land-CDO_2X2_1980_2005.nc')
NOSL = open_cesm_land('D:/data/CESM1/Lmon/f09.B-hist.NOS.land-CDO_2X2_1980_2005.nc')


def open_cesm_land_sd(file_path):
    
    #ds = xr.open_dataset(file_path).sel(lat=np.arange(-5,7,2),lon=np.arange(286,302,2),method='nearest') # South America winter
    ds = xr.open_dataset(file_path).sel(lat=np.arange(-5,7,2),lon=np.arange(15,31,2),method='nearest') # Central Africa winter
    ds.coords['lon']=(ds.coords['lon']+180)%360-180
    ds=ds.sortby(ds.lon) 
    
    ##-- group data into yearly means from seasons

    GRTM=ds.TG.groupby('time.month').std('time').mean(('lat','lon')) #ground temperature
    TEMP=ds.TSA.groupby('time.month').std('time').mean(('lat','lon')) #2m air temperature
    GEVP=ds.QSOIL.groupby('time.month').std('time').mean(('lat','lon')) #ground evaporation
    GEVP=GEVP*86400
    SPHM=ds.Q2M.groupby('time.month').std('time').mean(('lat','lon')) # 2m specific humidity
    SPHM=SPHM*1000
    SOM=ds.SOILLIQ.sel(levgrnd=slice('0.007101')).groupby('time.month').std('time').mean(('lat','lon')) # soil liquid water
    SOM = np.squeeze(SOM)
        
    return GRTM,TEMP,GEVP,SPHM,SOM
        
#open the files   
SONL = open_cesm_land('D:/data/CESM1/Lmon/f09.B-hist.SON.land-CDO_2X2_1980_2005.nc')
NOSL = open_cesm_land('D:/data/CESM1/Lmon/f09.B-hist.NOS.land-CDO_2X2_1980_2005.nc')

#compute for the difference in the variables
GRTM = NOSL[0] - SONL[0]
TEMP = NOSL[1] - SONL[1]
GEVP = NOSL[2] - SONL[2]
SPHM = NOSL[3] - SONL[3]
SOM  = NOSL[4] - SONL[4]



#open the files   
SONL_SD = open_cesm_land_sd('D:/data/CESM1/Lmon/f09.B-hist.SON.land-CDO_2X2_1980_2005.nc')
NOSL_SD = open_cesm_land_sd('D:/data/CESM1/Lmon/f09.B-hist.NOS.land-CDO_2X2_1980_2005.nc')

#compute for the difference in the variables
GRTM_SD = NOSL_SD[0] - SONL_SD[0]
TEMP_SD = NOSL_SD[1] - SONL_SD[1]
GEVP_SD = NOSL_SD[2] - SONL_SD[2]
SPHM_SD = NOSL_SD[3] - SONL_SD[3]
SOM_SD  = NOSL_SD[4] - SONL_SD[4]



####
data_LND = {'Land Surface Temperature': LST.values,
            'Air Temperature': TEMP.values,
            #'Ground Temperature': GRTM.values,
            'Canopy ET': ET.values}

df_data_LND = pd.DataFrame(data_LND)


####
data_SNW = {'Soil Liquid': SOM.values}

df_data_SNW = pd.DataFrame(data_SNW)



####
data_LND_SD = {'Land Surface Temperature': LST_SD.values,
            'Air Temperature': TEMP_SD.values,
            'Canopy ET': ET_SD.values}

df_data_LND_SD = pd.DataFrame(data_LND_SD)


####
data_SNW_SD = {'Soil Liquid': SOM_SD.values}

df_data_SNW_SD = pd.DataFrame(data_SNW_SD)


# plot data
# font settings
s = 25
font = {'weight' : 'normal',
        'size'   : s,
        'serif': 'Arial'}

plt.rc('font', **font)
plt.rc('axes', linewidth=1)

# figure set up
fig = plt.figure(figsize=(25,19),dpi=300)
plt.gcf().subplots_adjust(hspace=0.3, wspace=0.4)


ax1 = fig.add_subplot(221)
ax2 = fig.add_subplot(222)
ax3 = fig.add_subplot(223)
ax4 = fig.add_subplot(224)

ax_list = [ax1, ax2, ax3, ax4]

for ax in ax_list:
    ax.set_xticks(range(1, 12+1))
    ax.set_xticklabels(['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'])
    ax.axhline(y = 0, color = 'grey', linestyle = 'dashed')
    ax.set_xlim(1,12)

x = range(1,12+1)


# Panel 1
ax1.set_ylim(-8,8)

namelist = []
lines    = []

cols = ['red','blue','black']
j=0

for ds in df_data_RAD.columns:
    y = df_data_RAD[ds].values
    
    lines += ax1.plot(x, y, ls='-', color = cols[j], marker = 'o', lw=2)
    

    j=j+1
        
    namelist.append(ds)

for i, var in enumerate(df_data_RAD.columns):
    ax1.errorbar(x, df_data_RAD[var], yerr=np.abs(df_data_RAD_SD[var]), fmt='-o', color=['red','blue','black'][i],
                 markersize=1, capsize=3, elinewidth=2, capthick=2)
    
    
##--Panel 2
axa = ax2.twinx() 
ax2.set_ylim(-0.6,0.6)
axa.set_ylim(-0.2,0.2)

namelist_lnd = []
lines_lnd    = []

cols_lnd = ['black','red']
j=0

for ds in df_data_LND.columns:
    #print(ds)
    y = df_data_LND[ds].values
    
    if ds == 'Canopy ET' :
        lines_lnd += axa.plot(x, y, ls='-', color = 'green', marker = 'o', lw=2)
    else:
        lines_lnd+= ax2.plot(x, y, ls='-', color = cols_lnd[j], marker = 'o', lw=2)

    j=j+1
        
    namelist_lnd.append(ds)

for i, var in enumerate(df_data_LND.columns):
    
    if var == 'Canopy ET':
        axa.errorbar(x, df_data_LND[var], yerr=np.abs(df_data_LND_SD[var]), fmt='-o', color='green',
                     markersize=1, capsize=3, elinewidth=2, capthick=2)
    else:  
        ax2.errorbar(x, df_data_LND[var], yerr=np.abs(df_data_LND_SD[var]), fmt='-o', color=['black','red'][i],
                 markersize=1, capsize=3, elinewidth=2, capthick=2)


##-- Panel 3
 
ax3.set_ylim(-0.3,0.3)

namelist_snw = []
lines_snw    = []

cols_snw = ['lightseagreen']
k=0

for ds in df_data_SNW.columns:
    y = df_data_SNW[ds].values
      
    lines_snw += ax3.plot(x, y, ls='-', color = cols_snw[k], marker = 'o', lw=2)
    k=k+1

    namelist_snw.append(ds)

for i, var in enumerate(df_data_SNW.columns):
    ax3.errorbar(x, df_data_SNW[var], yerr=np.abs(df_data_SNW_SD[var]), fmt='-o', color=['lightseagreen'][i],
                 markersize=1, capsize=3, elinewidth=2, capthick=2)
        
        

##-- Panel 4
axx = ax4.twinx()     
ax4.set_ylim(-0.5,0.5)
axx.set_ylim(-0.28,0.28)

namelist_veg = []
lines_veg    = []

cols_veg = ['lightseagreen','purple','yellowgreen']
k=0

for ds in df_data_VEG.columns:
    y = df_data_VEG[ds].values
    
    if ds == 'Total Leaf Area Index' :
        lines_veg += axx.plot(x, y, ls='-', color = 'green', marker = 'o', lw=2)
           
    else:        
        lines_veg += ax4.plot(x, y, ls='-', color = cols_veg[k], marker = 'o', lw=2)
        
        k=k+1
        
    namelist_veg.append(ds)

for i, var in enumerate(df_data_VEG.columns):
    
    if var == 'Total Leaf Area Index':
        axx.errorbar(x, df_data_VEG[var], yerr=np.abs(df_data_VEG_SD[var]), fmt='-o', color='green',
                     markersize=1, capsize=3, elinewidth=2, capthick=2)
    else:  
        ax4.errorbar(x, df_data_VEG[var], yerr=np.abs(df_data_VEG_SD[var]), fmt='-o', color=['lightseagreen','purple','yellowgreen'][i],
                 markersize=1, capsize=3, elinewidth=2, capthick=2)



#plt.grid()
ax1.set_ylabel('Radiation flux (Wm$^{-2}$)', fontsize=26)
#axx.set_ylabel('TLAI', fontsize=26, color='g')
ax2.set_ylabel('Temperature (K)', fontsize=26)
ax3.set_ylabel('Soil moisture state (kg m$^{-2}$)', fontsize=26)
ax3.set_xlabel('Months', fontsize=26)
axa.set_ylabel('Canopy ET (mm day$^{-1}$)', fontsize=26, color='green')
ax4.set_ylabel('Carbon mass flux (g C m$^{-2} day^{-1}$)', fontsize=26)
ax4.set_xlabel('Months', fontsize=26)

gv.set_titles_and_labels(ax1, lefttitle="(a) Surface Radiation Fluxes", lefttitlefontsize=30)
gv.set_titles_and_labels(ax2, lefttitle="(b) Temperature & Canopy Evapotranspiration", lefttitlefontsize=30)
gv.set_titles_and_labels(ax3, lefttitle="(c) Soil Moisture State", lefttitlefontsize=30)
gv.set_titles_and_labels(ax4, lefttitle="(d) Vegetation Properties", lefttitlefontsize=30)

axx.tick_params(axis='y', colors='green')
axa.tick_params(axis='y', colors='green')

ax1.legend(lines, namelist, ncol=1, loc = 'lower left', labelcolor='linecolor', frameon = False)
ax2.legend(lines_lnd, namelist_lnd, ncol=1, loc = 'lower left', labelcolor='linecolor', frameon = False)
ax3.legend(lines_snw, namelist_snw, ncol=1, loc = 'lower left', labelcolor='linecolor', frameon = False)
ax4.legend(lines_veg, namelist_veg, ncol=1, loc = 'lower left', labelcolor='linecolor', frameon = False)

# Add a suptitle
#fig.suptitle('South America', fontsize=48, y=0.95)
fig.suptitle('Central Africa', fontsize=48, y=0.95)

#fig.savefig('C:/Users/Jesse/Dropbox (UFL)/Jesse/Manuscript/figures/figure5.jpg', bbox_inches='tight', pad_inches = 0.1)
#fig.savefig('C:/Users/Jesse/Dropbox (UFL)/Jesse/Manuscript/figures/figure5.pdf', bbox_inches='tight', pad_inches = 0.1)

fig.savefig('C:/Users/Jesse/Dropbox (UFL)/Jesse/Manuscript/figures/figure6.jpg', bbox_inches='tight', pad_inches = 0.1)
fig.savefig('C:/Users/Jesse/Dropbox (UFL)/Jesse/Manuscript/figures/figure6.pdf', bbox_inches='tight', pad_inches = 0.1)
