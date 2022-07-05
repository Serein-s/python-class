import xarray as xr
import numpy as np
from scipy.stats import pearsonr
from cartopy.util import add_cyclic_point
import matplotlib
import proplot as pplt
#防止中文出错
matplotlib.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

f = xr.open_dataset(r"D:\data\py_class\data\mslp.mon.mean.nc",
                    drop_variables=["time_bnds"])
f.mslp.attrs['units'] = 'hPa'  #更改单位
f['mslp'] /= 100.

#冬季全球SLP
slp_winter = f.mslp.loc[f.time.dt.month.isin([12, 1, 2])].loc['1989-12-01':'2020-02-01']
#塔希提岛
txtd = np.array(slp_winter.loc[:, -17.5, 212.5]).reshape(31, 3).mean((1))
#冬季全球平均SLP
Y=np.array(slp_winter).reshape(31,3,73,144).mean((1))
#冬季平均的Tahiti岛SLP
X=txtd
#计算
res_k=[]#存放系数
res_p=[]#存放p值
for i in range(73):
    for j in range(144):
        k,p=pearsonr(X,Y[:,i,j])
        res_k.append(k)
        res_p.append(p)
        
ck, cycle_lon = add_cyclic_point(np.array(res_k).reshape(73,144), coord=slp_winter.lon)
LON, LAT = np.meshgrid(cycle_lon,slp_winter.lat)


fig = pplt.figure(figsize=(12, 5))
ax = fig.subplots(nrows=1, proj='robin', proj_kw={'lon_0': 150})
c1 = ax.contourf(LON, LAT,ck,levels=15,cmap='RdBu_r',transform=ccrs.PlateCarree(),colorbar='b',
                 colorbar_kw={'shrink':0.5,'tickdir':'in'},lw=0.5,extend = 'both')
ax.contour(LON, LAT,ck,levels=15,colors='k',transform=ccrs.PlateCarree(),linewidths=0.5)
ax.contourf(slp_winter.lon,slp_winter.lat,np.array(res_p).reshape(73,144),levels=[0, 0.05, 1],
            hatches=['.', None],colors="none",transform=ccrs.PlateCarree())
ax.format(
    suptitle='1990-2020年冬季平均的Tahiti岛SLP（x）与冬季平均全球SLP（y）的相关系数',
    suptitle_kw={'size':12},
    coast=True,coastlinewidth=0.7,
    rivers=True,
    
)
fig.savefig(r'D:\data\py_class\work8\ccs.jpg',dpi=300,bbox_inches='tight')
pplt.show()
