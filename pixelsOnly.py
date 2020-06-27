import pickle
import pandas as pd
import os


# pickxtrain = open('X_train.pickle', 'rb')
# pickytrain = open('y_train.pickle', 'rb')
# pickxtest = open('X_test.pickle', 'rb')
# pickytest = open('y_test.pickle', 'rb')
#
# X_train = pickle.load(pickxtrain)
# y_train = pickle.load(pickytrain)
# X_test = pickle.load(pickxtest)
# y_test = pickle.load(pickytest)

# X_Train_pixelDF = pd.DataFrame(columns=['S2T0', 'S3T0', 'S3T1', 'S3T2', 'S3T3', 'S3T4', 'S3T5'])
# y_Train_pixelDF = pd.DataFrame(columns=['S2VAL'])
# X_Test_pixelDF = pd.DataFrame(columns=['S2T0', 'S3T0', 'S3T1', 'S3T2', 'S3T3', 'S3T4', 'S3T5'])
# y_Test_pixelDF = pd.DataFrame(columns=['S2VAL'])

# for j in range(20):#X_train.shape[0]):
#     #print(X_train.iloc[j][0])
#     for i in range(len(X_train.iloc[j][0])):
#         try:
#             tmp_data = {'S2T0': X_train.iloc[j][0][i],
#                         'S3T0': X_train.iloc[j][1][i],
#                         'S3T1': X_train.iloc[j][2][i],
#                         'S3T2': X_train.iloc[j][3][i],
#                         'S3T3': X_train.iloc[j][4][i],
#                         'S3T4': X_train.iloc[j][5][i],
#                         'S3T5': X_train.iloc[j][6][i],
#                         }
#         except:
#             print("An error occured on train, index j: ", j, " and i: ", i)
#         X_Train_pixelDF = X_Train_pixelDF.append(tmp_data, ignore_index=True)
#     for i in range(len(y_train.iloc[j][0])):
#         tmp_data = {'S2VAL': y_train.iloc[j][0][i],
#                     }
#         y_Train_pixelDF = y_Train_pixelDF.append(tmp_data, ignore_index=True)
#
# for j in range(20):#X_test.shape[0]):
#     #print(X_train.iloc[j][0])
#     for i in range(len(X_test.iloc[j][0])):
#         try:
#             tmp_data = {'S2T0': X_test.iloc[j][0][i],
#                         'S3T0': X_test.iloc[j][1][i],
#                         'S3T1': X_test.iloc[j][2][i],
#                         'S3T2': X_test.iloc[j][3][i],
#                         'S3T3': X_test.iloc[j][4][i],
#                         'S3T4': X_test.iloc[j][5][i],
#                         'S3T5': X_test.iloc[j][6][i],
#                         }
#         except:
#             print("An error occured on test, index j: ", j, " and i: ", i)
#         X_Test_pixelDF = X_Test_pixelDF.append(tmp_data, ignore_index=True)
#     for i in range(len(y_test.iloc[j][0])):
#         tmp_data = {'S2VAL': y_test.iloc[j][0][i],
#                     }
#         y_Test_pixelDF = y_Test_pixelDF.append(tmp_data, ignore_index=True)
#
# print(X_Train_pixelDF)
# print(y_Train_pixelDF)
# print(X_Test_pixelDF)
# print(y_Test_pixelDF)

pickx = open('X.pickle', 'rb')
picky = open('y.pickle', 'rb')
X = pickle.load(pickx)
y = pickle.load(picky)

X_pixelDF = pd.DataFrame(columns=['S2T0', 'S3T0', 'S3T1', 'S3T2', 'S3T3', 'S3T4', 'S3T5'])
y_pixelDF = pd.DataFrame(columns=['S2VAL'])

for j in range(len(X.index)):
    try:
        for i in range(len(X.iloc[j][0])):
            try:
                tmp_data = {'S2T0': X.iloc[j][0][i],
                            'S3T0': X.iloc[j][1][i],
                            'S3T1': X.iloc[j][2][i],
                            'S3T2': X.iloc[j][3][i],
                            'S3T3': X.iloc[j][4][i],
                            'S3T4': X.iloc[j][5][i],
                            'S3T5': X.iloc[j][6][i],
                            }
                tmp_data_y = {'S2VAL': y.iloc[j][0][i]
                              }
            except:
                print("An error occured on train, index j: ", j, " and i: ", i)
            X_pixelDF = X_pixelDF.append(tmp_data, ignore_index=True)
            y_pixelDF = y_pixelDF.append(tmp_data_y, ignore_index=True)
    except:
        print("An error occured on train, outer loop, on j: ", j, " and i: ", i)

print(X_pixelDF)
print(y_pixelDF)

cwd = 'C:/NDVI_DATA/pickle_pixel'
os.chdir(cwd)

pickx_pixle = open("X_pixle.pickle", 'wb')
picky_pixle = open("y_pixle.pickle", 'wb')


pickle.dump(X_pixelDF, pickx_pixle)
pickle.dump(y_pixelDF, picky_pixle)


pickx_pixle.close()
picky_pixle.close()