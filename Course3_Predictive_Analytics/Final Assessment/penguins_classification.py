# -*- coding: utf-8 -*-
"""penguins classification.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1vYi3m-OZmqQisJdXIZ6b-jqbAoRvVGAZ
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler,StandardScaler,LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression,LogisticRegression
from sklearn.metrics import accuracy_score,r2_score,precision_score,recall_score,classification_report

"""# load data"""

df = pd.read_csv('/content/penguins_classification.csv')
df

"""# data pre processing"""

df.info()

df.isnull().sum()

df['bill_depth_mm']= df['bill_depth_mm'].fillna(df['bill_depth_mm'].mean())

df.isnull().sum()

df.duplicated().sum()

def outliers_iqr(df):
    q1 = np.percentile(df, 25)
    q3 = np.percentile(df, 75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    outliers = [x for x in df if x < lower_bound or x > upper_bound]
    return outliers
numerical_columns = df.select_dtypes(include=[np.number])
outliers_dict = {}
for col in numerical_columns.columns:
    outliers_dict[col] = outliers_iqr(df[col])
for col, outliers in outliers_dict.items():
    print("Outliers in column '{}': {}".format(col, outliers))

"""#EDA"""

df.shape

#correlation blw nums

numerical_columns = df.select_dtypes(include=['float64', 'int64']).columns
correlation_matrix = df[numerical_columns].corr()
print(correlation_matrix)

#heat map
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm')
plt.title('Heatmap of Correlation Matrix')
plt.show()

#scatter
numerical_columns = df.select_dtypes(include=['float64', 'int64']).columns
for i in range(len(numerical_columns)):
    for j in range(i + 1, len(numerical_columns)):
        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=df, x=numerical_columns[i], y=numerical_columns[j])
        plt.title(f'Scatter Plot between {numerical_columns[i]} and {numerical_columns[j]}')
        plt.show()

"""# model training and testing"""

df.head()

# for i in df.select_dtypes(include='object'):
#   df[i]=df[i].fillna(df[i].mode()[0])
# for i in df.select_dtypes(include=['int64','float64']):
#   df[i]=df[i].fillna(df[i].mean())

df.columns

encoder = LabelEncoder()
cols = ['species', 'island', 'bill_length_mm', 'bill_depth_mm',
       'flipper_length_mm', 'body_mass_g', 'year']
for col in cols:
  df[col]= encoder.fit_transform(df[col])

df.head()

X = df.drop(['species','island','body_mass_g','year'],axis = 1)
y = df['species']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LogisticRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
y_pred

"""# metrics"""

from sklearn.metrics import classification_report,confusion_matrix



accuracy = accuracy_score(y_test, y_pred)
print("Accuracy: ", accuracy,"\n")

# For more detailed evaluation
report= classification_report(y_test, y_pred)
print("Classification R\n: ",report)

conf_matrix = confusion_matrix(y_test,y_pred)
print("Cnf: \n",conf_matrix)