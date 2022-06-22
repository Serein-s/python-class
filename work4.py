from cartopy.util import add_cyclic_point
import cartopy.feature as cfeature
import matplotlib
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import numpy as np
#防止中文出错
matplotlib.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

data=xr.open_dataset(r"D:\data\py_class\data\mslp.mon.mean.nc", drop_variables=["time_bnds"])
slp= data.mslp.loc[data.time.dt.month.isin([12])].loc['1990-12-01':'2020-12-01']/100.
ave_slp= np.array(slp).reshape(31, 73, 144).mean(0)  #求气候态
slp_2015= data.mslp.loc[data.time.dt.month.isin([12])].loc['2015-12-01']/100.
abn=slp_2015-ave_slp
#除去0和360处空白
def cyclic_data(data,lon,lat):
    c_data, cycle_lon = add_cyclic_point(data, coord=lon)
    LON, LAT = np.meshgrid(cycle_lon,lat)    
    return c_data,LON, LAT

#Robinson底图
def contour_map(ax,img_extent,cmaps,data,lon,lat):
    ax.set_extent(img_extent, crs=ccrs.Robinson())
    ax.set_global()
    ax.add_feature(cfeature.LAND, facecolor='lightgrey')
    ax.add_feature(cfeature.OCEAN, facecolor='white')
    ax.add_feature(cfeature.COASTLINE.with_scale('50m'))
    ax.add_feature(cfeature.LAKES, alpha=0.5)
    ax.add_feature(cfeature.RIVERS)
    #gl=ax.gridlines(draw_labels=True, color='gray', alpha=0.5, linestyle=':')
   # gl.top_labels = False
    #gl.right_labels = False
    # 绘制等值线图
    contour = ax.contourf(lon,lat,data,levels=14,cmap=cmaps,transform=ccrs.PlateCarree(), extend = 'both')
    ax.contour(lon,lat,data,levels=14,colors='k',transform=ccrs.PlateCarree(),linewidths=0.5)    
    cb=plt.colorbar(contour,shrink=0.65,pad=0.02)#色标
    cb.ax.set_title('hPa',fontsize=12)
    
leftlon, rightlon, lowerlat, upperlat = (-180, 180, -90, 90)
img_extent = [leftlon, rightlon, lowerlat, upperlat]  #经纬度范围

# 生成画布
fig = plt.figure(figsize=(8,14))
#plt.subplots_adjust(hspace=0.4)#子图间距
ax1 = fig.add_subplot(3, 1, 1, projection=ccrs.Robinson(central_longitude=150))

c_slp,lon,lat=cyclic_data(ave_slp,slp.lon,slp.lat)
contour_map(ax1, img_extent,'RdBu_r',c_slp,lon,lat)
ax1.set_title('1990-2020年12月的平均SLP图（气候态）',fontsize=12)  #设置标签
ax1.set_title(' (a) ', loc='left', fontsize=12)
#ax1.margins(0)
ax2 = fig.add_subplot(3, 1, 2, projection=ccrs.Robinson(central_longitude=150))
c_slp_2015,lon_2015,lat_2015=cyclic_data(slp_2015,slp.lon,slp.lat)
contour_map(ax2, img_extent,'RdBu_r',c_slp_2015,lon_2015,lat_2015)
ax2.set_title('2015年12月的SLP', fontsize=12)  #设置标签
ax2.set_title(' (b) ', loc='left', fontsize=12)
#ax2.margins(0)
ax3= fig.add_subplot(3, 1, 3, projection=ccrs.Robinson(central_longitude=150))
c_abn,lon_abn,lat_abn=cyclic_data(abn,slp.lon,slp.lat)
contour_map(ax3, img_extent,'seismic',c_abn,lon_abn,lat_abn)
ax3.set_title('2015年12月减去气候态的异常', fontsize=12)  #设置标签
ax3.set_title(' (c) ', loc='left', fontsize=12)
#ax3.margins(0)
plt.savefig(r"D:\data\py_class\work4\1.jpg",dpi=150,bbox_inches = 'tight') # 存图
#plt.gcf().subplots_adjust(left=0.05,top=0.91,bottom=0.09) 
plt.tight_layout()
plt.show()
