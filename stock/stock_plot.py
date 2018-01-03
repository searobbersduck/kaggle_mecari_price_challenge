import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

csv_file = 'x.csv'
df = pd.DataFrame.from_csv(csv_file)
# df['日期'] = df['日期'].apply(lambda s: datetime.strptime(s.strip(), '%Y-%m-%d')).astype('datetime64[ns]').astype(int)
df = df.sort_values(by=['日期'])
df = df.reset_index(drop=True)
# df['交易金额(元)']
df['交易量(股)'] = df['交易量(股)'].apply(lambda s: s//2e5)

df[['收盘价','开盘价', '交易量(股)']][::5].plot(figsize=(16,5))
plt.show()

df.to_csv('y.csv')