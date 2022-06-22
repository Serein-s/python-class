from pandas.core.frame import DataFrame
import pandas as pd
import numpy as np
Temp1 = pd.read_csv(r"D:\data\py_class\work1\Temp.txt", sep="\s+")
Prec1 = pd.read_csv(r"D:\data\py_class\work1\Prec.csv")
Temp = Temp1.drop_duplicates()
Prec = Prec1.drop_duplicates()
S = pd.merge(Temp, Prec)
ID1 = S.Station_Id_C
ID = list(ID1.drop_duplicates())
Day1 = S.Day
Day = list(Day1.drop_duplicates())
#建立空列表
Tmax = []  #日最高气温
Tmin = []  #日最低气温
Psum = []  #日平均气温
Tmean = []  #日降水量

# for循环 步长间隔24
for i in range(0, 600, 24):
    #使用mean、sum、min、max函数求算术平均值、和、最小值、最大值
    a = (np.mean(S.TEM_Max[i:i + 24]))
    b = (np.sum(S.PRE_1h[i:i + 24]))
    c = (np.min(S.TEM_Min[i:i + 24]))
    d = (np.max(S.TEM_Max[i:i + 24]))

    #使用list.append()在列表末尾添加新的对象
    Tmax.append(d)
    Tmin.append(c)
    Psum.append(b)
    Tmean.append(a)
 
data = {'Tmax': Tmax,
        'Tmin': Tmin,
        'Tmean': Tmean,
        'Psum': Psum}
## 行标签
mindex = pd.MultiIndex.from_product([ID, Day], names=['Station_Id_C', 'Day'])
df = DataFrame(data, index=mindex)
df.to_excel(r"D:\data\py_class\work1\data.xlsx")
