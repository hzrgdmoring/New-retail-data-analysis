# -*- coding: utf-8 -*-
import calendar
import pandas as pd
import numpy as np

direction = 'D:\\Study\\teddy\\project\\'
filename1 = 'task1-1'
location = [ 'A', 'B', 'C', 'D', 'E' ]

res1 = np.zeros( [ 5, 12 ] ) #每月的每单平均交易额
res2 = np.zeros( [ 5, 12 ] ) #日均订单量

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
        res1[ num_counts, m-1 ] = df2['实际金额'].sum() / df2['实际金额'].count()
        res2[ num_counts, m-1 ] = df2['实际金额'].count() / calendar.monthrange( 2017, m )[1]
        # calendar.monthrange( year, month ) 返回（这个月最后一天是星期几，这个月有多少天）的tuple

    num_counts += 1
    
tt1 = pd.DataFrame( res1, columns=list(range(1,13)), index=['A','B','C','D','E'] )
tt1.to_csv( direction+'task1-3_每月的每单平均交易额.csv', encoding='GB2312' )

tt2 = pd.DataFrame( res2, columns=list(range(1,13)), index=['A','B','C','D','E'] )
tt2.to_csv( direction+'task1-3_日均订单量.csv', encoding='GB2312' )

