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

#read all the data points
filename = "point_data.csv"
df_0= pd.read_csv(filename,delimiter = ',')
df_0['NTL'].fillna(0, inplace=True)
#remove and reclassify poopulation and NTL 
df_0 = df_0[(df_0['POP'] > 0)]
df_0.loc[df_0.NTL < 0, 'NTL'] = 0


#join with income classification
filename2 = "income_classification.csv"
df_inc= pd.read_csv(filename2,delimiter = ',')
df2 = pd.merge(df_0, df_inc,on='GID_0',how = 'left')
df2['Income'] = df2.Income.fillna('None')
print(len(df2.GID_0.unique()))

#select urban population that does not have NTL value
df_urban_other = df2[(df2['POP'] > 0) & (df2['SMOD'] > 20)&(df2['NTL'] == 0)]

#select rural population
df_rural = df2[(df2['POP'] > 0) & (df2['SMOD'] <20)]

#selecrt urban population with NTL >0
df2 = df2[(df2['POP'] > 0) & (df2['SMOD'] > 20) &(df2['NTL'] > 0)]

#set a threshold for selecting data for iForest test based on medium NTL value
thld = np.percentile(df2.NTL, 50)

#data for anomaly detection
df2_p1 =  df2[(df2['NTL'] > thld)]

#data considered as normal
df2_p2 =  df2[(df2['NTL'] <= thld)]
df2 = df2_p1


#filter data
#save a copy
popAndNtl= df2
#rename the columns
popAndNtl_v2 = df2[["POP", "NTL"]]

#import iforest
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler


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


import statistics
print(len(dfall.loc[dfall.Outlier == -1]))
de_outlier = dfall.loc[dfall.Outlier == -1]

#save all the outliers
de_outlier.to_csv('outlier.csv',index = False)

#reclassify outliers to 0
ntl_mean = int(statistics.mean(dfall.NTL.tolist()))
dfall.loc[dfall.Outlier == -1, 'NTL'] = 0

#drop ourlier column
dfall.drop('Outlier', axis=1, inplace=True)

#save final data to file
df_urban_final= dfall[(dfall['SMOD'] > 20)]

#save all the urban points
df_urban_final.to_csv('urban_points.csv',index = False)

#save all points
dfall.to_csv('all_points.csv',index = False)
