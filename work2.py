import matplotlib.pyplot as plt
import xarray as xr
import numpy as np
import matplotlib
#防止中文出错
matplotlib.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

f = xr.open_dataset(r"D:\data\py_class\data\mslp.mon.mean.nc",drop_variables = ["time_bnds"])
f.attrs['units'] = 'hPa'#更改单位
#塔希提岛
txtd=f.mslp.loc[:,-17.5,212.5]/100.0
#达尔文岛
dewd=f.mslp.loc[:,-12.5,130]/100.0
#计算南方涛动指数
SOI=txtd-dewd
fig = plt.figure(figsize=(12,8))#准备画板并设置画板大小
ax1=fig.add_subplot(211)#指向#2行1列第1行
ax1.plot(txtd.time, txtd ,marker=".",c='r')

ax1.set_ylabel('hPa',fontsize=20)
ax1.set_title('塔希提岛海平面气压',fontsize=15)
ax2=fig.add_subplot(212)#指向#2行2列第2行
ax2.plot(dewd.time, dewd, marker=".",c='g')
ax2.set_xlabel('time',fontsize=20)
ax2.set_ylabel('hPa',fontsize=20)
ax2.set_title('达尔文岛海平面气压',fontsize=15)
plt.savefig(r'D:\data\py_class\work2\1.jpg')

fig1 = plt.figure(figsize=(12,5))#准备画板并设置画板大小
ax=fig1.add_subplot(111)#指向#1行1列第1行
ax.hist(SOI)
ax.set_xlabel('气压差(单位：hPa)',fontsize=15)
ax.set_ylabel('频率',fontsize=15)
ax.set_title('南方涛动指数',fontsize=15)
plt.savefig(r'D:\data\py_class\work2\2.jpg')
plt.show()
