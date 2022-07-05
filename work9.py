import xarray as xr
import numpy as np
from scipy.stats import pearsonr
from cartopy.util import add_cyclic_point
import matplotlib
import proplot as pplt
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from scipy.stats.mstats import ttest_ind
#防止中文出错
matplotlib.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
#SLP
f=xr.open_dataset(r"D:\data\py_class\data\mslp.mon.mean.nc",drop_variables = ["time_bnds"])
f.mslp.attrs['units'] = 'hPa'#更改单位
f['mslp']/=100.
#U V 风场
f_u=xr.open_dataset(r"D:\data\py_class\work9\uwnd.mon.mean.nc",drop_variables = ["time_bnds"])
u_winter=f_u.uwnd.loc[f_u.time.dt.month.isin([12,1,2])].loc['1989-12-01':'2020-02-01',850]
f_v=xr.open_dataset(r"D:\data\py_class\work9\vwnd.mon.mean.nc",drop_variables = ["time_bnds"])
v_winter=f_v.vwnd.loc[f_v.time.dt.month.isin([12,1,2])].loc['1989-12-01':'2020-02-01',850]

slp_winter=f.mslp.loc[f.time.dt.month.isin([12,1,2])].loc['1989-12-01':'2020-02-01']
#塔希提岛
txtd=np.array(slp_winter.loc[:,-17.5,212.5]).reshape(31,3).mean((1))
#达尔文岛
dewd=np.array(slp_winter.loc[:,-12.5,130]).reshape(31,3).mean((1))

Winter_SOI=txtd-dewd
Winter_SOI=(Winter_SOI-Winter_SOI.mean(0))/Winter_SOI.std()


#异常年
year=np.arange(1990,2021)
year_max=year[Winter_SOI>1]
year_min=year[Winter_SOI<-1]

def cal_data(data,year_max,year_min):    
    f_year=np.array(data).reshape(-1,3,73,144).mean(1)
    f_year_max=f_year[year_max-1990]
    f_year_min=f_year[year_min-1990]
    f_data=(f_year_max.mean(0)-f_year_min.mean(0))
    _,p = ttest_ind(f_year_max,f_year_min,equal_var=False)
    return f_data,p
slp_data,p_slp=cal_data(slp_winter,year_max,year_min)
u_data,p_u=cal_data(u_winter,year_max,year_min)
v_data,p_v=cal_data(v_winter,year_max,year_min)
def cal_cycle(data,f_data):
    c_data, cycle_lon = add_cyclic_point(data, coord=f_data.lon)
    LON, LAT = np.meshgrid(cycle_lon,f_data.lat)
    return LON, LAT,c_data
slp_lon,slp_lat,slp=cal_cycle(slp_data,slp_winter)
p_lon,p_lat,p=cal_cycle(p_slp,slp_winter)

u_lon,u_lat,u=cal_cycle(u_data,u_winter)
p_u_lon,p_u_lat,pu=cal_cycle(p_u,u_winter)

v_lon,v_lat,v=cal_cycle(v_data,v_winter)
p_v_lon,p_v_lat,pv=cal_cycle(p_v,v_winter)
#SOI
fig = pplt.figure(figsize=(15,15))
ax1 = fig.add_axes([0.22, 0.75, 0.6, 0.21])
c_color = []
for i in range(1990, 2020 + 1):
    if Winter_SOI[i - 1990] > 0:
        c_color.append('red')
    elif Winter_SOI[i - 1990] <= 0:
        c_color.append('blue')
ax1.bar(year,Winter_SOI,color=c_color)
ax1.axhline(1,c='g',linestyle="--")
ax1.axhline(-1,c='g',linestyle="--")
ax1.axhline(0,c='g',linestyle="--")
ax1.set_ylim(-2.1, 3)
plt.xticks(size=15)
plt.yticks(size = 15)
ax1.set_title('SOI',size=20)
ax1.set_title('(a)',loc='left',size=20)

ax2 = fig.subplot(312, proj='robin', proj_kw={'lon_0': 160},title='1990-2020年冬季平均全球SLP异常',title_kw={'size':20})
c1 = ax2.contourf(slp_lon,slp_lat,slp,levels=20,cmap='RdBu_r',transform=ccrs.PlateCarree(),colorbar='b',
                 colorbar_kw={'shrink':0.5,'tickdir':'in'},lw=0.5,extend = 'both')
ax2.contour(slp_lon,slp_lat,slp,levels=20,colors='k',transform=ccrs.PlateCarree(),linewidths=0.5)
ax2.contourf(p_lon,p_lat,p,levels=[0, 0.05, 1],hatches=['..', None],colors="none",transform=ccrs.PlateCarree())
ax2.set_title('(b)',loc='left',size=20)
ax2.format(
    coast=True,coastlinewidth=0.7,
    rivers=True, 
)

ax3 = fig.subplot(313, proj='robin', proj_kw={'lon_0': 160},title='1990-2020年冬季平均全球uv风场850hPa异常',titlesize=20)
Colors =("Silver")
lev=[-1,-0.05,0.05]
ax3.contourf(p_u_lon,p_u_lat,pu,levels=lev,cmap=Colors,zorder=0,transform=ccrs.PlateCarree())
c1=ax3.contourf(p_v_lon,p_v_lat,pv,levels=lev,cmap=Colors,zorder=1,transform=ccrs.PlateCarree())
ax3.quiver(u_lon[::2,::2],u_lat[::2,::2],u[::2,::2],v[::2,::2],c='k',zorder=2,transform=ccrs.PlateCarree(),scale=250)
ax3.format(
    coast=True,coastlinewidth=0.7,
    rivers=True,
)
ax3.set_title('(c)',loc='left',size=20)
fig.savefig(r'D:\data\py_class\work9\01.jpg',
                dpi=300,
                bbox_inches='tight')
