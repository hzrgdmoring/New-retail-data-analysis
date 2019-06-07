# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

direction = 'D:\\Study\\teddy\\project\\'
filename = '附件1.csv'
f = open( direction + filename )
df = pd.read_csv( f )
f.close()

attachment = '附件2.csv'
f = open( direction + attachment )
df_at = pd.read_csv( f )
f.close()

typeset = list( df_at['二级类'].value_counts().index.values )
#typeset = pd.DataFrame(df_at['二级类'].value_counts().index.values)
res = np.zeros( [len(typeset), 12] )

# 创建字典用于查询（标签匹配）
pro_dict = [ [j, k ] for j,k in zip( df_at['商品'], df_at['二级类'] ) ]
pro_dict = dict( pro_dict )
def whichkind_2( product_name ):
    return pro_dict[ product_name ] 

df['支付时间'] = pd.to_datetime( df['支付时间'], errors='coerce' ) #售货机C出现了一个异常的日期数据，将其赋予成无效值来处理
year_month = np.array( [ [ j.year, j.month ] for j in df['支付时间'] ] )
temp1 = year_month[:,0] == 2017

for m in range(1,13):
    temp2 = year_month[:,1] == m
    temp = [ temp1[j] and temp2[j] for j in range( temp1.shape[0] ) ]
    df2 = df.copy() # 需要注意的一步，若不写这个且下一行直接写成 df2 = df[ temp ] 就会在后续对df2进行操作是出现对视图赋值的警告
    df2 = df2[ temp ]
    df2.reindex( range( len(df2) ) )
    
    temp3 = [ whichkind_2( j ) for j in df2['商品'] ]
#    temp3 = pd.DataFrame( temp3 )
    '''
    不能将temp3转换成dataframe之后再并到df2中，因为temp3的index会重新从0开始计数而
    在第二次循环（m=2）时，df2的index时直接从二月（1693行）开始的，在合并的时候就会
    出现index对不上号而全部以nan填充
    '''
    df2['二级类'] = temp3 # 此处对应上述需要注意的一步
    
    num_counts = 0
    for j in typeset:
        '''
        同理，如果先将temp3转成dataframe再通过df2[ temp3['二级类'] == j ]进行索
        引的话，也会由同样index对不上号的原因在第二次循环时报错
        '''
        if df2[ df2['二级类'] == j ]['实际金额'].count() == 0: # 避免出现分母为0的情况
            res[ num_counts, m-1 ] = 0
        else:
            res[ num_counts, m-1 ] = df2[ df2['二级类'] == j ]['实际金额'].sum() / df2[ df2['二级类'] == j ]['实际金额'].count()
        num_counts += 1

from matplotlib.ticker import MultipleLocator #用于设置刻度标签的倍数（详细程度）

plt.rcParams['font.sans-serif'] = 'SimHei'
plt.rcParams['axes.unicode_minus'] = False

fig = plt.figure( figsize=(20,30) )
ax1 = fig.add_subplot(111)

s = res.reshape( 240 )
x = np.array( range(1,13) )
for i in range(19):
    x = np.r_[ x, np.array( range(1,13) ) ]
y = np.array( typeset )
for i in range(11):
    y = np.c_[ y, np.array( typeset ) ]
y = y.reshape( 240 )

ax1.scatter( x, y, s*300, alpha = 0.5 ) # alpha是亮度
plt.xticks( fontsize = 20 )
plt.yticks( fontsize = 20 )
ax1.set_xlabel( '月份', fontsize = 25 )
ax1.set_ylabel( '商品二级类名', fontsize = 25 )
plt.title( '每月交易额均值', fontsize = 30 )
ax1.xaxis.set_major_locator( MultipleLocator(1) ) #用于设置刻度标签的倍数（详细程度），这里设置为1的倍数
plt.savefig( direction+'task2-4.png' ) #先保存再show否则会save一片空白
plt.show()
    