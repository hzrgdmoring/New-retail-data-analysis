# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from scipy import  stats
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.graphics.api import qqplot

plt.rcParams['font.sans-serif'] = 'SimHei'
plt.rcParams['axes.unicode_minus'] = False
    
direction = 'D:\\Study\\teddy\\project\\'
filename = '附件1.csv'
f = open( direction + filename )
df = pd.read_csv( f )
f.close()

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

df['支付时间'] = pd.to_datetime( df['支付时间'], errors='coerce' )

temp = np.array( [ whichkind( j ) for j in df['商品'] ] )
df_drinks = df.copy()
df_drinks = df_drinks[ temp ]
df_ndrinks = df.copy()
df_ndrinks = df_ndrinks[ ~temp ]

# 统计饮料类的销售情况
res_drinks = np.zeros( 12 )
year_month = np.array( [ [ j.year, j.month ] for j in df_drinks['支付时间'] ] )
temp1 = year_month[:,0] == 2017

num_counts = 0
for m in range(1,13):
    temp2 = year_month[:,1] == m
    temp = [ temp1[j] and temp2[j] for j in range( temp1.shape[0] ) ]
    df_temp1 = df_drinks.copy()
    df_temp1 = df_temp1[ temp ]
    res_drinks[ num_counts ] = df_temp1['实际金额'].sum()
    num_counts += 1
    
# 统计非饮料类的销售情况
res_ndrinks = np.zeros( 12 )
year_month = np.array( [ [ j.year, j.month ] for j in df_ndrinks['支付时间'] ] )
temp1 = year_month[:,0] == 2017

num_counts = 0
for m in range(1,13):
    temp2 = year_month[:,1] == m
    temp = [ temp1[j] and temp2[j] for j in range( temp1.shape[0] ) ]
    df_temp1 = df_ndrinks.copy()
    df_temp1 = df_temp1[ temp ]
    res_ndrinks[ num_counts ] = df_temp1['实际金额'].sum()
    num_counts += 1
    
#---------------------------------开始预测---------------------------------#

df_forcast_drink = pd.DataFrame( res_drinks, columns = ['实际销量'], index = pd.date_range( '2017-01', periods = 12, freq = 'M' ) ) #index不能直接赋1，2，3，...

#  一阶差分图
fig = plt.figure( figsize=(12,8) )
ax = fig.add_subplot(111)
diff1 = df_forcast_drink.diff(1)
diff1.plot( ax = ax )
plt.savefig( direction+'task4-drinks_diff1.png' )

# 绘制acf和pacf图
diff1= df_forcast_drink.diff(1)
fig = plt.figure(figsize=(12,8))
ax1=fig.add_subplot(211)
fig = sm.graphics.tsa.plot_acf( df_forcast_drink, lags=10, ax=ax1 )
ax2 = fig.add_subplot(212)
fig = sm.graphics.tsa.plot_pacf( df_forcast_drink, lags=10, ax=ax2 )
plt.savefig( direction+'task4-drinks_acf_pacf.png' )

# 通过信息准则最终确定所选模型
arma_mod10 = sm.tsa.ARMA( df_forcast_drink, (1,0) ).fit()
print( arma_mod10.aic, arma_mod10.bic, arma_mod10.hqic )
arma_mod01 = sm.tsa.ARMA( df_forcast_drink, (0,1) ).fit()
print( arma_mod01.aic, arma_mod01.bic, arma_mod01.hqic )
arma_mod11 = sm.tsa.ARMA( df_forcast_drink, (1,1) ).fit()
print( arma_mod11.aic, arma_mod11.bic, arma_mod11.hqic )

predict_dta = arma_mod10.predict( '2018-01', '2018-02', dynamic = True )
print( predict_dta )
fig, ax = plt.subplots( figsize=(16, 14) )
ax = df_forcast_drink.loc[ '2017-01': ].plot( ax = ax )

show_pre = pd.DataFrame( predict_dta['2018-01'], columns = ['实际销量'] )
show_pre = show_pre.append(df_forcast_drink.loc['2017-12'])
show_pre.columns = ['销量预测']
show_pre.plot (ax = ax )

plt.legend(fontsize = 20  )
plt.yticks( fontsize = 20 )
plt.xticks( fontsize = 20 )
plt.ylabel( '销售额', fontsize = 23 )
plt.xlabel( '月份', fontsize = 23 )
plt.title('2018年1月饮料类商品销售额预测', fontsize = 25 )

num_show = res_drinks.copy()
num_show = np.append( num_show, predict_dta['2018-01'] )
num_show = pd.DataFrame( num_show, columns = ['销量'], index = pd.date_range( '2017-01', periods = 13, freq = 'M' ) )
for x, y in zip( num_show.index, num_show['销量'] ):
    plt.text( x, y-100, '%.2f' % y, ha='center', va = 'bottom', fontsize = 20, color = 'black' )

plt.savefig( direction+'task4-drinks_predict.png' )

plt.show()

#---------------------------非饮料类商品销售额预测---------------------------#

df_forcast_ndrink = pd.DataFrame( res_ndrinks, columns = ['实际销量'], index = pd.date_range( '2017-01', periods = 12, freq = 'M' ) ) #index不能直接赋1，2，3，...

#  一阶差分图
fig = plt.figure( figsize=(12,8) )
ax = fig.add_subplot(111)
diff1 = df_forcast_ndrink.diff(1)
diff1.plot( ax = ax )
plt.savefig( direction+'task4-ndrinks_diff1.png' )

# 绘制acf和pacf图
diff1= df_forcast_ndrink.diff(1)
fig = plt.figure(figsize=(12,8))
ax1=fig.add_subplot(211)
fig = sm.graphics.tsa.plot_acf( df_forcast_ndrink, lags=10, ax=ax1 )
ax2 = fig.add_subplot(212)
fig = sm.graphics.tsa.plot_pacf( df_forcast_ndrink, lags=10, ax=ax2 )
plt.savefig( direction+'task4-ndrinks_acf_pacf.png' )

# 通过信息准则最终确定所选模型
arma_mod10 = sm.tsa.ARMA( df_forcast_ndrink, (1,0) ).fit()
print( arma_mod10.aic, arma_mod10.bic, arma_mod10.hqic )
arma_mod01 = sm.tsa.ARMA( df_forcast_ndrink, (0,1) ).fit()
print( arma_mod01.aic, arma_mod01.bic, arma_mod01.hqic )
#arma_mod11 = sm.tsa.ARMA( df_forcast_ndrink, (1,1) ).fit()
#print( arma_mod11.aic, arma_mod11.bic, arma_mod11.hqic )

predict_dta = arma_mod01.predict( '2018-01', '2018-02', dynamic = True )
print( predict_dta )
fig, ax = plt.subplots( figsize=(16, 14) )
ax = df_forcast_ndrink.loc[ '2017-01': ].plot( ax = ax )

show_pre = pd.DataFrame( predict_dta['2018-01'], columns = ['实际销量'] )
show_pre = show_pre.append(df_forcast_ndrink.loc['2017-12'])
show_pre.columns = ['销量预测']
show_pre.plot (ax = ax )

plt.legend(fontsize = 20  )
plt.yticks( fontsize = 20 )
plt.xticks( fontsize = 20 )
plt.ylabel( '销售额', fontsize = 23 )
plt.xlabel( '月份', fontsize = 23 )
plt.title('2018年1月饮料类商品销售额预测', fontsize = 25 )

num_show = res_ndrinks.copy()
num_show = np.append( num_show, predict_dta['2018-01'] )
num_show = pd.DataFrame( num_show, columns = ['销量'], index = pd.date_range( '2017-01', periods = 13, freq = 'M' ) )
for x, y in zip( num_show.index, num_show['销量'] ):
    plt.text( x, y-100, '%.2f' % y, ha='center', va = 'bottom', fontsize = 20, color = 'black' )

plt.savefig( direction+'task4-ndrinks_predict.png' )

plt.show()