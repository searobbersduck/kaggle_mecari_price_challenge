import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

csv_file = 'date_info.csv'

df = pd.read_csv(csv_file, delimiter=',')

print('date_info shape: ')
print(df.shape)
print('====> columns values: ')
print(df.columns.values)
print(df.head(n=5))

