# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 14:31:04 2023

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

from analyze_freeze_thaw_method_2 import analyze_freeze_thaw_2
from analyze_freeze_thaw_method_2 import julian_to_date

main_temp_data = pd.read_csv("temp_prcp_data.csv")

main_temp_data['Tavg']=(main_temp_data['Tmax']+main_temp_data['Tmin'])/2

### compute rain on thawed soil ###

zones = ["High", "Intermediate", "Low"]

period = ["Past","Present"]

### using mean temperature as the variable
Tvars =["Tavg"]

first = 0           # flag for joining all iteration # Method 1


## name of variables in the water balance file
names = ['OFE','J','Y','P','RM','Q','Ep','Es','Er','Dp','UpStrmQ','SubRIn',
         'Latqcc','Total_Soil_Water','Total_Frozen_Water','Snow_water','QOFE',
         'Tile','Irr','Area']



df_final = []       # for saving df in each loop


for Tvar in Tvars:
    for z in zones:
        for p in period:
            #z = "Intermediate"
            #p = "Past"
            fold_name = z+"_"+p+"_wat"
            
            temp_data = main_temp_data[(main_temp_data["Zone"]==z) & (main_temp_data["Period"]==p)]
            
            ### Freeze thaw cycle is computed using the function

            ## First reading water balance file for specific zone and period
            dirs = mydir + "\\"+fold_name+"\\H126.wat.dat" 
            wat_data = pd.read_table(dirs, skiprows = 22, delim_whitespace=True, names = names)
            
            ### applying the function for classification
            loop_data = analyze_freeze_thaw_2(wat_data, temp_data, Tvar)
            
            
            loop_data['threshold'] = Tvar
            
            
            ###### After completing this task, would like to join all the iteration as single dataframe ###
            ################################################################################################
            
            #### Method 1 ######
            
            # if first == 0:
                
            #     final_data = loop_data
            #     first = first + 1
            
            # else:
            #     final_data = pd.concat(final_data, loop_data)
            
            #### Method 2 ##########
            
            df_final.append(loop_data)

        ############################
    
    ###############################################################################################
    

final_data = pd.concat(df_final)

final_data.to_csv("data_with_raintype.csv")


###################ANALYSIS#################################

### summarize which condition is met the most #####

# Annual 
type_sum = final_data.groupby(['Zone','Myindices','threshold'])['Day'].count().reset_index()
#eve_type_sum_avg = eve_type_sum.groupby(['Zone','Period','Raintype','threshold'])['Day'].mean().reset_index()
    
# Seasonal 
#eve_type_sum_seas = final_data.groupby(['Zone','Period','Wateryear','seasons','Raintype','threshold'])['Day'].count().reset_index()
#eve_type_sum_seas_avg = eve_type_sum_seas.groupby(['Zone','Period','seasons','Raintype','threshold'])['Day'].mean().reset_index()


### plot with plot_nine library #####
pF = ggplot(type_sum, aes('Myindices', 'Day'))+geom_bar(stat = "identity", position = "dodge")+facet_wrap("Zone", scales ="free") +ggtitle("Rain type by zone and threshold")
ggsave(pF, "count_type_condition_tavg.png", height = 10, width = 18)



##### Analyse rain on thaw events ######

### summarize #####

# Annual 
eve_type_sum = final_data.groupby(['Zone','Period','Wateryear','Raintype','threshold'])['Day'].count().reset_index()
eve_type_sum_avg = eve_type_sum.groupby(['Zone','Period','Raintype','threshold'])['Day'].mean().reset_index()
    
# Seasonal 
eve_type_sum_seas = final_data.groupby(['Zone','Period','Wateryear','seasons','Raintype','threshold'])['Day'].count().reset_index()
eve_type_sum_seas_avg = eve_type_sum_seas.groupby(['Zone','Period','seasons','Raintype','threshold'])['Day'].mean().reset_index()


### plot with plot_nine library #####
pC = ggplot(eve_type_sum_avg, aes('Zone', 'Day', fill = 'Period'))+geom_bar(stat = "identity", position = "dodge")+facet_grid("Raintype~threshold", scales ="free") +ggtitle("Average Rain type by zone")
ggsave(pC, "raintype_annual_avg_meth_2.png", height = 10, width = 12)
### only rain on thawed events ####
eve_type_sum_seas_avg_nly_thw = eve_type_sum_seas_avg[eve_type_sum_seas_avg['Raintype']=="Rain on Thawing Soil"]

pD = ggplot(eve_type_sum_seas_avg_nly_thw, aes('seasons', 'Day', fill = 'Period'))+geom_bar(stat = "identity", position = "dodge")+facet_grid("threshold ~ Zone", scales="free_y")+ggtitle("Average Rain on thawing soil by zone and seasons")
ggsave(pD, "rainonthaw_seasonal_avg_meth_2.png", height = 10, width = 12)
    
 #############################################################################   

####### look for rain on thaw situation in some years of interest (extreme high and low erosion years) 

years_of_interest  = [1959,1961,1978,1993,1995,2001,2003,2013,2016]
years = years_of_interest
########### Annual ###############
check_eve = eve_type_sum[eve_type_sum['Wateryear'].isin(years)]
check_avg = eve_type_sum_avg
check_avg["Wateryear"] = "Average"


## combining specific year values with averages ###
check_final = pd.concat([check_eve,check_avg])
check_final['Wateryear'] = check_final['Wateryear'].astype(str)
check_final_thawing = check_final[check_final["Raintype"]=="Rain on Thawing Soil"]


pK = ggplot(check_final_thawing, aes('Wateryear', 'Day', fill = 'Period'))+geom_bar(stat = "identity", position = "dodge")+facet_wrap("Zone", scales="free_y")+ggtitle("Average Rain on thawing soil by zone comparisons")
ggsave(pK, "rainonthaw_avg_compare.png", height = 10, width = 18)


########### Seasonal ###############

check_eve_seas = eve_type_sum_seas[eve_type_sum_seas['Wateryear'].isin(years)]
check_avg_seas = eve_type_sum_seas_avg
check_avg_seas["Wateryear"] = "Average"

check_final_seas = pd.concat([check_eve_seas,check_avg_seas])
check_final_seas['Wateryear'] = check_final_seas['Wateryear'].astype(str)
check_final_thawing_seas = check_final_seas[check_final_seas["Raintype"]=="Rain on Thawing Soil"]

pK2 = ggplot(check_final_thawing_seas, aes('Wateryear', 'Day', fill = 'Period'))+geom_bar(stat = "identity", position = "dodge")+facet_grid("Zone ~ seasons", scales="free_y")+ggtitle("Average Rain on thawing soil by zone comparisons")
ggsave(pK2, "rainonthaw_avg_compare_seas.png", height = 10, width = 18)

 

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
