# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

direction = 'D:\\Study\\teddy\\project\\'
filename1 = 'task1-1'
location = [ 'A', 'B', 'C', 'D', 'E' ]

res1 = np.zeros( [ 5, 12 ] ) #每月总交易额
res2 = np.zeros( [ 5, 12 ] ) #交易额月环比增长率

num_counts = 0
for i in location:
    f = open( direction + filename1 + i + '.csv' )
    df = pd.read_csv( f )
    f.close()

    df['支付时间'] = pd.to_datetime( df['支付时间'], errors='coerce' ) #售货机C出现了一个异常的日期数据，将其赋予成无效值来处理
    year_month = np.array( [ [ j.year, j.month ] for j in df['支付时间'] ] )
    temp1 = year_month[:,0] == 2017
    
    for m in range(1,13):
        temp2 = year_month[:,1] == m
        temp = [ temp1[j] and temp2[j] for j in range( temp1.shape[0] ) ]
        df2 = df[ temp ]
        res1[ num_counts, m-1 ] = df2['实际金额'].sum()


    num_counts += 1

# 计算月环比增长率
temp = res1.copy()
temp = np.delete( temp, -1, axis = 1 )
temp = np.c_[ np.zeros( 5 ), temp ]
temp = res1-temp
temp = np.delete( temp, 0, axis = 1 )
res2 = temp / res1[:,:11]

plt.rcParams['font.sans-serif'] = 'SimHei'
plt.rcParams['axes.unicode_minus'] = False

from matplotlib.ticker import MultipleLocator #用于设置刻度标签的倍数（详细程度）

num_counts = 0
for i in location:
    fig = plt.figure( figsize=(16,14) )
    ax1 = fig.add_subplot(111) # 子图总行数、总列数、子图位置
    ax1.bar( list(range(2,13)), res2[ num_counts, : ], 0.4, facecolor = 'lightskyblue', label='交易额月环比增长率' )
    plt.xticks( fontsize = 20 ) # 设置刻度字体大小
    plt.yticks( fontsize = 20 )
    ax1.legend( loc=2, fontsize = 15 )
    ax1.set_ylabel( '交易额月环比增长率', fontsize = 20 )
    ax1.xaxis.set_major_locator( MultipleLocator(1) ) #用于设置刻度标签的倍数（详细程度），这里设置为1的倍数
    if i == 'A':
        ax1.set_ylim([-1, 1.5])
    elif i == 'C':
        ax1.set_ylim([-1, 2.5])
    elif i == 'D':
        ax1.set_ylim([-1, 1.5])
    else:
        ax1.set_ylim([-1, 1.8])
    
    for x, y in zip( list(range(2,13)), res2[ num_counts, : ] ):
        if y > 0:
            plt.text( x, y+0.01, '%.2f' % y, ha='center', va = 'bottom', fontsize = 20, color = 'lightskyblue' ) # '%.2f' 保留两位小数
        else:
            plt.text( x, y-0.06, '%.2f' % y, ha='center', va = 'bottom', fontsize = 20, color = 'lightskyblue' )
        
    ax2 = ax1.twinx()
    ax2.plot( list(range(1,13)), res1[ num_counts, : ], 'o-r', label='每月总交易额'  )
    plt.yticks( fontsize = 20 ) #次y轴的刻度文字大小要再设置一次
    ax2.set_ylabel( '每月总交易额（元）', fontsize = 20 )
    if i == 'A':
        ax2.set_ylim([0, 9000])
    elif i == 'C':
        ax2.set_ylim([0, 12000])
    elif i == 'D':
        ax2.set_ylim([0, 8000])
    elif i == 'E':
        ax2.set_ylim([0, 24000])
    else:
        ax2.set_ylim([0, 10000])
    ax2.legend( loc=1, fontsize = 15 )
    
    for x, y in zip( list(range(1,13)), res1[ num_counts, : ] ):
        plt.text( x-0.33, y+1.2, '%.0f' % y, ha='center', va = 'bottom', fontsize = 16, color = 'r' )
    
    plt.title('售货机'+i+'每月总交易额及交易额月环比增长率', fontsize = 25 )        
    plt.savefig( direction+'task2-2('+i+').png' ) #先保存再show否则会save一片空白
    plt.show()
    
    num_counts += 1
    