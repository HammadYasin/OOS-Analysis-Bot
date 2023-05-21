import pandas as pd
import numpy as np
import os
import datetime as dt
from datetime import datetime, timedelta

# path = r'C:\Users\YasinHammad(Ascend)\Desktop\OOS-Analysis-Bot'
path = r'D:\Ascend\Analytics_Use_Cases\OOS-Analysis-Bot'
os.chdir(path)

stock_consumption = pd.read_excel('stock_consumption.xlsx')
contracts_summary = pd.read_excel('contracts_summary.xlsx')
batch_details = pd.read_excel('batch_details_processed.xlsx')

oos_table = stock_consumption[(stock_consumption.stock_category == "Out of Stock")]
oos_table['required_quantity'] = oos_table['average_consumption'] * 2
oos_table = pd.merge(oos_table, contracts_summary[["region_id","item_id","supply_ratio"]], on = ['region_id',"item_id"],how='left')
oos_table= oos_table.drop(columns = ['total_stock','average_consumption','covering_months','stock_category'])
# oos_table.to_excel('oos_table.xlsx')


overstock_table = stock_consumption[(stock_consumption.stock_category == "Over Stock")|(stock_consumption.stock_category =="Avaiable_Non_Moving_items")]
overstock_table = pd.merge(overstock_table,batch_details[["region_id","item_id","batch_id",'expiry_date']],on=['region_id',"item_id"],how='left')
overstock_table ['available_quantity'] = overstock_table['total_stock'] - overstock_table['average_consumption'] * 6
overstock_table= overstock_table.drop(columns=["total_stock",'average_consumption','covering_months','stock_category'])


# overstock_table.to_excel('overstock_table.xlsx')

oos_table = pd.read_excel('oos_table.xlsx')
overstock_table = pd.read_excel('overstock_table.xlsx')
overstock_table = overstock_table.drop('expiry_cost', axis = 1)
overstock_table = overstock_table.drop_duplicates()
reg_dist = pd.read_excel('region_distance.xlsx')

overstock_table['item_id'].value_counts()
oos_table = oos_table[oos_table['item_id'] == 'item_100373']
overstock_table = overstock_table[overstock_table['item_id'] == 'item_100373']

date_before = dt.datetime.today() + dt.timedelta(days = 60)
date_after = dt.datetime.today() + dt.timedelta(days = 120)
stock_transfer = oos_table.merge(overstock_table, how = 'outer', on = 'item_id')
stock_transfer = stock_transfer.rename(columns = {'region_id_x': 'source_region_id', 'region_id_y': 'dest_region_id'})
stock_transfer = stock_transfer[stock_transfer['expiry_date'] > date_before]
stock_transfer['expiry_cost'] = np.where(stock_transfer['expiry_date'] > date_after, 0,
                                         np.where(stock_transfer['required_quantity'] > stock_transfer['available_quantity'],
                                                  stock_transfer['available_quantity'] * stock_transfer['unit_price'],
                                                  stock_transfer['required_quantity'] * stock_transfer['unit_price']))
stock_transfer = stock_transfer.merge(reg_dist, how = 'left', on = ['source_region_id', 'dest_region_id'])


                                          