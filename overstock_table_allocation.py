import pandas as pd
import numpy as np
import os
from datetime import datetime

path = r'C:\Users\YasinHammad(Ascend)\Desktop\OOS-Analysis-Bot'
os.chdir(path)

batch_details = pd.read_excel('batch_details_processed.xlsx').dropna()
stock_consumption = pd.read_excel('stock_consumption.xlsx')

batches_df = batch_details.copy()

batches_dfg = batches_df.groupby(['item_id', 'region_id'])['available_quantity'].sum().reset_index()
inventory_df = stock_consumption.merge(batches_dfg, on = ['item_id', 'region_id'], how = 'right')
inventory_df['total_stock'] = inventory_df['overstock']
inventory_df['used_quantity'] = inventory_df['available_quantity'] - inventory_df['total_stock']
inventory_df['used_quantity'] = np.where(inventory_df['used_quantity'] < 0, 0, inventory_df['used_quantity'])

# group batches by item ID and region ID
batches_grouped = batches_df.groupby(['item_id', 'region_id'])

i = 1
# allocate available quantity to batches based on expiry date
for group_name, group_df in batches_grouped:
    # get the available quantity for the item and region
    used_quantity = inventory_df.loc[(inventory_df['item_id'] == group_name[0]) & (inventory_df['region_id'] == group_name[1]), 'used_quantity'].item()
    # sort batches by expiry date in ascending order
    group_df = group_df.sort_values(by = 'expiry_date', key = lambda x: pd.to_datetime(x, format='%Y-%m-%d'))
        
    # allocate available quantity to batches based on expiry date
    group_df['dispensed_quantity'] = 0
    for index, row in group_df.iterrows():
        if used_quantity >= row['available_quantity']:
            group_df.at[index, 'dispensed_quantity'] = row['available_quantity']
            used_quantity -= row['available_quantity']
        else:
            group_df.at[index, 'dispensed_quantity'] = used_quantity
            used_quantity = 0
    # update the allocated quantity for the group in the batches dataframe
    group_df = group_df.sort_index()
    batches_df.loc[(batches_df['item_id'] == group_name[0]) & (batches_df['region_id'] == group_name[1]), 'dispensed_quantity'] = group_df['dispensed_quantity'].values
    print(i)
    i += 1
batches_df['overstock_quantity'] = batches_df['available_quantity'] - batches_df['dispensed_quantity']
batches_df = batches_df.drop('dispensed_quantity', axis = 1)
# print the result
# for index, row in batches_df.iterrows():
#     print(f"Batch {row['batch_id']}: {row['available_quantity']} remaining")
batches_df.to_excel('batch_details_processed_ovs.xlsx', index = False)