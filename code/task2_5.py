# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

direction = 'D:\\Study\\teddy\\project\\'
filename = 'task1-1C.csv'

f = open( direction + filename )
df = pd.read_csv( f )
f.close()

df['支付时间'] = pd.to_datetime( df['支付时间'], errors='coerce' ) #售货机C出现了一个异常的日期数据，将其赋予成无效值来处理

year_month = np.array( [ [ j.year, j.month ] for j in df['支付时间'] ] )
temp1 = year_month[:,0] == 2017

for m in range(6,9):
    temp2 = year_month[:,1] == m
    temp = [ temp1[j] and temp2[j] for j in range( temp1.shape[0] ) ]
    df2 = df.copy() # 需要注意的一步，若不写这个且下一行直接写成 df2 = df[ temp ] 就会在后续对df2进行操作是出现对视图赋值的警告
    df2 = df2[ temp ]
    
    if m == 6:
        last_day = 30
    else:
        last_day = 31
    
    day = [ j.day for j in df2['支付时间'] ]
    hour = [ j.hour for j in df2['支付时间'] ]
    df2['day'] = day # 此处对应上述需要注意的一步
    df2['hour'] = hour # 此处对应上述需要注意的一步
    
    res = np.zeros( [24,last_day] )   
    for d in range(1,last_day+1):
        df3 = df2[ df2['day'] == d ]
        temp3 = df3['hour'].value_counts()
        for h in range(24):
            if not( h in temp3.index ):
                res[ h, d-1 ] = 0
            else:
                res[ h, d-1 ] = temp3[h]
    

    plt.figure( figsize=(16,14) )
    sns.set( font_scale = 2 ) #调整colobar的字体大小
    sns.heatmap( res, vmax = 20, vmin = 0, cmap = 'hot' )
    plt.rcParams['font.sans-serif'] = 'SimHei'
    plt.rcParams['axes.unicode_minus'] = False
    plt.xlabel( '日期', fontsize = 25 )
    plt.ylabel( '小时', fontsize = 25 )
    plt.xticks( fontsize = 15 ) # 设置刻度字体大小
    plt.yticks( fontsize = 15 )
    plt.title( '售货机C的'+str(m)+'月订单量热力图', fontsize = 30 )
    plt.savefig( direction+'task2-5('+str(m)+').png' )
    plt.show()
    
