# -*- coding: utf-8 -*-
"""
Created on Tue May 16 16:41:27 2023

@author: YasinHammad(Ascend)
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime

path = r'C:\Users\YasinHammad(Ascend)\Desktop\OOS-Analysis-Bot'
os.chdir(path)

stock_consumption = pd.read_excel('stock_consumption.xlsx')
contracts_summary = pd.read_excel('contracts_summary.xlsx')
batch_details = pd.read_excel('batch_details_processed.xlsx')

oos_table = stock_consumption[(stock_consumption.stock_category == "Out of Stock")]

oos_table['required_quantity'] = oos_table['average_consumption']*2

oos_table = pd.merge(oos_table,contracts_summary[["region_id","item_id","supply_ratio"]],on=['region_id',"item_id"],how='left')
oos_table= oos_table.drop(columns=['total_stock','average_consumption','covering_months','stock_category'])
print(oos_table)

oos_table.to_excel('oos_table.xlsx')


overstock_table = stock_consumption[(stock_consumption.stock_category == "Over Stock")|(stock_consumption.stock_category =="Avaiable_Non_Moving_items")]

overstock_table = pd.merge(overstock_table,batch_details[["region_id","item_id","batch_id",'expiry_date']],on=['region_id',"item_id"],how='left')

overstock_table ['available_quantity'] = overstock_table['total_stock'] - overstock_table['average_consumption']*6

overstock_table= overstock_table.drop(columns=["total_stock",'average_consumption','covering_months','stock_category'])

overstock_table.to_excel('overstock_table.xlsx')