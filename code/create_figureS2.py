# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 13:24:20 2023

@author: Jesse
"""


import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter


## plotting
# Create a wider than normal figure to support our many plots
fig = plt.figure(figsize=(12,6),dpi=300)
plt.gcf().subplots_adjust(hspace=0.1, wspace=0.1)
plt.rcParams["font.family"] = "Arial"

ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=-180))
ax.stock_img()
ax.coastlines()

plt.gca().set_yticks(np.arange(-60,90,30),crs=ccrs.PlateCarree())
plt.gca().set_xticks(np.arange(-120,240,60),crs=ccrs.PlateCarree())
lon_formatter=LongitudeFormatter(degree_symbol=''); lat_formatter=LatitudeFormatter(degree_symbol='')
ax.xaxis.set_major_formatter(lon_formatter); ax.yaxis.set_major_formatter(lat_formatter);ax.tick_params(labelsize=16)
xticks = ax.xaxis.get_major_ticks(); xticks[2].set_visible(False)

### -- draw rectangle
#ax.add_patch(plt.Rectangle(((60),(30)),30,15,edgecolor='red',fill=False, lw=2.5)) ### North America summer
#ax.add_patch(plt.Rectangle(((-120),(40)),30,15,edgecolor='red',fill=False, lw=2.5)) ### Eurasia summer

ax.add_patch(plt.Rectangle(((105),(-5)),15,10,edgecolor='green',fill=False, lw=2.5)) ### South America summer
ax.add_patch(plt.Rectangle(((-165),(-5)),15,10,edgecolor='blue',fill=False, lw=2.5)) ### Central Africa  summer

ax.add_patch(plt.Rectangle(((60),(50)),30,15,edgecolor='red',fill=False, lw=2.5)) ### North America winter
ax.add_patch(plt.Rectangle(((-90),(50)),30,15,edgecolor='magenta',fill=False, lw=2.5)) ### Eurasia  winter


ax.grid(linestyle="--")
plt.show()

# Save the plot by calling plt.savefig() BEFORE plt.show()
#plt.savefig('coastlines.pdf')
#fig.savefig('D:/plots/NorthAmerica_sig_JJA.png', bbox_inches='tight', pad_inches = 0.1)
#fig.savefig('D:/plots/Eurasia_sig_JJA.png', bbox_inches='tight', pad_inches = 0.1)

#fig.savefig('D:/plots/SouthAmerica_sig_JJA.png', bbox_inches='tight', pad_inches = 0.1)
#fig.savefig('D:/plots/CentralAfrica_sig_JJA.png', bbox_inches='tight', pad_inches = 0.1)

fig.savefig('C:/Users/Jesse/Dropbox (UFL)/Jesse/Manuscript/figures/Figure_S2_regions.jpg', bbox_inches='tight', pad_inches = 0.1)
fig.savefig('C:/Users/Jesse/Dropbox (UFL)/Jesse/Manuscript/figures/Figure_S2_regions.pdf', bbox_inches='tight', pad_inches = 0.1)

