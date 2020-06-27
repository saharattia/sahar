import pandas as pd
import numpy as np
import datetime
import os
from os import listdir
from sklearn.model_selection import train_test_split
import pickle


def make_master_df(dir, num_fields):
    master_df = pd.DataFrame(columns=['S2T0', 'S3T0', 'S3T1', 'S3T2', 'S3T3', 'S3T4', 'S3T5', 'S2VAL'])
    for i in range(1, num_fields):
        print("Loading field number: ", i,"\n")
        cwd = dir+'f'+str(i)
        os.chdir(cwd)
        files = os.listdir(cwd)  # Get all the files in that directory
        print("Files in %r: %s" % (cwd, files))
        filepaths = [f for f in listdir(cwd) if f.endswith('.csv')]
        lsorted = sorted(filepaths, key=lambda x: int(os.path.splitext(x)[0]))
        df = pd.concat(map(pd.read_csv, lsorted))

        df_v = pd.DataFrame(columns=['S2T0', 'S3T0', 'S3T1', 'S3T2', 'S3T3', 'S3T4', 'S3T5', 'S2VAL'])
        num_columns = len(df_v.columns)
        row = 0

        while row < len(df)-8:
            temp_data = {'S2T0': [df.iloc[row, 3].replace('[', '').replace(']', '')],
                         'S3T0': [df.iloc[row+1, 3].replace('[', '').replace(']', '')],
                         'S3T1': [df.iloc[row+2, 3].replace('[', '').replace(']', '')],
                         'S3T2': [df.iloc[row+3, 3].replace('[', '').replace(']', '')],
                         'S3T3': [df.iloc[row+4, 3].replace('[', '').replace(']', '')],
                         'S3T4': [df.iloc[row+5, 3].replace('[', '').replace(']', '')],
                         'S3T5': [df.iloc[row+6, 3].replace('[', '').replace(']', '')],
                         'S2VAL': [df.iloc[row+7, 3].replace('[', '').replace(']', '')]}
            temp_df = pd.DataFrame(temp_data)
            row += 8
            df_v = df_v.append(temp_df, ignore_index=True)

        df_v = df_v.applymap(lambda x: x.split(", ") if x!="" else [])
        df_v = df_v.applymap(lambda x: [float(item) for item in x])
        df_v = df_v.applymap(lambda x: np.asarray(x))
        print("Field ",i," loading complete. The data: \n", df_v)

        # In case we wish to validate the first object in every dataframe
        # print(len(df_v.loc[0, 'S2T0']))
        # print(len(df_v.loc[0, 'S3T0']))
        # print(len(df_v.loc[0, 'S3T1']))
        # print(len(df_v.loc[0, 'S3T2']))
        # print(len(df_v.loc[0, 'S3T3']))
        # print(len(df_v.loc[0, 'S3T4']))
        # print(len(df_v.loc[0, 'S3T5']))
        # print(len(df_v.loc[0, 'S2VAL']))

        df_v.to_csv('C:/NDVI_DATA/fields/field'+str(i)+'.csv', index=False)
        master_df = master_df.append(df_v, ignore_index=True)

    # master_df.to_csv('C:/NDVI_DATA/all/all.csv', index=False)
    master_df = master_df.applymap(lambda y: np.nan if len(y) == 0 else y)
    return master_df


def fill_na(origin_df):
    print("NA filling stage begin. \n")
    print("Number of Nulls: \n", origin_df.isna().sum())

    df_filled = origin_df.fillna(method='pad', limit=1)
    df_filled = df_filled.fillna(method='bfill', limit=1)
    df_filled = df_filled.fillna(method='pad', limit=1)

    print("Number of Nulls midway: \n", df_filled.isna().sum())

    df_filled = df_filled.fillna(method='bfill', limit=1)
    df_filled = df_filled.fillna(method='pad', limit=1)

    print("Number of Nulls end: \n", df_filled.isna().sum())
    return df_filled


def get_xy(df):
    x_origin = df.loc[:, df.columns != 'S2VAL']
    y_origin = df.loc[:, df.columns == 'S2VAL']
    return x_origin, y_origin


def drop_nas(df):
    print("Before dropna: ", df.shape)
    df = df.dropna()
    print("After dropna: ", df.shape)
    return df


def send_pickle_XY(pickle_dir, df_X, df_Y):
    os.chdir(pickle_dir)

    pickx = open("X.pickle", 'wb')
    picky = open("y.pickle", 'wb')

    pickle.dump(df_X, pickx)
    pickle.dump(df_Y, picky)

    pickx.close()
    picky.close()


field_dir = 'C:/Users/user/PycharmProjects/NDVI/data/'
number_of_fields = 5

all_fields_df = make_master_df(field_dir, number_of_fields)

# all_fields_df = all_fields_df.fillna()
all_fields_df = drop_nas(all_fields_df)

x_df, y_df = get_xy(all_fields_df)

p_dir = 'C:/Users/user/PycharmProjects/NDVI/'

send_pickle_XY(p_dir, x_df, y_df)
