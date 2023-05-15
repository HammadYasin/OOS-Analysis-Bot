import pandas as pd
import os

path = r'D:\Ascend\Analytics_Use_Cases\OOS-Analysis-Bot'
os.chdir(path)

batch_details = pd.read_excel('batch_details.xlsx').dropna()
onhand_report = pd.read_excel('onhand_report.xlsx')


# define the batch data structure
class Batch:
    def __init__(self, quantity, expiry_date, region_id, item_id):
        self.quantity = quantity
        self.expiry_date = expiry_date
        self.region_id = region_id
        self.item_id = item_id


batches = []
quantity = list(batch_details['quantity'])
expiry_date = list(batch_details['expiry_date'])
region_id = list(batch_details['region_id'])
item_id = list(batch_details['item_id'])
for quantity, expiry_date, region_id, item_id in zip(quantity, expiry_date, region_id, item_id):
    batches.append(Batch(quantity, expiry_date, region_id, item_id))


# create batches using apply() method
# batches = batch_details.apply(lambda x: Batch(x['quantity'], x['expiry_date'], x['region_id'], x['item_id']), axis = 1).tolist()

# create batches using list comprehension
# batches = [Batch(*x) for x in batch_details[['quantity', 'expiry_date', 'region_id', 'item_id']].to_numpy()]

# sort the batches by expiry date
batches.sort(key = lambda batch: batch.expiry_date)


onhand_report['total_stock'] = onhand_report['main_store_stock'] + onhand_report['sub_store_stock']
available_quantity = onhand_report.groupby(['region_id', 'item_id'])['total_stock'].sum()
# available_quantity_dict =  available_quantity.to_dict()

# loop over batches and allocate as much as possible
allocation = []
i = 1
for batch in batches:
    for x in available_quantity.index:
        if  (int(batch.region_id) == x[0] and batch.item_id == x[1]):
            if available_quantity[x] > 0:
                if batch.quantity <= available_quantity[x]:
                    allocation.append(batch.quantity)
                    available_quantity[x] -= batch.quantity
                else:
                    allocation.append(available_quantity[x])
                    available_quantity[x] = 0
            else:
                allocation.append(0)
    print(i)
    i += 1

# convert the allocation list to a Pandas Series
allocation = pd.Series(allocation)