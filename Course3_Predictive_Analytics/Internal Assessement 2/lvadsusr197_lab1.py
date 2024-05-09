# -*- coding: utf-8 -*-
"""LVADSUSR197_lab1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ETzuzMDuUdjj3u8wAeJHAvDcKheP4tvq
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('/content/winequality-red.csv')
df

"""# Handling Missing values and Outliers"""

df.info()

df.shape

df.isnull().sum()

df.dropna(inplace=True)

df.shape

df.isnull().sum()

def outliers_iqr(data):
    q1 = np.percentile(data, 25)
    q3 = np.percentile(data, 75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    outliers = [x for x in data if x < lower_bound or x > upper_bound]
    return outliers
numerical_columns = df.select_dtypes(include=[np.number])
outliers_dict = {}
for col in numerical_columns.columns:
    outliers_dict[col] = outliers_iqr(df[col])
for col, outliers in outliers_dict.items():
    print("Outliers in column '{}': {}".format(col, outliers))

df.duplicated().sum()

df = df.drop_duplicates()

df.duplicated().sum()

df.shape

df.head()

from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()

X = df.drop(['free sulfur dioxide','quality'],axis = 1)
y = df['quality']

X_scaled = scaler.fit_transform(X)
print(pd.DataFrame(X_scaled))

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X_scaled,y,test_size=0.2,random_state=42)

#KNN
#  for number of neighbors (k) = 2

from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score


model = KNeighborsClassifier(n_neighbors=2)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

#performance
accuracy = accuracy_score(y_test, y_pred)
print("KNN Accuracy:", accuracy)

report = classification_report(y_test, y_pred)
print("classification Report Accuracy:", report)

#KNN
#  for number of neighbors (k) = 3

from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report

model = KNeighborsClassifier(n_neighbors=3)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

#performance
accuracy = accuracy_score(y_test, y_pred)
print("KNN Accuracy:", accuracy)

report = classification_report(y_test, y_pred)
print("classification Report Accuracy:", report)