import sys
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter
from sklearn import preprocessing
from sklearn.neighbors import KNeighborsRegressor as KNN
from sklearn.neighbors import KNeighborsClassifier as KNNc
import sklearn.metrics as Metrics
import warnings

# Global variables
BNB_BLUE = '#007A87'
BNB_RED = '#FF5A5F'
BNB_DARK_GRAY = '#565A5C'
BNB_LIGHT_GRAY = '#CED1CC'

warnings.filterwarnings('ignore')

csv_file = './data/listings.csv'
listings = pd.read_csv(csv_file, delimiter=',')
y = listings.price
del listings['price']

# bad_features = ['scrape_id', 'last_scraped', 'picture_url', 'host_picture_url',
#                 'host_id', 'neighbourhood', 'state', 'market', 'country',
#                 'weekly_price', 'monthly_price', 'calendar_last_scraped',
#                 'host_name', 'host_since', 'street', 'calendar_updated',
#                 'first_review', 'last_review']

'''
remove column value 'street', it will be used next.
'''
bad_features = ['scrape_id', 'last_scraped', 'picture_url', 'host_picture_url',
                'host_id', 'neighbourhood', 'state', 'market', 'country',
                'weekly_price', 'monthly_price', 'calendar_last_scraped',
                'host_name', 'host_since', 'calendar_updated',
                'first_review', 'last_review']

listings.drop(bad_features, axis=1, inplace=True)
entries = listings.shape[0]
features = listings.shape[1]-1
print('number of entries: {}'.format(entries))
print('number of features: ', features)
# print(listings.head(n=3))

def percent_empty(df):
    bools = df.isnull().tolist()
    percent_empty = float(bools.count(True))/float(len(bools))
    return percent_empty, float(bools.count(True))

emptiness = []
missing_columns = []

for i in range(listings.shape[1]):
    p, n = percent_empty(listings.iloc[:, i])
    if n > 0:
        missing_columns.append(listings.columns.values[i])
    emptiness.append(round((p), 2))

empty_dict = dict(zip(listings.columns.values.tolist(), emptiness))
empty = pd.DataFrame.from_dict(empty_dict, orient='index').sort_values(by=0)
ax = empty.plot(kind='bar', color=BNB_BLUE, figsize=(16,6))
ax.set_xlabel('Predictor')
ax.set_ylabel('Percent Empty/NaN')
ax.set_title('Feature Emptiness')
ax.legend_.remove()
plt.show()

listings.drop('square_feet', axis=1, inplace=True)
missing_columns.remove('square_feet')
features = listings.shape[1]

y = y.apply(lambda s: float(s[1:].replace(',','')))
listings['extra_people'] = listings['extra_people'].apply(
    lambda s: float(s[1:].replace(',', ''))
)
# List of columns to be converted to floating point
to_float = ['id', 'latitude', 'longitude', 'accommodates',
            'bathrooms', 'bedrooms', 'beds', 'guests_included',
            'extra_people', 'minimum_nights', 'maximum_nights',
            'availability_30', 'availability_60', 'availability_90',
            'availability_365', 'number_of_reviews', 'review_scores_rating',
            'review_scores_accuracy', 'review_scores_cleanliness',
            'review_scores_checkin', 'review_scores_communication',
            'review_scores_location', 'review_scores_value', 'host_listing_count']
for feature_name in to_float:
    listings[feature_name] = listings[feature_name].astype(float)

listings = listings[listings.bedrooms != 0]
listings = listings[listings.beds != 0]
listings = listings[listings.bathrooms != 0]

listings = listings.join(y)
listings = listings[listings.price != 0]

print('number of entries removed: ', entries-listings.shape[0])
entries = listings.shape[0]
print('number of entries:', entries)

nb_counter = Counter(listings.neighbourhood_cleansed)
tdf = pd.DataFrame.from_dict(nb_counter, orient='index').sort_values(by=0)
tdf = tdf.iloc[-20:, :]
# ax = tdf.plot(kind='bar', figsize= (50,10), color=BNB_BLUE)
# ax.set_title('Neighborhood by number of listings')
# ax.set_xlabel('Neighborhood')
# ax.set_ylabel('# of Listings')
# plt.show()
print('number of neighborhoods: ', len(nb_counter))

nb_del = []
for i in nb_counter.keys():
    if nb_counter[i] < 100:
        nb_del.append(i)
        listings = listings[listings.neighbourhood_cleansed != i]

for i in nb_del:
    del nb_counter[i]

tdf = pd.DataFrame.from_dict(nb_counter, orient='index').sort_values(by=0)
# ax = tdf.plot(kind='bar', figsize=(22,4), color=BNB_BLUE)
# ax.set_title('Neighborhoods by house # (Top 48)')
# ax.set_xlabel('Neighborhood')
# ax.set_ylabel('# of listings')
# plt.show()
print('Number of entries removed: ', entries-listings.shape[0])
entries = listings.shape[0]

def encode_categorical(array):
    print(array.name)
    if not array.dtype == np.dtype('float64'):
        return preprocessing.LabelEncoder().fit_transform(array.astype(str))
    else:
        return array

tmp_listings = listings.copy()
tmp_listings = tmp_listings.dropna(axis=0)
tmp_listings = tmp_listings.apply(encode_categorical)

corr_matrix = np.corrcoef(tmp_listings.T)
corr_df = pd.DataFrame(data=corr_matrix, columns=tmp_listings.columns, index=tmp_listings.columns)

# plt.figure(figsize=(7,7))
# plt.pcolor(corr_matrix, cmap='RdBu')
# plt.xlabel('Predictor Index')
# plt.ylabel('Predictor Index')
# plt.title('Heatmap of Correlation Matrix')
# plt.colorbar()
# plt.show()

listings.drop(['zipcode', 'city', 'availability_30',
               'availability_60', 'availability_90'], axis=1, inplace=True)
missing_columns.remove('zipcode')

print(tmp_listings.columns.values)

listings.drop('name', axis=1, inplace=True)

def KNN_predict(df_missing, df_temp, df_filled, column_name, k):
    y = df_filled[column_name]
    X_filled = df_filled.drop(column_name, axis=1)
    X_missing = df_temp.drop(column_name, axis=1)
    if df_filled[column_name].dtype == np.dtype('float64'):
        knn = KNN(n_neighbors=k, n_jobs=-1)
    else:
        knn = KNNc(n_neighbors=k, n_jobs=-1)
    knn.fit(X_filled, y)
    df_predict = df_missing.copy()
    df_predict[column_name] = knn.predict(X_missing)
    return df_predict

def KNN_fill(df, missing_columns):
    df_missing = df[pd.isnull(df).any(axis=1)]
    df_missing = df[pd.isnull(df).any(axis=1)]
    df_filled = df[~pd.isnull(df).any(axis=1)]
    test_ind = int(0.3*len(df_filled.index))
    best_ks = []
    for column in missing_columns:
        temp_df = df_missing.copy()
        for c in missing_columns:
            if c != column:
                temp_df[c].fillna((temp_df[c].median()), inplace=True)
        for k in range(10):
            RSS = []
            scores = []
            for k in range(1, 15, 2):
                df_shuffle = df_filled.sample(frac=1)
                df_test = df_shuffle.iloc[:test_ind, :]
                df_train = df_shuffle.iloc[test_ind:,:]
                df_pred = KNN_predict(df_test, df_test, df_train, column, k)
                if df[column].dtype == np.dtype('float64'):
                    RSS.append(((df_pred[column]-df_test[column])**2).mean())
                else:
                    scores.append(Metrics.accuracy_score(df_test[column], df_pred[column], normalize=True))
            if df[column].dtype == np.dtype('float64'):
                best_ks.append(np.argmin(RSS)+1)
            else:
                best_ks.append(np.argmax(scores)+1)
        best_k = int(np.mean(best_ks))
        df_missing = KNN_predict(df_missing, temp_df, df_filled, column, best_k)
    df_final = pd.concat([df_filled, df_missing])
    df_final = df_final.sort_index()

    return df_final

listings = listings.apply(encode_categorical)

del listings['price']
listings_clean = KNN_fill(listings, missing_columns)
listings = listings.join(y)
listings_clean = listings_clean.join(y)

for c in missing_columns:
    listings_clean[c] = listings_clean.round()

listings_clean.to_csv(path_or_buf='./data/listings_clean1.csv')



'''

问题解决方案：

def encode_categorical(array):
    print(array.name)
    if not array.dtype == np.dtype('float64'):
        return preprocessing.LabelEncoder().fit_transform(array.astype(str))
    else:
        return array

preprocessing.LabelEncoder().fit_transform(array.astype(str))，其中array.astype(str)如果不写，会带来如下bug:

LabelEncoder: TypeError: '>' not supported between instances of 'float' and 'str'

解决方案：

https://stackoverflow.com/questions/46406720/labelencoder-typeerror-not-supported-between-instances-of-float-and-str

'''