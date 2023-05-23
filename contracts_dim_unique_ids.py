# -*- coding: utf-8 -*-
"""
Created on Tue May 23 10:50:24 2023

@author: YasinHammad(Ascend)
"""

#Import Libraries

import pandas as pd
import os

#Defining Path

path = r'C:\Users\YasinHammad(Ascend)\Desktop\OOS-Analysis-Bot'
#path = r'D:\Ascend\Analytics_Use_Cases\OOS-Analysis-Bot'
os.chdir(path)


#Defining required tables in Dataframe

contracts_dim = pd.read_excel('contracts_dim.xlsx')



#Sorting 

contracts_dim = contracts_dim.sort_values('shipment_counts', ascending=False)
contracts_dim = contracts_dim.drop_duplicates(subset=['contract_id'])

#Exporting File
contracts_dim.to_excel('contracts_dim_new.xlsx',index=False)