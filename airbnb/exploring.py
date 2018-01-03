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

# Global settings
warnings.filterwarnings('ignore')

csv_file = 'data/listings.csv'
listings = pd.DataFrame.from_csv(csv_file)

print(listings.shape)
y = listings['price']
del listings['price']
print(listings.shape)


bad_features = ['scrape_id', 'last_scraped', 'picture_url', 'host_picture_url',
                'host_id', 'neighbourhood', 'state', 'market', 'country',
                'weekly_price', 'monthly_price', 'calendar_last_scraped',
                'host_name', 'host_since', 'street', 'calendar_updated',
                'first_review', 'last_review']
listings.drop(bad_features, axis=1, inplace=True)
print(listings.shape)

# print(listings.head(n=3))

emptiness = []
missing_columns = []

def percent_empty(df):
    bools = df.isnull().tolist()
    percent_empty = float(bools.count(True)/len(bools))
    return percent_empty, bools.count(True)

for i in range(listings.shape[1]):
    p, n = percent_empty(listings.iloc[:, i])
    if n > 0:
        missing_columns.append(listings.columns.values[i])
    emptiness.append(round(p,2))

empty_dict = dict(zip(listings.columns.values.tolist(), emptiness))
empty = pd.DataFrame.from_dict(empty_dict, orient='index').sort_values(by=0)
# ax = empty.plot(kind='bar', color = BNB_RED, figsize=(16,15))
# ax.set_title('feature emptiness')
# ax.set_xlabel('predictor')
# ax.set_ylabel('percent empty/nan')
# ax.legend_.remove()
# plt.show()

listings.drop('square_feet', axis=1, inplace=True)
missing_columns.remove('square_feet')
print(listings.shape)

y = y.apply(lambda s: float(s[1:].replace(',', '')))
listings['extra_people'] = listings['extra_people'].apply(lambda s: float(s[1:].replace(',', '')))

to_float = ['latitude', 'longitude', 'accommodates',
            'bathrooms', 'bedrooms', 'beds', 'guests_included',
            'extra_people', 'minimum_nights', 'maximum_nights',
            'availability_30', 'availability_60', 'availability_90',
            'availability_365', 'number_of_reviews', 'review_scores_rating',
            'review_scores_accuracy', 'review_scores_cleanliness',
            'review_scores_checkin', 'review_scores_communication',
            'review_scores_location', 'review_scores_value', 'host_listing_count']

for i in to_float:
    listings[i] = listings[i].astype(float)

listings = listings[listings.bedrooms != 0]
print(listings.shape)
listings = listings[listings.beds != 0]
print(listings.shape)

listings = listings.join(y)
listings = listings[listings.price != 0]
print(listings.shape)

# print(listings.neighbourhood_cleansed.head(n=20))

nb_counts = Counter(listings.neighbourhood_cleansed)
# tdf = pd.DataFrame.from_dict(nb_counts, orient='index').sort_values(by=0)
# ax = tdf.plot(kind='bar', figsize=(50,10), color=BNB_BLUE, alpha=.85)
# ax.set_title('Neighborhoods by number of listings')
# ax.set_xlabel('Neighborhood')
# ax.set_ylabel('# of listings')
# plt.show()
# print('number of neighborhoods: ', len(nb_counts))

del_nb = []

for i in nb_counts.keys():
    if nb_counts[i] < 100:
        del_nb.append(i)
        listings = listings[listings.neighbourhood_cleansed != i]

print(listings.shape)
print(len(nb_counts))

for i in del_nb:
    del nb_counts[i]
print(len(nb_counts))

tdf = pd.DataFrame.from_dict(nb_counts, orient='index').sort_values(by=0)
# ax = tdf.plot(kind='bar', figsize=(50,10), color=BNB_BLUE)
# ax.set_title('neighborhoods by number of listings')
# ax.set_xlabel('neighbor')
# ax.set_ylabel('of listings')
# plt.show()
print('number of neighborhoods: ', len(nb_counts))

def encode_categorical(array):
    if not array.dtype == np.dtype('float64'):
        return preprocessing.LabelEncoder().fit_transform(array.astype(str))
    else:
        return array

tmp_listings = listings.copy()
print(tmp_listings.shape)
tmp_listings = tmp_listings.dropna(axis=0)
print(tmp_listings.shape)
tmp_listings = tmp_listings.apply(encode_categorical)
print(tmp_listings.shape)

corr_matrix = np.corrcoef(tmp_listings.T)
corr_df = pd.DataFrame(data=corr_matrix, columns=tmp_listings.columns, index=tmp_listings.columns)

# plt.figure(figsize=(7, 7))
# plt.pcolor(corr_matrix, cmap='RdBu')
# plt.xlabel('predictor index')
# plt.ylabel('predictor index')
# plt.colorbar()
# plt.show()

# Remove features
listings.drop(['zipcode', 'city', 'availability_30',
               'availability_60', 'availability_90'], axis=1, inplace=True)

missing_columns.remove('zipcode')

print(listings.shape)
listings.drop('name', axis=1, inplace=True)
print(listings.shape)


# KNN_predict
#
# Function to predict missing data using KNN
# Input: df_missing (dataframe)
#        df_filled (dataframe)
#        column_name (string)
#        k (integer)
# Output: df_predict (dataframe of predicted values)
def KNN_predict(df_missing, df_temp, df_filled, column_name, k):
    # Training and test set
    y = df_filled[column_name]
    X_filled = df_filled.drop(column_name, axis=1)
    X_missing = df_temp.drop(column_name, axis=1)

    # Predict with KNN
    if df_filled[column_name].dtype == np.dtype('float64'):
        knn = KNN(n_neighbors=k, n_jobs=-1)
    else:
        knn = KNNc(n_neighbors=k, n_jobs=-1)
    knn.fit(X_filled, y)
    df_predict = df_missing.copy()
    df_predict[column_name] = knn.predict(X_missing)

    return df_predict


# KNN_fill
#
# Function to predict missing data for all columns using KNN
# and temporary median displacement for other missing values in
# other columns
# Input: df (dataframe)
#        missing_columns (list of strings)
# Output: df_final (filled dataframe)
def KNN_fill(df, missing_columns):
    # Separate the rows with missing data information
    df_missing = df[pd.isnull(df).any(axis=1)]
    df_filled = df[~pd.isnull(df).any(axis=1)]
    test_ind = int(0.3 * len(df_filled.index))

    # Find an appropriate k for KNN
    best_ks = []

    # Go through all columns with missing data, skip property type
    for column in missing_columns:
        # Impute with median temporarily (only quantitative missing values in our
        # model at this point so no need for mode)
        temp_df = df_missing.copy()
        for c in missing_columns:
            # Do not impute selected column
            if c != column:
                temp_df[c].fillna((temp_df[c].median()), inplace=True)

        # Create 10 simulated test and train set from df_filled
        for k in range(10):
            RSS = []
            scores = []

            # For each simulated test and train set, try k-values: 1 to 15 (counting by 2)
            for k in range(1, 15, 2):
                df_shuffled = df_filled.sample(frac=1)
                df_test = df_shuffled.iloc[:test_ind, :]
                df_train = df_shuffled.iloc[test_ind:, :]

                # Fill rows with missing information
                df_pred = KNN_predict(df_test, df_test, df_train, column, k)

                # Compute score of filled in data
                if df[column].dtype == np.dtype('float64'):
                    RSS.append(((df_pred[column] - df_test[column]) ** 2).mean())
                else:
                    scores.append(Metrics.accuracy_score(df_test[column], df_pred[column], normalize=True))

            # Record the k that yields best score
            if df[column].dtype == np.dtype('float64'):
                best_ks.append(np.argmin(RSS) + 1)
            else:
                best_ks.append(np.argmax(scores) + 1)

        # Take the mean of the best k over 100 simulations
        best_k = int(np.mean(best_ks))

        # Fill rows with missing information, using the optimal k
        df_missing = KNN_predict(df_missing, temp_df, df_filled, column, best_k)

    # Concatenate rows with no missing info and the row we filled in
    df_final = pd.concat([df_filled, df_missing])
    df_final = df_final.sort_index()

    return df_final

listings = listings.apply(encode_categorical)
del listings['price']
print(listings.shape)

listings_clean = KNN_fill(listings, missing_columns)

listings = listings.join(y)
listings_clean = listings_clean.join(y)

for c in missing_columns:
    listings[c] = listings_clean[c].round()

listings_clean.to_csv('data/listings_clean2.csv')
listings_clean = listings_clean.iloc[:100, :]
listings_clean.to_csv('data/listings_cut.csv')