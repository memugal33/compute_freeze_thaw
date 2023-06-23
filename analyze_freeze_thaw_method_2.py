# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 10:34:21 2023

@author: mugalsamrat.dahal
"""

import pandas as pd
import os, glob

import datetime


### Need this to convert julian day to day and month ###
def julian_to_date(julian_day, year):
    dt = datetime.datetime(year=year, month=1, day=1) + datetime.timedelta(julian_day - 1)
    return dt.day, dt.month
###########################


# maindir =  "C:\\Users\\mugalsamrat.dahal\\OneDrive - Washington State University (email.wsu.edu)\\Paper2\\Weppwatershed\\freeze_thaw_cycles\\Type_B"
# os.chdir(maindir)
# subdir = "high_past_wat"

# dirs = maindir + "\\"+subdir+"\\H126.wat.dat" 

# names = ['OFE','J','Y','P','RM','Q','Ep','Es','Er','Dp','UpStrmQ','SubRIn',
#          'Latqcc','Total_Soil_Water','Total_Frozen_Water','Snow_water','QOFE',
#          'Tile','Irr','Area']

# data = pd.read_table(dirs, skiprows = 22, delim_whitespace=True, names = names)

# data_temp = pd.read_csv("temp_prcp_data.csv")
# data_temp = data_temp[(data_temp['Zone']=="High")&(data_temp['Period']=="Past")]

# data_temp["Tavg"] = (data_temp['Tmax'] + data_temp["Tmin"])/2
# Tvar = "Tavg"


def analyze_freeze_thaw_2(data, data_temp, Tvar):
    
    '''
    data: The water balance output for single hillslope from WEPP, single zone, single period
    data_temp: The temperature data for single zone, single period
    
    Tvar: The temperature threshold that will be used
    
    General Rule:
        1) If todays frozen water is less than previous day frozen water
            soil state == thawed
        2) If todays frozen water is equal to previous day frozen water
            soil state = previous day's soil state
        3) If todays frozen water is higher than previous day frozen water
            soil state == frozen
    
    
    Task completed by the function
        1) Add a colomn with soil state
        2) Add a colomn with rain type
    '''
    
    
    ### calculate the mean for two ofes ###
    
    data = data.groupby(['Y','J']).mean().reset_index()
    
    ### get month and day from julianday
    data[['Day','Month']] = data.apply(lambda row: pd.Series(julian_to_date(int(row['J']), int(row['Y']))), axis = 1)
    
    #### Merge with temperature data
    data_analyse = pd.merge(data, data_temp, left_on = ["Y","Month","Day"], right_on= ["Year", "Month","Day"])
    
    ##### setting new colomns ############
    data_analyse['Soilstate']= None
    data_analyse["Raintype"] = None
    
    ### This is to count which condition was met for classification
    data_analyse["Myindices"] = None
    
    
    #### initialize #########
    j = 0
    prev_day_soil_state = None
    
    
    #### function for the general rule ############
    
    def det_sl_stt(tday_fw, pday_fw, prev_soil_state):
        '''
        

        Parameters
        ----------
        tday_fw : int
            Todays frozen water
        pday_fw : int
            Yesterdays frozen water
        prev_soil_state : str
            Previous days soil state

        Returns
        -------
        list
            Soil state and index for which condition was met.

        '''
        if tday_fw<pday_fw:
            slstate = "Thawing"
            ind = "1"
        elif tday_fw==pday_fw:
            if tday_fw == 0:
                slstate = "Unfrozen"
                ind = "4"
            else:
                slstate = prev_soil_state
                ind = "2"
        else:
            slstate = "Frozen"
            ind = "3"
        return [slstate,ind]
    
    ##############################################
    # First loop starts
    while j<len(data_analyse):
        #j = 1
        
        ### Get temperature, frozen water and precip
        Tvrs = data_analyse[Tvar].iloc[j]
        today_frz_wat = data_analyse['Total_Frozen_Water'].iloc[j]
        p = data_analyse["P"].iloc[j]
        
        ### for first row 
        if j==0:
            
            if Tvrs>0 or today_frz_wat==0:
                slstate = "Unfrozen"
            else:
                slstate = "Frozen"
            
            ### This is the index indicating that this condition was met
            indA = "Ca0"
        else:
            ## get the soil water and frozen water for today and previous day #######
            prev_day_soil_wat = data_analyse['Total_Soil_Water'].iloc[j-1]
            today_soil_wat = data_analyse['Total_Soil_Water'].iloc[j]
            prev_day_frz_wat = data_analyse['Total_Frozen_Water'].iloc[j-1]
            #######
            
            #### Still want to set up a condition with Temperature and soil water
            ## but the main deciding factor is the frozen water ###
            
            
            if Tvrs>0:
                
                ### setting up soil water conditions
                
                if today_soil_wat > prev_day_soil_wat:
                    
                    ### using the function to compute soil state
                    slstate = det_sl_stt(today_frz_wat, prev_day_frz_wat, prev_day_soil_state)[0]
                    
                    ### adding the index that this condition was met
                    ind1 = "a"+det_sl_stt(today_frz_wat, prev_day_frz_wat, prev_day_soil_state)[1]
            
                elif today_soil_wat == prev_day_soil_wat:
                    
                    ### using the function to compute soil state
                    slstate = det_sl_stt(today_frz_wat, prev_day_frz_wat, prev_day_soil_state)[0]
                    
                    ### adding the index that this condition was met
                    ind1 = "b"+det_sl_stt(today_frz_wat, prev_day_frz_wat, prev_day_soil_state)[1]
                    
                else:
                    
                    ### using the function to compute soil state
                    slstate = det_sl_stt(today_frz_wat, prev_day_frz_wat, prev_day_soil_state)[0]
                    
                    ### adding the index that this condition was met
                    ind1 = "c"+det_sl_stt(today_frz_wat, prev_day_frz_wat, prev_day_soil_state)[1]
                
                ### adding the index that this condition was met
                indA = "A"+ind1
                
                ##### This chunk is if Tvar<=0
            else:
                
                if today_soil_wat > prev_day_soil_wat:
                    
                    slstate = det_sl_stt(today_frz_wat, prev_day_frz_wat, prev_day_soil_state)[0]
                    
                    ### adding the index that this condition was met
                    ind1 = "a"+det_sl_stt(today_frz_wat, prev_day_frz_wat, prev_day_soil_state)[1]
            
                elif today_soil_wat == prev_day_soil_wat:
                    
                    slstate = det_sl_stt(today_frz_wat, prev_day_frz_wat, prev_day_soil_state)[0]
                    
                    ### adding the index that this condition was met
                    ind1 = "b"+det_sl_stt(today_frz_wat, prev_day_frz_wat, prev_day_soil_state)[1]
                    
                else:
                    
                    slstate = det_sl_stt(today_frz_wat, prev_day_frz_wat, prev_day_soil_state)[0]
                    
                    ### adding the index that this condition was met
                    ind1 = "c"+det_sl_stt(today_frz_wat, prev_day_frz_wat, prev_day_soil_state)[1]
                
                ### adding the index that this condition was met
                indA = "B"+ind1
                
                
        #### Now classify the precipitation event based on the soil state ####
        
        if p>0:
            rtype = "Rain on "+slstate+ " Soil"
        else:
            rtype = "No rain"
        
        ### save the values to respective places 
        
        data_analyse["Soilstate"].iloc[j]=slstate
        data_analyse["Raintype"].iloc[j]=rtype
        data_analyse["Myindices"].iloc[j] = indA
        
        ### assign the soil state to previous soil state 
        prev_day_soil_state = slstate
        
        ## move the loop forward
        j = j+1
        

    return data_analyse  
    
   
    
   
    
   
    
   
    
   
    
   
    
   
    
   
    
