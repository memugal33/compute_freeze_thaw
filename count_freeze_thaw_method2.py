# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 17:31:06 2023

@author: mugalsamrat.dahal
"""

def count_freeze_thaw_cycles(data_analyse):


    '''
        data_analyse = dataframe
        
        This dataframe needs to have soil state colomn which defines the soil as
        frozen, unfrozen or thawed.

        
        
    
        Task completed by the function:
            New colomn will be added which will add 1 to the row each time a freeze thaw cycle is completed
            
        Rules for freeze thaw cylce completion:
            Condition 1:
                i) If the soil state change from Frozen to thaw half cycle is complete
                ii) If the soil state change from thaw back to frozen... 1 cycle is complete..
            Condition 2:
                i) If the soil state change from thaw to frozen half cycle is complete
                ii) If the soil state change from frozen back to thaw... 1 cycle is complete..
            
            Task: identify the row where Freeze-thaw cycle is complete.. And add value 1 in that row.

            
            Condition 1 or 2 will be initiated based on the value of first row.
            Condition 1: First day is frozen
            
            1) Search for the closest thawed day, half cycle complete
            2) Now search for the closest frozen day, full cycle complete
            
            Condition 2: First day is thawed
            
            1) Search for the closest frozen day, half cycle complete
            2) Now search for the closest thawed day, full cycle complete
            
    '''
    
    
    ### function to check todays soil state ###
    def isfrozen(soilstate):
        
        if soilstate=="Frozen":
            a = True
        else:
            a = False
        return a
    
    
    data_analyse.loc[:,'index'] = 0
    j = 0   
    
    while j < len(data_analyse):
        
                ### The flag needs to be updated again after each cycle ###
                ### so need to erase the previous values ###
        
                myflag = None
                myflag2 = None
        
                ##### Second loop starts ##############
                for i in range(j, len(data_analyse)):
                    #i = 1
                    ##### This will initiate with either Condition 1 or Condition 2 ######
                    myflag = isfrozen(data_analyse.iloc[i]['Soilstate'])
                    ##############################################
        
                    ### Need to save this in another flag ####
                    myflag2 = myflag
                    ####################
        
                    #### start another loop to find where either freeze switches to thaw or vice versa
        
                    while myflag2 == myflag:
                        i = i+1
        
                        ### Need to break out of the loop if we reach end of the data ###
        
                        if i >= len(data_analyse):
                            break
                        #################################################################
        
                        #myflag2 = IsLessOrEqualToZero(data.loc[i, Tvar])
                        myflag2 = isfrozen(data_analyse.iloc[i]['Soilstate'])
                        
                        ### This loop will end as soon as the myflag doesnt match with myflag2
                        ### In other words the half cycle is complete
                        ### We have the location where that happens in the form of "i"
        
                    #### Again the same idea for the second half of the cyle #######
    
                    ### Need to save this in another flag ###
                    myflag = myflag2
                    #########################################
        
                    while myflag == myflag2:
                        i = i+1
        
                        ### Need to break out of the loop if we reach end of the data ###
        
                        if i >= len(data_analyse):
                            break
                        #################################################################
        
                        myflag = isfrozen(data_analyse.iloc[i]['Soilstate'])
        
                        ### This loop will end as soon as the myflag2 doesnt match with myflag
                        ### In other words the full freeze thaw cycle is now complete
                        ### We have the location where that happens in the form of "i"
        
                    ### Need to break out of the loop if we reach end of the data ###
                    if i >= len(data_analyse):
                        break
                    #################################################################
        
              
                    #####################################
        
                    data_analyse["index"].iloc[i] = 1

                    ### by doing this i am skipping some steps from first loop ###
                    ### Because those rows are already covered by second loop ###
        
                    j = i-1

                    # I am doing minus 1 here because in the next loop....
                    #.... I want the cycle to continue from this row itself
                    
        
                    #### Now second loop doesnt need to continue further, so break! ###
                    break
                    ########### It will initiate again with updated flags from first loop ###
        
                j = j + 1        
        
    return data_analyse
