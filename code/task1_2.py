# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

direction = 'D:\\Study\\teddy\\project\\'
filename1 = 'task1-1'
location = [ 'A', 'B', 'C', 'D', 'E' ]

res = np.zeros( [ 5, 2 ] )

num_counts = 0
for i in location:
    f = open( direction + filename1 + i + '.csv' )
    df = pd.read_csv( f )
    f.close()

    df['支付时间'] = pd.to_datetime( df['支付时间'], errors='coerce' ) #售货机C出现了一个异常的日期数据，将其赋予成无效值来处理

    year_month = np.array( [ [ j.year, j.month ] for j in df['支付时间'] ] )

    temp1 = year_month[:,0] == 2017
    temp2 = year_month[:,1] == 5
    temp = [ temp1[j] and temp2[j] for j in range( temp1.shape[0] ) ]

    df2 = df[ temp ]
    res[ num_counts, 0 ] = df2['实际金额'].sum()
    res[ num_counts, 1 ] = df2['实际金额'].count()
    num_counts += 1
    
res = np.r_[ res, res.sum(axis=0).reshape(1,2) ]
tt = pd.DataFrame( res, columns=['交易额(元)','订单量'], index=['A','B','C','D','E','总额'] )
tt.to_csv( direction+'task1-2.csv', encoding='GB2312' )