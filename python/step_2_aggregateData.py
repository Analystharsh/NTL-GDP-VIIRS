#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 19 14:01:06 2019

@author: xuantongwang
"""

import pandas as pd
import numpy as np

#Find REAL NAME
filename = "/Volumes/Extreme 500/GINI/Python/data/gadm2_info.csv"
df_name1= pd.read_csv(filename, delimiter = ',',usecols=['GID_0','GID_2'])
filename = "/Volumes/Extreme 500/GINI/Python/data/gadm2newid.csv"
df_name2= pd.read_csv(filename, delimiter = ',',usecols=['GID_2','New_ID2'])
df_name2.columns = ['GID_2','gadm2_1']

df_name_new = pd.merge(df_name1, df_name2,on='GID_2')


#filename = "E:/GINI/Python/data/urbandata.csv"
filename = "/Volumes/Extreme 500/GINI/Python/v4/if_urban_filtered.csv"
#rename column
df_urban = pd.read_csv(filename, delimiter = ',')
df_urban['NAME'] = df_urban['GID_0']

len(df_urban.GID_0.unique())
len(df_urban)
#summarize urban pop and ntl data
dfurban_ntlsum = df_urban.groupby(['GID_0'])['NTL'].sum().reset_index().sort_values('NTL', ascending = False)
dfurban_ntlsum.columns = ['NAME','SumNTL']

dfurban_popsum = df_urban.groupby(['GID_0'])['POP'].sum().reset_index().sort_values('POP', ascending = False)
dfurban_popsum.columns = ['NAME','SumUrPop']

dfurban_ntldis = df_urban.groupby(['GID_2'])['NTL'].sum().reset_index().sort_values('NTL', ascending = False)
dfurban_ntldis.columns = ['GID_2','DisNTL']

dfurban_popdis = df_urban.groupby(['GID_2'])['POP'].sum().reset_index().sort_values('POP', ascending = False)
dfurban_popdis.columns = ['GID_2','DisUrPop']

#append all pop
#filename_allpop = "E:/GINI/Python/data/ntl0_zonal.csv"
filename = "/Volumes/Extreme 500/GINI/Python/v4/all_data.csv"

df_all = pd.read_csv(filename, delimiter = ',')


df_allpop = df_all.groupby(['GID_0'])['POP'].sum().reset_index().sort_values('POP', ascending = False)
df_allpop.columns = ['NAME','TotalPOP']

df_dis = df_all.groupby(['GID_0','GID_2'])['POP'].sum().reset_index().sort_values('POP', ascending = False)
df_dis.columns = ['NAME','GID_2','DisPOP']

filename_agr = "/Volumes/Extreme 500/GINI/Python/data/agr.csv"
dfagr = pd.read_csv(filename_agr, delimiter = ',', usecols = ['Country Code','2015'])
dfagr.columns = ['NAME','AGR']
dfagr = dfagr[dfagr['AGR'].notnull()]
namelist = dfagr.NAME.unique().tolist()
#produce a new table
df_dis = df_dis[df_dis.NAME.isin(namelist)]
gid0list = df_dis.NAME.tolist()
gid2list = df_dis.GID_2.tolist()
cols = ['NAME', 'PerGDP', 'PerPop','PerUrGDPPC','PerRuGDPPC','GID_2']
result  = pd.DataFrame(columns = cols)

i = 0
while i < len(gid0list):
    #print(i)
    #find out country name
    country_name = gid0list[i]
    dis_name = gid2list[i]
    country_pop = df_allpop[df_allpop['NAME']==country_name].iloc[0][1]
    dis_pop = df_dis[df_dis['GID_2']==dis_name].iloc[0][2]
        
    #find out total per of pop
    dis_per_pop = dis_pop/country_pop
    country_ntl = dfurban_ntlsum[dfurban_ntlsum['NAME']==country_name].iloc[0][1]
    if len(dfurban_ntldis[dfurban_ntldis['GID_2']==dis_name])>0:
        dis_ntl = dfurban_ntldis[dfurban_ntldis['GID_2']==dis_name].iloc[0][1]
    else:
        dis_ntl = 0
    if len(dfurban_popdis[dfurban_popdis['GID_2']==dis_name])>0:
        urban_dis_pop = dfurban_popdis[dfurban_popdis['GID_2']==dis_name].iloc[0][1]
    else:
        urban_dis_pop = 0
    urban_country_pop = dfurban_popsum[dfurban_popsum['NAME']==country_name].iloc[0][1]
    
    rural_per_pop = (dis_pop-urban_dis_pop)/(country_pop-urban_country_pop)
    urban_per_ntl = dis_ntl/country_ntl
    agr = dfagr[dfagr['NAME']==country_name].iloc[0][1]/100
    rural_per_gdp = rural_per_pop*agr
    urban_per_gdp = urban_per_ntl*(1-agr)
    perurgdppc = urban_per_gdp/urban_dis_pop
    perrugdppc = rural_per_gdp/(dis_pop-urban_dis_pop)
    #find out total per of gdp
    dis_per_gdp = rural_per_gdp+urban_per_gdp
    #append values
    result = result.append({cols[0]: country_name, cols[1]: dis_per_gdp,cols[2]: dis_per_pop,cols[3]: perurgdppc,cols[4]: perrugdppc,cols[5]: dis_name}, ignore_index=True)
    i = i+1
    
    

######Part 4
#['NAME', 'PerGDP', 'PerPop']
#result = df_urb
result['gdppc']= result['PerGDP']/result['PerPop']
result.to_csv('gdpprofiledata.csv')
print(len(result.NAME.unique()))
result = result.sort_values('NAME', ascending = False)
print(result.PerGDP.sum(),"gdpsum")
print(result.PerPop.sum(),"popsum")
final_ctr = list(result.NAME.unique())

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
    df_ctr = df_all.loc[df_all['NAME'] == country]
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
    df_gini = df_gini.append({'NAME': str(country),'GINI': gini_co}, ignore_index=True)
    
ginirank = df_gini.sort_values(['GINI'], ascending=[True])
print(ginirank)
print("Unique Countries", len(ginirank.NAME.unique()))

#save to model
ginirank.to_csv(r'/Volumes/Extreme 500/GINI/Python/v4/ntlgini_all_dis.csv',index = False)


###########ADDITIONAL INFO
#filename_ntlgini = "ntlgini_allv2.csv"
#df_v2 = pd.read_csv(filename_ntlgini)


##attach smod values
#filename_allpop = "/Volumes/Extreme 500/GINI/Python/data/allpopdata.csv"
#df_all = pd.read_csv(filename_allpop, delimiter = ',')
#df_smod = pd.merge(df_all, df_name_new,on='gadm2_1')
##sum each smod pop
#df_smod2 = df_smod.groupby(['GID_0','smod_1'])['VALUE'].sum().reset_index().sort_values('VALUE', ascending = False)
##find percent
#df_all2 = pd.merge(df_all, df_name_new,on='gadm2_1')
#df_allpop2 = df_all2.groupby(['GID_0'])['VALUE'].sum().reset_index().sort_values('VALUE', ascending = False)
#df_smod3 = pd.merge(df_smod2, df_allpop2,on='GID_0')
#list(df_smod3)
#
#names = df_smod3.GID_0.unique().tolist()
#i = 0
#smodids = df_smod3['smod_1'].unique().tolist()
#for smodid in smodids:
#    cols = ['NAME']
#    cols.append('SMOD'+str(smodid))
#    result_temp  = pd.DataFrame(columns = cols)
#
#    dfsmodtemp = df_smod3[df_smod3['smod_1']==smodid]
#    for name in names:
#        dfsmodtemp2 = dfsmodtemp[dfsmodtemp['GID_0']==name]
#        if len (dfsmodtemp2)>0:
#            per_smod = (dfsmodtemp2['VALUE_x'].iloc[0])/(dfsmodtemp2['VALUE_y'].iloc[0])
#        else:
#            per_smod = 0
#        result_temp = result_temp.append({cols[0]:name, cols[1]:per_smod},ignore_index=True)
#    df_v2 = df_v2.merge(result_temp, how='left', on='NAME')
#    #df_v2 = df_v2.merge(df_v2,result_temp,on='NAME')
#df_v2.to_csv('ntlgini_allv2_v2.csv',index = False)

##calculate 2020 ratio


dfallbackup = df_all


df_ratio = pd.DataFrame()
for country in final_ctr:
    #print(country)
    df_ctr = df_all.loc[df_all['NAME'] == country]
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
    print(country,ieratio)
    df_ratio = df_ratio.append({'NAME': str(country),'2020Ratio': ieratio}, ignore_index=True)
    
df_v3 = ginirank.merge(df_ratio,on='NAME')

#join with continent and income data
filename2 = "/Volumes/Extreme 500/GINI/Python/data/income_code.csv"
df_inc= pd.read_csv(filename2,delimiter = ',')
df_inc.columns = ['NAME', 'NameF', 'Income']
filename3 = "/Volumes/Extreme 500/GINI/Python/data/continentcode.csv"
df_cont= pd.read_csv(filename3,delimiter = ',')
df_cont.columns = ['NAME', 'Continent']

df_v3 = pd.merge(df_v3, df_inc,on='NAME')
#df_v3 = pd.merge(df_v3, df_cont,on='NAME')

df_v3.to_csv('ntlginiratio_dis.csv',index = False)


#save point copy
filename = "/Volumes/Extreme 500/GINI/Python/v4/all_data.csv"

df_all = pd.read_csv(filename, delimiter = ',')

df_allv2 = pd.merge(df_all, result,on='GID_2')
df_allv2 = df_allv2[['FID','pointid','GID_0','GID_2','SMOD','PerUrGDPPC','PerRuGDPPC']]

filename_gdp = "/Volumes/Extreme 500/GINI/Python/data/gdp.csv"
dfgdp = pd.read_csv(filename_gdp, delimiter = ',', usecols = ['Country Code','2015'])
dfgdp.columns = ['GID_0','GDP']
dfgdp = dfgdp.dropna()

df_allv2 = pd.merge(df_allv2, dfgdp,on='GID_0')

def f(row):
    if row['SMOD'] >20:
        val = row['PerUrGDPPC']*row['GDP'];
    else:
        val = row['PerRuGDPPC']*row['GDP']
    return val
df_allv2['GDPPT'] = df_allv2.apply(f, axis=1)

df_allv2.to_csv('all_datapt_update.csv',index = False)
