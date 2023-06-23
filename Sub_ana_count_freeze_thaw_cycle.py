# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 22:32:49 2023

@author: mugalsamrat.dahal
"""

import os, glob
import pandas as pd



import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from sklearn.metrics import r2_score


from plotnine import *
###



### Declare main directory ###

mydir = "C:\\Users\\mugalsamrat.dahal\\OneDrive - Washington State University (email.wsu.edu)\\Paper2\\Weppwatershed\\freeze_thaw_cycles\\Type_D"
os.chdir(mydir)
###############

# from analyze_freeze_thaw_method_2 import analyze_freeze_thaw_2
# from analyze_freeze_thaw_method_2 import julian_to_date
from count_freeze_thaw_method2 import count_freeze_thaw_cycles


#### This code should be run after classifying the freeze and thaw soil state which is done using "Main_analysis.py" ..
main_ft_data = pd.read_csv("data_with_raintype.csv")



zones = ["High", "Intermediate", "Low"]

period = ["Past","Present"]

### using mean temperature as the variable
Tvars =["Tavg"]

first = 0           # flag for joining all iteration # Method 1

df_final = []       # for saving df in each loop


for Tvar in Tvars:
    for z in zones:
        for p in period:
            #z = "Intermediate"
            #p = "Past"

            ### Selecting the zone and period of interest first
            
            ft_data = main_ft_data[(main_ft_data["Zone"]==z) & (main_ft_data["Period"]==p)]

            ### applying the count function
            ft_data = count_freeze_thaw_cycles(ft_data)

            ft_data['threshold'] = Tvar
            
            df_final.append(ft_data)

            
final_data = pd.concat(df_final)

#final_data.to_csv("raintype_ft_Tavg.csv")

final_data_comb = final_data
######################################
### For freeze thaw cycles ##### 
#final_data = pd.concat([final_data, final_data2])

####summarize###

#Annual
FT_sum = final_data_comb.groupby(['Zone','Period','Wateryear','threshold'])['index'].sum().reset_index()
# Seasonal
FT_sum_seas = final_data_comb.groupby(['Zone','Period','Wateryear','seasons','threshold'])['index'].sum().reset_index()

# Annual
FT_sum_avg = FT_sum.groupby(['Zone','Period','threshold'])['index'].mean().reset_index()

#Seasonal
FT_sum_seas_avg = FT_sum_seas.groupby(['Zone','Period','seasons','threshold'])['index'].mean().reset_index()    
    
### plot with plot_nine library #####
pA = ggplot(FT_sum_avg, aes('Zone', 'index', fill = 'Period'))+geom_bar(stat = "identity", position = "dodge")+facet_wrap("threshold", ncol=1)+ggtitle("Average Freeze thaw cycle by zone and threshold") 
ggsave(pA, "FT_cycles_annual_average_meth_.png", height = 10, width = 12)

pB = ggplot(FT_sum_seas_avg, aes('seasons', 'index', fill = 'Period'))+geom_bar(stat = "identity", position = "dodge")+facet_grid("Zone~threshold")+ggtitle("Average Freeze thaw cycle by zone and threshold")
ggsave(pB, "FT_cycles_seasonal_average_meth_2.png", height = 10, width = 12)

###########################################

