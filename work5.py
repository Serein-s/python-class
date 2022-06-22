import xarray as xr
import numpy as np
import matplotlib.pyplot as plt

f = xr.open_dataset(r"D:\data\py_class\data\mslp.mon.mean.nc",
                    drop_variables=["time_bnds"])
f.mslp.attrs['units'] = 'hPa'  #更改单位
f['mslp'] /= 100.

slp_spring = f.mslp.loc[f.time.dt.month.isin(
    [3, 4, 5])].loc['1990-03-01':'2020-05-01']
slp_summer = f.mslp.loc[f.time.dt.month.isin(
    [6, 7, 8])].loc['1990-06-01':'2020-08-01']
slp_fall = f.mslp.loc[f.time.dt.month.isin(
    [9, 10, 11])].loc['1990-09-01':'2020-11-01']
slp_winter = f.mslp.loc[f.time.dt.month.isin(
    [12, 1, 2])].loc['1989-12-01':'2020-02-01']

#存放在一个数组内
slp = [slp_spring, slp_summer, slp_fall, slp_winter]

#建立空字典 存放数据
SOI = {}
name = ['Spring_SOI', 'Summer_SOI', 'Fall_SOI', 'Winter_SOI']


#计算SOI的函数
def cal_SOI(data):
    #塔希提岛
    txtd = np.array(data.loc[:, -17.5, 212.5]).reshape(31, 3).mean((1))
    #达尔文岛
    dewd = np.array(data.loc[:, -12.5, 130]).reshape(31, 3).mean((1))
    SOI = txtd - dewd
    return SOI


#PC序列底图
def bar_map(fig_ax, size, data_pc, start_year, end_year):
    c_color = []
    for i in range(start_year, end_year + 1):
        if data_pc[i - start_year] > 0:
            c_color.append('red')
        elif data_pc[i - start_year] <= 0:
            c_color.append('blue')
    fig_ax.set_ylim(np.min(data_pc) - 0.5, np.max(data_pc) + 0.5)
    fig_ax.axhline(0, linestyle="--")
    plt.xticks(size=size)
    plt.yticks(size=size)
    fig_ax.bar(range(start_year, end_year + 1), data_pc, color=c_color)


fig = plt.figure(figsize=(8, 14))
for i in range(4):
    SOI[name[i]] = cal_SOI(slp[i])
    ax = fig.add_subplot(4, 1, i + 1)
    bar_map(ax, 15, SOI[name[i]], 1990, 2020)
    ax.set_title('1990-2020 %s Index' % (name[i]), fontsize=15)
    ax.set_title('(%c)' % (ord('a') + i), loc='left', fontsize=15)

plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=2)
#存图
plt.savefig(r"D:\data\py_class\work5\SOI.jpg", dpi=300, bbox_inches='tight')
plt.show()
