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


def contour_map(ax, img_extent):
    ax.set_extent(img_extent, crs=ccrs.PlateCarree())
    ax.set_global()
    ax.add_feature(cfeature.LAND, facecolor='lightgrey')
    ax.add_feature(cfeature.OCEAN, facecolor='white')
    ax.add_feature(cfeature.COASTLINE.with_scale('50m'))
    ax.add_feature(cfeature.LAKES, alpha=0.5)
    ax.add_feature(cfeature.RIVERS)


f = xr.open_dataset(r"D:\data\py_class\data\mslp.mon.mean.nc",
                    drop_variables=["time_bnds"])
f.mslp.attrs['units'] = 'hPa'  #更改单位
f['mslp'] /= 100.

#冬季全球SLP
slp_winter = f.mslp.loc[f.time.dt.month.isin(
    [12, 1, 2])].loc['1989-12-01':'2020-02-01']
#塔希提岛
txtd = np.array(slp_winter.loc[:, -17.5, 212.5]).reshape(31, 3).mean((1))
#冬季全球平均SLP
Y = np.array(slp_winter).reshape(31, 3, 73, 144).mean((1))
#冬季平均的Tahiti岛SLP
X = np.vstack([txtd, np.ones(len(txtd))]).T
#y=kx+b
res_k = []  #存放系数
res_b = []  #存放截距
for i in range(73):
    for j in range(144):
        k, b = np.linalg.lstsq(X, Y[:, i, j], rcond=None)[0]
        res_k.append(k)
        res_b.append(b)

ck, cycle_lon = add_cyclic_point(np.array(res_k).reshape(73, 144),
                                 coord=slp_winter.lon)
LON, LAT = np.meshgrid(cycle_lon, slp_winter.lat)

img_extent = [-180, 180, -90, 90]
fig = plt.figure(figsize=(12, 5))
ax = fig.add_subplot(
    1, 1, 1, projection=ccrs.Robinson(central_longitude=150))  #Robinson())

# 绘制等值线图
c = ax.contour(LON,
               LAT,
               ck,
               levels=16,
               colors='k',
               transform=ccrs.PlateCarree(),
               linewidths=0.7)
ax.clabel(c, inline=10, fontsize=10)
ax.set_title('1990-2020年冬季平均的Tahiti岛SLP（x）与冬季平均全球SLP（y）的回归系数')
contour_map(ax, img_extent)
plt.savefig(r"D:\data\py_class\work6\k.jpg", dpi=300, bbox_inches='tight')
plt.show
