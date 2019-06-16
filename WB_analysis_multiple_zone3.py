# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 12:56:56 2019

@author: liu26
"""
import pandas as pd
import numpy as np

"""
# =============================================================================
# Please predefine following variables of the Water Balance analysis before executing the script
# =============================================================================

"""
Totalzones = 9                                                                  #How many budget zones are presented in the WB file.
start = 'start date'                                                            # start date of your simulation
end = ' end date '                                                              # end date of your simulation
freq =  'MS'                                                                    # frequency of your stress period 
date = pd.date_range(start=start, end=end,freq=freq, normalize=False, \
                     closed=None)                                               # generate a series of date of each stress period

#period = 35                                                                    #or define the total number of stress periods instead of
                                                                                #frequency then, comment the two lines above
#date = pd.date_range(start=start, end=end,periods = period, normalize=False, closed=None)

date = date.to_frame(index = False, name = 'DATE')
directory  = 'yourfiledirectory' # your file directory
filename = '/yourfilename'                                               # your file name
names = ['TOTAL TIME', 'STRESS PERIOD', 'TIMESTEP', 'BUDGET ID']                        # still can add more column names based on your own case
        
#%% Import dataset, name the columns and assign date to it. 
df = pd.read_csv(directory+filename, index_col = False, skiprows = 0)           # import dataset
df.columns = names + df.columns.tolist()[len(names):]                           # assign column name to the dataframe
n=-1
date_new=[]
for i in range(Totalzones*len(date)):
    if np.mod(i,Totalzones)==0:
        n+=1
    date_new.append(date['DATE'][n])
df['DATE']= date_new                                                            # assign a new date column to the dataset   

length = df['TOTAL TIME'].diff(Totalzones)                                      # calculate period length
length.loc[length.isnull()] = df['TOTAL TIME']     
df['PERIOD LENGTH'] = length                                                    # assign a new period length column to the dataset
#%% Unit transfer and sorting
df.iloc[:,4:-2] = df.iloc[:,4:-2].mul(df['PERIOD LENGTH'],axis = 0)             # transfer the unit of the data from m3/d to m3/mth
df.set_index(['BUDGET ID','DATE'],inplace = True)                               # use multi-index. zone budget ID as the 1st level index, date as the 2nd level index
df.sort_index(axis = 0, level =0, ascending = True, inplace = True)             # sorting by zone budget ID

#%% Water Budget for the whole domain

WB_yearly = df.iloc[:,4:].groupby(pd.Grouper(level='DATE', freq='A')).sum()     #sum up the monthly data into yearly data. 

"""
# =============================================================================
# Predefine variables for the budget zone you would like to check
# =============================================================================
"""
targetzone = 1

zonebudget = df.iloc[df.index.get_level_values('BUDGET ID') == targetzone]      # flitering out the target zone you would like to check up
zone_yearly = zonebudget.iloc[:,4:].groupby(pd.Grouper(level='DATE', freq='A')).sum() #calculate the yaerly budget of your target zone. 

#%%
summaryfile = pd.ExcelWriter('your excel file', engine = 'openpyxl')
sheet_name = 'monthly'
df.to_excel(summaryfile,sheet_name =sheet_name,index = True)
summaryfile.save()

