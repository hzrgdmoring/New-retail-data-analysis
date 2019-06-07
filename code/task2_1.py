# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

direction = 'D:\\Study\\teddy\\project\\'
filename = '附件1.csv'

f = open( direction + filename )
df = pd.read_csv( f )
f.close()

'''
去掉一些用不上的列
'''
df.pop('订单号')
df.pop('设备ID')
df.pop('状态')
df.pop('提现')

df['支付时间'] = pd.to_datetime( df['支付时间'], errors='coerce' ) #售货机C出现了一个异常的日期数据，将其赋予成无效值来处理

year_month = np.array( [ [ j.year, j.month ] for j in df['支付时间'] ] )

temp1 = year_month[:,0] == 2017
temp2 = year_month[:,1] == 6
temp = [ temp1[j] and temp2[j] for j in range( temp1.shape[0] ) ]

df2 = df[ temp ]
product_sales = df2['商品'].value_counts()

plt.rcParams['font.sans-serif'] = 'SimHei'
plt.rcParams['axes.unicode_minus'] = False
plt.figure( figsize=(16,14) )
plt.bar( product_sales.index.values[0:5], product_sales.iloc[0:5], 0.4, facecolor = 'lightskyblue' )
for x, y in zip( product_sales.index.values[0:5], product_sales.iloc[0:5] ):  
    plt.text( x, y+0.08, '%.0f' % y, ha ='center', va = 'bottom',fontsize = 20 ) # 添加数值
plt.xticks( fontsize = 20 ) # 设置刻度字体大小
plt.yticks( fontsize = 20 )
plt.ylabel( '销量', fontsize = 20 )
plt.title('2017年6月销量前5的商品销量', fontsize = 20 )
plt.savefig( direction+'task2-1.png' ) #先保存再show否则会save一片空白
plt.show()
