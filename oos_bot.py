import pandas as pd
import numpy as np
import os


path = r'D:\Ascend\Analytics_Use_Cases\oos_bot'
os.chdir(path)

batch_details = pd.read_excel('batch_details.xlsx')
onhand_report = pd.read_excel('onhand_report.xlsx')



##########################################################

from datetime import datetime, timedelta

# define the batch data structure
class Batch:
    def __init__(self, quantity, expiry_date):
        self.quantity = quantity
        self.expiry_date = expiry_date

# define a function to allocate batches
def allocate_batches(total_quantity, available_quantity, expiry_dates):
    batches = []
    for quantity, expiry_date in zip(total_quantity, expiry_dates):
        batches.append(Batch(quantity, expiry_date))

    # sort the batches by expiry date
    batches.sort(key=lambda batch: batch.expiry_date)

    # allocate batches until all available quantity is used
    allocation = []
    for batch in batches:
        if available_quantity > 0:
            if batch.quantity <= available_quantity:
                allocation.append(batch.quantity)
                available_quantity -= batch.quantity
            else:
                allocation.append(available_quantity)
                available_quantity = 0
        else:
            allocation.append(0)

    return allocation

# example usage
total_quantity = [100, 200, 300]
expiry_dates = [datetime(2023, 6, 1), datetime(2023, 7, 1), datetime(2023, 8, 1)]
available_quantity = 400

allocation = allocate_batches(total_quantity, available_quantity, expiry_dates)
print(allocation)

##########################################################
