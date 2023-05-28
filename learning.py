# -*- coding: utf-8 -*-
"""Tugas Pemrograman 3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1UWGFlsd2DmhZ7ULE5lyyAWAkjOXzK7lV
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from collections import Counter
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report

df = pd.read_excel('traintest.xlsx')
df = df.drop('id', axis=1)

df.head()

print(df['y'].value_counts())
sns.catplot(x='y', data=df, kind='count')
plt.show()

x_data = df.drop("y", axis=1).to_numpy()
y_data = df["y"].to_numpy()

from imblearn.over_sampling import SMOTE

x_data, y_data = SMOTE().fit_resample(x_data, y_data)

df_new = pd.DataFrame()
df_new['y'] = y_data

print(df_new['y'].value_counts())
sns.catplot(x='y', data=df_new, kind='count')
plt.show()

x_data

y_data

x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size=0.2)

"""## **Membangun Model**"""

class KNN:
    def __init__(self, k=5):
        self.K = k

    def train(self, X, y):  # X adalah data setiap kolom, y adalah label
        self.X_train = X
        self.y_train = y

    def predict(self, X):  # X berupa matriks
        y_prediksi = []
        for i in range(len(X)):
            y_prediksi.append(self._prediksi(X[i]))
            
        return np.array(y_prediksi)

    def _prediksi(self, x):  # x adalah item

        #1. hitung jarak ke semua data training
        jarak_titik = [self.jarak(x, x_train) for x_train in self.X_train]

        #2. urutkan berdasarkan jarak terdekat
        k_terbaik = np.argsort(jarak_titik)[:self.K]

        #3. ambil label k_terbaik
        label_k_terbaik = [self.y_train[i] for i in k_terbaik]
        
        #4. voting yg paling banyak
        hasil_voting = Counter(label_k_terbaik).most_common(1)

        return hasil_voting[0][0]

    def jarak(self, x1, x2):
        # Euclidean Distance
        return np.sqrt(np.sum((x1-x2)**2))

model_knn = KNN(k=8)
model_knn.train(x_train, y_train)

"""## **Prediksi Data Test**"""

hasil_knn = model_knn.predict(x_test)

print(hasil_knn)

y_test

"""##  **Evaluasi Model**"""

conf_matrix_knn = confusion_matrix(y_test, hasil_knn)

plt.figure(figsize=(8, 7))

group_names = ['TN', 'FP', 'FN', 'TP']
group_counts = ["{0:0.0f}".format(value) for value in conf_matrix_knn.flatten()]
group_percentages = ["{0:.2%}".format(value) for value in conf_matrix_knn.flatten() / np.sum(conf_matrix_knn)]

labels = [f"{v1}\n{v2}\n{v3}" for v1, v2, v3 in zip(group_names, group_counts, group_percentages)]
labels = np.asarray(labels).reshape(2, 2)

ax = sns.heatmap(conf_matrix_knn, annot=labels, xticklabels=[0, 1], yticklabels=[0, 1], cmap='Blues', fmt='')
bottom, top = ax.get_ylim()
ax.set_ylim(bottom + 0.5, top - 0.5)

plt.ylabel('Actual')
plt.xlabel('Predicted')
plt.title('Confusion matrix KNN', pad=16)
plt.show()

print(classification_report(y_test, hasil_knn))

def accuracy_metric(actual, predicted):
	correct = 0
    
	for i in range(len(actual)):
		if actual[i] == predicted[i]:
			correct += 1

	return correct / float(len(actual)) * 100.0

print("Accuracy :", accuracy_metric(y_test, hasil_knn))

"""## **Prediksi Data**"""

df_test = pd.read_excel('traintest.xlsx', 'test')
df_test.head()

df_id = df_test[['id']]
df_out = df_test[['x1', 'x2', 'x3']]

df_id.head()

df_out.head()

df_out_arr = df_out.to_numpy()
hasil_prediksi = model_knn.predict(df_out_arr)

print(hasil_prediksi)

df_out.insert(3, "y", hasil_prediksi)
df_out.insert(0, "id", df_id)
df_out

df_out.to_excel('output.xlsx', index=False)

