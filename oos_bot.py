import pandas as pd
import numpy as np
import os


path = r'D:\Ascend\Analytics_Use_Cases\oos_bot'
os.chdir(path)

batch_details = pd.read_excel('batch_details.xlsx')
onhand_report = pd.read_excel('onhand_report.xlsx')
