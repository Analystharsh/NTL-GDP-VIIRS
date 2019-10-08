#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  6 03:47:34 2019

@author: tonywang
"""

import pandas as pd
import numpy as np

#read all the urban data points
filename = "/urban_points.csv"
df_urban_all = pd.read_csv(filename, delimiter = ',')

#read all data
filename = "all_points.csv"
df_all = pd.read_csv(filename, delimiter = ',')

#find the total national population
df_allpop = df_all.groupby(['GID_0'])['POP'].sum().reset_index().sort_values('POP', ascending = False)
df_allpop.columns = ['GID_0','TotalPOP']

#read all unique country names
df_all_names = df_allpop.GID_0.unique().tolist()

#create empty dataframe to store distrct-level data
cols1 = ['GID_0','SumNTL']
dfurban_ntlsum = pd.DataFrame(columns=cols1)
cols2 = ['GID_0','SumUrPop']
dfurban_popsum = pd.DataFrame(columns=cols2)
cols3 = ['GID_dis','DisNTL']
dfurban_ntldis = pd.DataFrame(columns=cols3)
cols4 = ['GID_dis','DisUrPop']
dfurban_popdis = pd.DataFrame(columns=cols4)

#process level 2 countries first
#group by level 2 first
df_dis2 = df_all.groupby(['GID_0','GID_2'])['POP'].sum().reset_index().sort_values('POP', ascending = False)
df_dis2.columns = ['GID_0','GID_dis','DisPOP']
df_dis2_names = df_dis2.GID_0.unique().tolist()

##summarize level 2 urban pop and ntl data
df_urban = df_urban_all[df_urban_all['GID_0'].isin(df_dis2_names)]
dfurban_ntlsum_l2 = df_urban.groupby(['GID_0'])['NTL'].sum().reset_index().sort_values('NTL', ascending = False)
dfurban_ntlsum_l2.columns = ['GID_0','SumNTL']

dfurban_popsum_l2 = df_urban.groupby(['GID_0'])['POP'].sum().reset_index().sort_values('POP', ascending = False)
dfurban_popsum_l2.columns = ['GID_0','SumUrPop']

dfurban_ntldis_l2 = df_urban.groupby(['GID_2'])['NTL'].sum().reset_index().sort_values('NTL', ascending = False)
dfurban_ntldis_l2.columns = ['GID_dis','DisNTL']

dfurban_popdis_l2 = df_urban.groupby(['GID_2'])['POP'].sum().reset_index().sort_values('POP', ascending = False)
dfurban_popdis_l2.columns = ['GID_dis','DisUrPop']

#append new values
dfurban_ntlsum = dfurban_ntlsum.append(dfurban_ntlsum_l2) 
dfurban_popsum = dfurban_popsum.append(dfurban_popsum_l2) 
dfurban_ntldis = dfurban_ntldis.append(dfurban_ntldis_l2) 
dfurban_popdis = dfurban_popdis.append(dfurban_popdis_l2) 


#check for countries with missing level 2
miss_list_dis = np.setdiff1d(df_all_names,df_dis2_names)

#group by level 1
df_dis1 = df_all[df_all['GID_0'].isin(miss_list_dis)]
df_dis_p2 = df_dis1.groupby(['GID_0','GID_1'])['POP'].sum().reset_index().sort_values('POP', ascending = False)
df_dis_p2.columns = ['GID_0','GID_dis','DisPOP']
df_dis1_names = df_dis_p2.GID_0.unique().tolist()

##summarize level 1 urban pop and ntl data
df_urban = df_urban_all[df_urban_all['GID_0'].isin(df_dis1_names)]
dfurban_ntlsum_l1 = df_urban.groupby(['GID_0'])['NTL'].sum().reset_index().sort_values('NTL', ascending = False)
dfurban_ntlsum_l1.columns = ['GID_0','SumNTL']

dfurban_popsum_l1 = df_urban.groupby(['GID_0'])['POP'].sum().reset_index().sort_values('POP', ascending = False)
dfurban_popsum_l1.columns = ['GID_0','SumUrPop']

dfurban_ntldis_l1 = df_urban.groupby(['GID_1'])['NTL'].sum().reset_index().sort_values('NTL', ascending = False)
dfurban_ntldis_l1.columns = ['GID_dis','DisNTL']

dfurban_popdis_l1 = df_urban.groupby(['GID_1'])['POP'].sum().reset_index().sort_values('POP', ascending = False)
dfurban_popdis_l1.columns = ['GID_dis','DisUrPop']

#append new values
dfurban_ntlsum = dfurban_ntlsum.append(dfurban_ntlsum_l1) 
dfurban_popsum = dfurban_popsum.append(dfurban_popsum_l1) 
dfurban_ntldis = dfurban_ntldis.append(dfurban_ntldis_l1) 
dfurban_popdis = dfurban_popdis.append(dfurban_popdis_l1) 

#group by level 0
miss_list_dis2 = np.setdiff1d(miss_list_dis,df_dis1_names)
#select level 0
df_dis0 = df_all[df_all['GID_0'].isin(miss_list_dis2)]

#group by level 0
df_dis_p3 = df_dis0.groupby(['GID_0'])['POP'].sum().reset_index().sort_values('POP', ascending = False)
df_dis_p3.columns = ['GID_0','DisPOP']

df_dis_p3['GID_dis']=df_dis_p3['GID_0']
df_dis_p3 = df_dis_p3[['GID_0','GID_dis','DisPOP']]

df_urban = df_urban_all[df_urban_all['GID_0'].isin(df_dis1_names)]
dfurban_ntlsum_l0 = df_urban.groupby(['GID_0'])['NTL'].sum().reset_index().sort_values('NTL', ascending = False)
dfurban_ntlsum_l0.columns = ['GID_0','SumNTL']



dfurban_popsum_l0 = df_urban.groupby(['GID_0'])['POP'].sum().reset_index().sort_values('POP', ascending = False)
dfurban_popsum_l0.columns = ['GID_0','SumUrPop']


#append new values
dfurban_ntlsum = dfurban_ntlsum.append(dfurban_ntlsum_l0) 
dfurban_popsum = dfurban_popsum.append(dfurban_popsum_l0) 

#becasue they only have level 0
dfurban_ntldis_l0 = dfurban_ntlsum_l0
dfurban_ntldis_l0.columns = ['GID_dis','DisNTL']
dfurban_popdis_l0= dfurban_popsum_l0
dfurban_popdis_l0.columns = ['GID_dis','DisUrPop']
dfurban_ntldis = dfurban_ntldis.append(dfurban_ntldis_l0) 
dfurban_popdis = dfurban_popdis.append(dfurban_popdis_l0) 


df_dis0_names = df_dis_p3.GID_0.unique().tolist()

cols = ['GID_0','GID_dis','DisPOP']
df_dis = pd.DataFrame(columns=cols)
df_dis = df_dis.append(df_dis2) 
df_dis = df_dis.append(df_dis_p2)
df_dis = df_dis.append(df_dis_p3)


#read all the agriculatural production ratios
filename_agr = "agr.csv"
dfagr = pd.read_csv(filename_agr, delimiter = ',', usecols = ['NAME','AGR'])
dfagr.columns = ['GID_0','AGR']
dfagr = dfagr[dfagr['AGR'].notnull()]
namelist = dfagr.GID_0.unique().tolist()
#produce a new table
df_dis = df_dis[df_dis.GID_0.isin(namelist)]
gid0list = df_dis.GID_0.tolist()
GID_dis_list = df_dis.GID_dis.tolist()
cols = ['GID_0', 'PerGDP', 'PerPop','PerUrGDPPC','PerRuGDPPC','GID_dis']
result  = pd.DataFrame(columns = cols)

#calculate GDP per capita for each sub-national district
i = 0
while i < len(gid0list):#len(gid0list)
    #print(i)
    #find out country name
    country_name = gid0list[i]
    dis_name = GID_dis_list[i]
    country_pop = df_allpop[df_allpop['GID_0']==country_name].iloc[0][1]
    dis_pop = df_dis[df_dis['GID_dis']==dis_name].iloc[0][2]
        
    #find out total per of pop
    dis_per_pop = dis_pop/country_pop
    #extract total urban ntl info
    if len(dfurban_ntlsum[dfurban_ntlsum['GID_0']==country_name])>0:
        country_ntl = dfurban_ntlsum[dfurban_ntlsum['GID_0']==country_name].iloc[0][1]
    else: 
        country_ntl = 0
    #extract total urban pop info
    if len(dfurban_popsum[dfurban_popsum['GID_0']==country_name])>0:
        urban_country_pop = dfurban_popsum[dfurban_popsum['GID_0']==country_name].iloc[0][1]
    else:
        urban_country_pop = 0
    #extract dis urban ntl info
    if len(dfurban_ntldis[dfurban_ntldis['GID_dis']==dis_name])>0:
        dis_ntl = dfurban_ntldis[dfurban_ntldis['GID_dis']==dis_name].iloc[0][1]
    else:
        dis_ntl = 0
    #extract dis urban pop info
    if len(dfurban_popdis[dfurban_popdis['GID_dis']==dis_name])>0:
        urban_dis_pop = dfurban_popdis[dfurban_popdis['GID_dis']==dis_name].iloc[0][1]
    else:
        urban_dis_pop = 0
    
    rural_per_pop = (dis_pop-urban_dis_pop)/(country_pop-urban_country_pop)
    if country_ntl != 0: 
        urban_per_ntl = dis_ntl/country_ntl
    else:
        urban_per_ntl = 0
    agr = dfagr[dfagr['GID_0']==country_name].iloc[0][1]/100
    rural_per_gdp = rural_per_pop*agr
    urban_per_gdp = urban_per_ntl*(1-agr)
    perurgdppc = urban_per_gdp/urban_dis_pop
    perrugdppc = rural_per_gdp/(dis_pop-urban_dis_pop)
    #find out total per of gdp
    dis_per_gdp = rural_per_gdp+urban_per_gdp
    #append values
    result = result.append({cols[0]: country_name, cols[1]: dis_per_gdp,cols[2]: dis_per_pop,cols[3]: perurgdppc,cols[4]: perrugdppc,cols[5]: dis_name}, ignore_index=True)
    i = i+1
 

#calculate GINI
result['gdppc']= result['PerGDP']/result['PerPop']
result = result.sort_values('GID_0', ascending = False)
final_ctr = list(result.GID_0.unique())
df_all = result
# Finding Gini Coefficient
def gini(pop, inc):
    n = len(pop)
    a = 0
    p = pop[0]
    i = inc[0]
    for t in range(1,n):
        a  += (100-p)*(inc[t]-i) - ((pop[t]-p)*(inc[t]-i)/2)
        p = pop[t]
        i = inc[t]
    eq = (100.0*100.0)/2
    gini_co = (eq - a)/eq
    return gini_co
    
df_gini = pd.DataFrame()

for country in final_ctr:
    #print(country)
    df_ctr = df_all.loc[df_all['GID_0'] == country]
    df_ctr['PerGDP']=df_ctr['PerGDP']*100
    df_ctr['PerPop']=df_ctr['PerPop']*100
    print(country)
    df_ctr = df_ctr.sort_values(['gdppc'], ascending=[True])
    pop_perc = df_ctr["PerPop"].values.tolist()
    print("sum pop",sum(pop_perc))
    pop_perc = [0.0]+pop_perc
    i = 1
    while i < len(pop_perc):
        pop_perc[i] = pop_perc[i]+pop_perc[i-1]
        i = i+1
    gdp_perc = df_ctr["PerGDP"].values.tolist()
    print("sum gdp",sum(gdp_perc))
    gdp_perc = [0.0]+gdp_perc
    i = 1
    while i < len(gdp_perc):
        gdp_perc[i] = gdp_perc[i]+gdp_perc[i-1]
        i = i+1
    #print("sort done")
    gini_co = gini(pop_perc,gdp_perc)
    print(gini_co)
    df_gini = df_gini.append({'GID_0': country,'GINI': gini_co}, ignore_index=True)
    
ginirank = df_gini.sort_values(['GINI'], ascending=[True])


#calculate 20:20 ratios
dfallbackup = df_all
final_ctr = list(result.GID_0.unique())
df_ratio = pd.DataFrame()
for country in final_ctr:
    #print(country)
    df_ctr = df_all.loc[df_all['GID_0'] == country]
    df_ctr_bottom = df_ctr.sort_values(['gdppc'], ascending=[True])
    df_ctr_top = df_ctr.sort_values(['gdppc'], ascending=[False])
    
    gdp_bottom = 0
    pop_bottom = 0
    gdp_top = 0
    pop_top = 0
    i = 0
    excess_rate = 0
    while pop_bottom<= 0.2:
        gdp_val = df_ctr_bottom['PerGDP'].iloc[i]
        pop_val = df_ctr_bottom['PerPop'].iloc[i]
        i = i+1
        if pop_bottom+pop_val >0.2:
            excess_rate = (0.2-pop_bottom)/pop_val
            gdp_bottom = gdp_bottom+gdp_val*excess_rate
        else:
            gdp_bottom = gdp_bottom+gdp_val
        pop_bottom = pop_bottom+pop_val
        
    i = 0
    excess_rate = 0
    while pop_top<= 0.2:
        gdp_val = df_ctr_top['PerGDP'].iloc[i]
        pop_val = df_ctr_top['PerPop'].iloc[i]
        i = i+1
        if pop_top+pop_val >0.2:
            excess_rate = (0.2-pop_top)/pop_val
            gdp_top = gdp_top+gdp_val*excess_rate
        else:
            gdp_top = gdp_top+gdp_val
        pop_top = pop_top+pop_val
    ieratio = gdp_top/gdp_bottom
    df_ratio = df_ratio.append({'GID_0': country,'2020Ratio': ieratio}, ignore_index=True)
    
df_v3 = ginirank.merge(df_ratio,on='GID_0')

#save and update point data with GDP per pixel
filename = "/Volumes/Extreme 500/GINI/Python/v4/all_data25.csv"
df_all = pd.read_csv(filename, delimiter = ',')
df_all['GID_dis'] = df_all['GID_2']
#create new dis columjn
df_all.GID_dis.fillna(df_all.GID_1, inplace=True)
df_all.GID_dis.fillna(df_all.GID_0, inplace=True)

#join the gdppc data
df_allv2 = pd.merge(df_all, result,on='GID_dis')
df_allv2 = df_allv2[['FID','pointid','GID_0_x','SMOD','POP','PerUrGDPPC','PerRuGDPPC']]
df_allv2.columns = ['FID','pointid','GID_0','SMOD','POP','PerUrGDPPC','PerRuGDPPC']
#actual gdp per point
filename_gdp = "/Volumes/Extreme 500/GINI/Python/data/gdp.csv"
dfgdp = pd.read_csv(filename_gdp, delimiter = ',', usecols = ['Country Code','2015'])
dfgdp.columns = ['GID_0','GDP']
dfgdp = dfgdp.dropna()

df_allv2 = pd.merge(df_allv2, dfgdp,on='GID_0')

def f(row):
    if row['SMOD'] >20:
        val = row['PerUrGDPPC']*row['GDP']*row['POP'];
    else:
        val = row['PerRuGDPPC']*row['GDP']*row['POP'];
    return val
df_allv2['GDPPT'] = df_allv2.apply(f, axis=1)

df_allv2.to_csv('all_data_update.csv',index = False)

