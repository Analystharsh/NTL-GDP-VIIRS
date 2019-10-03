#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 09:10:30 2019

@author: xuantongwang
"""

import pandas as pd
import scipy as sp
import numpy as np
from scipy.stats import chi2
import seaborn as sns


filename = "/Volumes/Extreme 500/GINI/Python/v4/data0922.csv"
df_0= pd.read_csv(filename,delimiter = ',')
df_0['NTL'].fillna(0, inplace=True)
df_0 = df_0[(df_0['POP'] > 0)]
df_0.loc[df_0.NTL < 0, 'NTL'] = 0


#join with continent and income data
filename2 = "/Volumes/Extreme 500/GINI/Python/data/income_code.csv"
df_inc= pd.read_csv(filename2,delimiter = ',')

filename3 = "/Volumes/Extreme 500/GINI/Python/data/continentcode.csv"
df_cont= pd.read_csv(filename3,delimiter = ',')

filename = "/Volumes/Extreme 500/GINI/Python/data/gadm2_info.csv"
df_name1= pd.read_csv(filename, delimiter = ',',usecols=['GID_0','GID_2'])
filename = "/Volumes/Extreme 500/GINI/Python/data/gadm2newid.csv"
df_name2= pd.read_csv(filename, delimiter = ',',usecols=['GID_2','New_ID2'])
df_name2.columns = ['GID_2','gadm2_1']

df_name_new = pd.merge(df_name1, df_name2,on='GID_2')

#merge newid with continent and income
df2 = pd.merge(df_0, df_inc,on='GID_0')
df_urban_other = df2[(df2['POP'] > 0) & (df2['SMOD'] > 20)&(df2['NTL'] == 0)]
df_rural = df2[(df2['POP'] > 0) & (df2['SMOD'] <20)]
df2 = df2[(df2['POP'] > 0) & (df2['SMOD'] > 20) &(df2['NTL'] > 0)]
secondqt = np.percentile(df2.NTL, 50)
df2_p1 =  df2[(df2['NTL'] > secondqt)]
df2_p2 =  df2[(df2['NTL'] <= secondqt)]
df2 = df2_p1
#4 sets of data: df_p2, df2, df_urban_other, df_rural


#filter data
popAndNtl= df2

popAndNtl_v2 = df2[["POP", "NTL"]]
#popAndNtl.plot.scatter(x = "POP", y = "NTL")
#test1 = popAndNtl[popAndNtl['NTL']<1]


from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

#clf = IsolationForest(max_samples=10000, contamination=.01)
#clf.fit(popAndNtl)
#outliers_predicted = clf.predict(popAndNtl)
##check the results
#df2['outlier'] = outliers_predicted
#plt.figure(figsize = (10,5))
#plt.scatter(df2['POP'], df2['NTL'], c=df2['outlier'])
#plt.show()




list_inc = popAndNtl.Income.unique().tolist()
list_country = popAndNtl.GID_0.unique().tolist()
cols_0 = list(popAndNtl)
cols=cols_0.append("Outlier")
dfall = pd.DataFrame(columns=cols)

for inc_i in list_inc: 
    popAndNtl_temp = popAndNtl[(popAndNtl['Income']==inc_i)]
    if len(popAndNtl_temp)>0:
        df_rest = pd.DataFrame(columns=cols_0)
        #append 4 sets of data: df_p2, df2, df_urban_other, df_rural

        new_df = popAndNtl_temp[["POP", "NTL"]]
        print(len(new_df),inc_i)
        #normalize data
        scaler = MinMaxScaler()
        new_df = scaler.fit_transform(new_df)
        new_df = pd.DataFrame(new_df, columns = ["POP", "NTL"])
        #new_df.plot.scatter(x = "POP", y = "NTL")
        ##test2 = popAndNtl.sort_values('NTL')
        #detect outliers
        clf = IsolationForest(max_samples=5000, contamination=.001)
        clf.fit(new_df)
        outliers_predicted = clf.predict(new_df)
        #append cluster outlier
        popAndNtl_temp['Outlier'] = outliers_predicted
        #append to dataframe
        
        #all all data
        df_p2_v2 = df2_p2[(df2_p2['Income']==inc_i)]
        df_rest = df_rest.append(df_p2_v2) 
        df_urban_other_v2 = df_urban_other[(df_urban_other['Income']==inc_i)]
        df_rest = df_rest.append(df_urban_other_v2) 
        df_rural_v2 = df_rural[(df_rural['Income']==inc_i)]
        df_rest = df_rest.append(df_rural_v2) 
        df_rest['Outlier'] = 1
        df_rest = df_rest.append(popAndNtl_temp) 
       
        dfall = dfall.append(df_rest) 

        #plot
        plt.figure(figsize = (30,15))
        plt.scatter(df_rest['POP'], df_rest['NTL'], c=df_rest['Outlier'])
        #plt.show()
        title = str(inc_i)+'.png'
        plt.savefig(title)

plt.figure(figsize = (10,5))
plt.scatter(dfall['POP'], dfall['NTL'], c=dfall['Outlier'])
plt.savefig('final.png')
#plt.show()



import statistics
print(len(dfall.loc[dfall.Outlier == -1]))
de_outlier = dfall.loc[dfall.Outlier == -1]
dfall.to_csv('outlier.csv',index = False)


ntl_mean = int(statistics.mean(dfall.NTL.tolist()))
dfall.loc[dfall.Outlier == -1, 'NTL'] = 0
dfall.drop('Outlier', axis=1, inplace=True)

df_urban_final= dfall[(dfall['SMOD'] > 20)]
df_urban_final.to_csv('if_urban_filtered.csv',index = False)

dfall.to_csv('all_data.csv',index = False)

#popAndNtl['outlier'] = clusters
#outlier_count = np.count_nonzero(clusters == -1)