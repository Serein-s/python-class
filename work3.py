import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.mpl.ticker as cticker
import matplotlib.pyplot
from cartopy.util import add_cyclic_point
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
#读取nc
f = xr.open_dataset(r"D:\data\py_class\data\mslp.mon.mean.nc",drop_variables = ["time_bnds"])
#提取2015年12月的mslp，单位：hPa
z = f['mslp'].loc[f.time.dt.month.isin([12])].loc['2015-12-01']/100.
#防止中文出错
matplotlib.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
#除去0和360处空白
lon=f.lon
lat=f.lat
cz, cycle_lon = add_cyclic_point(z, coord=lon)
LON, LAT = np.meshgrid(cycle_lon, lat)


def contour_map(fig_ax,img_extent,spec):
    #投影设置
    fig_ax.set_extent(img_extent, crs=ccrs.PlateCarree())
    #填加海岸线
    fig_ax.add_feature(cfeature.COASTLINE.with_scale('50m')) 
    #添加湖泊
    fig_ax.add_feature(cfeature.LAKES, alpha=0.5)
    #添加经纬度设置
    fig_ax.set_xticks(np.arange(leftlon,rightlon+spec,spec), crs=ccrs.PlateCarree())
    fig_ax.set_yticks(np.arange(lowerlat,upperlat+spec,spec), crs=ccrs.PlateCarree())
    lon_formatter = cticker.LongitudeFormatter()
    lat_formatter = cticker.LatitudeFormatter()
    fig_ax.xaxis.set_major_formatter(lon_formatter)
    fig_ax.yaxis.set_major_formatter(lat_formatter)

leftlon, rightlon, lowerlat, upperlat = (-180, 180, -90, 90)
img_extent = [leftlon, rightlon, lowerlat, upperlat]  #经纬度范围

# 生成画布
fig = plt.figure(figsize=(20, 10))
ax1=fig.add_axes([0.05, 0.75, 0.61, 0.405],projection=ccrs.PlateCarree())

# 绘制等值线图
c1 = ax1.contour(LON, LAT, cz, cmap='jet',levels=np.arange(960,1040,10),linewidths=0.9)
contour_map(ax1, img_extent, 30)

ax1.clabel(c1,colors='black') #添加等值线的值
ax1.set_title('2015年12月的海平面气压',fontsize=15) #设置标题
plt.xticks(fontsize=13)#设置刻度大小
plt.yticks(fontsize=13)


ax2 =fig.add_axes([0.65, 0.7, 0.5, 0.5],projection=ccrs.PlateCarree())

# 绘制填色图
c2 = ax2.contourf(LON, LAT,cz,levels=np.arange(960,1040,10), cmap='RdBu_r',extend = 'both')
c21 = ax2.contour(LON, LAT,cz,colors='black',levels=np.arange(960,1040,10),linewidths=0.9)
contour_map(ax2, img_extent, 30)
ax2.set_title('2015年12月的海平面气压',fontsize=15)
plt.xticks(fontsize=13)#设置刻度大小
plt.yticks(fontsize=13)

plt.rcParams['axes.unicode_minus'] = False##负号显示问题
#srink控制colorbar长度，pad控制colorbar和图的距离
cbar=fig.colorbar(c2, shrink=0.8, pad=0.03)
cbar.ax.set_title("hPa",size=15)#色标标签
#存图
plt.savefig(r"D:\data\py_class\work3\1.jpg",dpi=150,bbox_inches='tight')
plt.show()
