import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

csv_file = 'data/air_store_info.csv'

df = pd.read_csv(csv_file, delimiter=',')

print('====> columns: ')
print(df.columns.values)
print('====>air_store_info list size: ')
print(df.shape)
print('====> list as follows: ')
print(df.head(n=5))

grouped_by_id = df.groupby(['air_store_id'])
print('====>id count: ')
print(len(grouped_by_id.groups))

grouped_by_genre = df.groupby(['air_genre_name'])
print('====> genre count: ')
print(len(grouped_by_genre.groups))
print('====> genre: ')
print(grouped_by_genre.groups.keys())
df.set_index('air_genre_name')

grouped_by_area = df.groupby(['air_area_name'])
print('====> air count: ')
print(len(grouped_by_area))
print('====> air area: ')
print(grouped_by_area.groups.keys())

grouped_by_lat_long = df.groupby(['latitude', 'longitude'])
print('====> latitude&longitude count: ')
print(len(grouped_by_lat_long.groups))
