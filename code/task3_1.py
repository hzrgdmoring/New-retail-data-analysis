# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

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
        return True
    else:
        return False

def ishot( hot, nhot, num ):
    if num >= hot:
        return '热销'
    elif num <= nhot:
        return '滞销'
    else:
        return '正常'
    
for i in location:
    f = open( direction + filename1 + i + '.csv' )
    df = pd.read_csv( f )
    f.close()
    
    temp = np.array( [ whichkind( j ) for j in df['商品'] ] )
    df2 = df.copy()
    df2 = df2[ temp ]
    stat = df2['商品'].value_counts()
    hot = stat.quantile(0.75)
    nhot = stat.quantile(0.25)
    
    tag = [ ishot( hot, nhot, j ) for j in stat ]
    stat = pd.DataFrame(stat)
    stat['标签'] = tag
    stat.rename( columns={'商品':'销量'}, inplace=True )
    stat.to_csv( direction+'task3-1'+i+'.csv', encoding='GB2312' )
    