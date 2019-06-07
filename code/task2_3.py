# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

direction = 'D:\\Study\\teddy\\project\\'
filename1 = 'task1-1'
location = [ 'A', 'B', 'C', 'D', 'E' ]

attachment = '附件2.csv'
f = open( direction + attachment )
df_at = pd.read_csv( f )
f.close()

# 创建字典用于查询（标签匹配）
pro_dict = [ [j, k ] for j,k in zip( df_at['商品'], df_at['大类'] ) ]
pro_dict = dict( pro_dict )

def whichkind( product_name ):
    if pro_dict[ product_name ] == '饮料':
        return 0.25
    else:
        return 0.2

res = np.zeros( 5 ) #每台售货机的毛利率
num_counts = 0
for i in location:
    f = open( direction + filename1 + i + '.csv' )
    df = pd.read_csv( f )
    f.close()
    
    temp = np.array( [ k*whichkind( j ) for j,k in zip( df['商品'], df['实际金额'] ) ] )
    res[ num_counts ] = temp.sum()

    num_counts += 1
    
plt.figure( figsize=(8,8) )
plt.rcParams.update({'font.size': 22}) #用rc参数来调整字体大小最实际了
colors = [ 'lightskyblue', 'orangered', 'greenyellow', 'yellow', 'plum' ]
explode = [0.01,0.01,0.01,0.01,0.01]
plt.pie( res, labels = location, explode = explode, colors = colors, autopct = '%.2f%%' )
plt.title('各售货机毛利润占总毛利润的比例', fontsize = 20 )
#plt.legend( loc=1, fontsize = 15 )
plt.savefig( direction+'task2-3.png' ) #先保存再show否则会save一片空白
plt.show()
