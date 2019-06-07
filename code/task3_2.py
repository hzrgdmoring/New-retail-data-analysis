# -*- coding: utf-8 -*-
from wordcloud import WordCloud
from scipy.misc import imread
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

direction = 'D:\\Study\\teddy\\project\\'
filename1 = 'task3-1'
location = [ 'A', 'B', 'C', 'D', 'E' ]

for i in location:
    f = open( direction + filename1 + i + '.csv' )
    df = pd.read_csv( f )
    f.close()
    
    df.rename( columns={'Unnamed: 0':'商品'}, inplace=True )
    frequencies = [ [j, k ] for j,k in zip( df['商品'], df['销量'] ) ]
    frequencies = dict( frequencies )
    
    my_mask = np.array( imread( direction+'售货机.png' ) )
    my_wordcloud = WordCloud(font_path='C:\\windows\\Fonts\\simhei.ttf',
                             background_color='white',width=600,height=600,
                             scale=2,
                             colormap='plasma',
                             prefer_horizontal = 0.7,
                             mask=my_mask)
    my_wordcloud.generate_from_frequencies( frequencies )
    
    plt.imshow( my_wordcloud, interpolation='bilinear' )
    plt.axis('off')
    plt.show()
    my_wordcloud.to_file( direction+'task3-2('+i+').png' )