# -*- coding: utf-8 -*-
import pandas as pd

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

location = [ 'A', 'B', 'C', 'D', 'E' ]

for i in location:
    temp = df[ df['地点'] == i ]
    temp.to_csv( direction+'task1-1'+i+'.csv', encoding='GB2312', index = None )