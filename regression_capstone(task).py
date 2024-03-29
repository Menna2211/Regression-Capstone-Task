# -*- coding: utf-8 -*-
"""Regression Capstone(TASK).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1qByfjIxOj34lafMZ7qwViwBm8hYBhc-_

# **Mount drive and import libraries**

*   mount drive with Google Colab and Get your Authentication Key
*   change directory to E2Edata folder
"""

from google.colab import drive
drive.mount('/content/drive/')
import os
os.chdir('/content/drive/MyDrive/E2Edata')  # Fix This if your file is in a Certain Directory in Your Drive

"""**Import important libraries**"""

import  pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from  sklearn.model_selection  import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

from sklearn.preprocessing import PolynomialFeatures
from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso

from sklearn.model_selection import GridSearchCV

"""# **Date Loading**

Concrete Compressive Strength.
Compressive strength or compression strength is the capacity of a material or structure to withstand loads tending to reduce size, as opposed to tensile strength, which withstands loads tending to elongate.

Compressive strength is one of the most important engineering properties of concrete. It is a standard industrial practice that the concrete is classified based on grades. This grade is nothing but the Compressive Strength of the concrete cube or cylinder. Cube or Cylinder samples are usually tested under a compression testing machine to obtain the compressive strength of concrete. The test requisites differ country to country based on the design code.

Here is your Required [Data ](https://drive.google.com/file/d/1Csmy8fz4BDM70wD07XJYKPqOr8BAPfzE/view?usp=sharing)


1.   Load The Data File named by ''Concrete_Data.xlsx'
2.   preperaing Data






"""

df=pd.read_excel('Concrete_Data.xlsx')
df

"""Hint:
1.  Number of instances - 1030
2.  Number of Attributes - 9 (8 input features, 1 output)

Simplifying Column names
"""

df=pd.read_excel('Concrete_Data.xlsx', header = None, names=['Cement', 'Blast_Furnace_Slag', 'Fly_Ash','Water','Superplasticizer','Coarse_Aggregate','Fine Aggregate','Age','Concrete_compressive_strength'])
df.drop(df.index[0], inplace=True)
df

"""Checking for 'null' values , and Count missing values in each column"""

df.isna().sum()

"""Note : There are no null values in the data.

check type of features
"""

df.dtypes

"""* changeing Cement, Blast_Furnace_Slag ,Fly_Ash,Water ,Coarse_Aggregate ,Fine Aggregate ,Concrete_compressive_strength and Superplasticizer from object to float
* changeing Age from object to int
"""

df[['Cement', 'Blast_Furnace_Slag', 'Fly_Ash','Water','Superplasticizer','Coarse_Aggregate','Fine Aggregate','Concrete_compressive_strength']] = df[['Cement', 'Blast_Furnace_Slag', 'Fly_Ash','Water','Superplasticizer','Coarse_Aggregate','Fine Aggregate','Concrete_compressive_strength']].astype("float")
df[['Age']] = df[['Age']].astype("int")
df.dtypes

"""Describe and explore dataset"""

df.describe()

df.info()

"""plotting the heatmap Correlation coefficients between the features.

"""

import seaborn as sns
plt.figure(figsize = (8,5))
sns.heatmap(df.corr(),annot=True)

"""**Observations**


*   Cement , Age and Super plasticizer are strongly positive correlated with Compressive Strength
*   Compressive Strength seems to have a negative high correlation with water, Fly ash and Fine aggregate

*   coarse aggregate has the lowst correlation with all features , we can drop it if we need

"""

df.corr()

"""Checking the pairwise relations of Features."""

sns.pairplot(df)

"""**Observations**
*   Compressive strength increases with cement
*   Compressive strength increases with age
*   Compressive strength increases with super plasticizer
*   Concrete Compressive strength increases when less water is used
*   Flyash increases the strength decreases

Checking for duplicated data
"""

d = df[df.duplicated()]
d

"""droping the duplicated dates and keep only the first one."""

df.drop_duplicates(keep='first',inplace=True)
df

"""After removing duplicated datas
* Number of instances - 1005
* Still Number of Attributes - 9 (8 input features, 1 output)
we didn't drop any features
*NOW we will start processing the data and feed it to linear Regression models.
"""

import seaborn as sns
plt.figure(figsize = (8,5))
sns.heatmap(df.corr(),annot=True)

"""# **Data Spliting**

1.   Split training and Testing Data
2.   run the shuffle with Fix the Seed

"""

x = df.drop(['Concrete_compressive_strength'],axis = 1)
y = df['Concrete_compressive_strength']
print('The size of X :', x.shape )
print('The size Y :',  y.shape )

x_train,x_test,y_train , y_test = train_test_split(x,y , test_size =0.3 , random_state=0  )

"""3. Check the Type and Size of the Arrays you created by Printing them"""

print('The Features to be trained on :', x_train.shape )
print('The Labels to be trained on :',  y_train.shape )
print('The Features to be tested on :',  x_test.shape )
print('The Labels to be tested on :',  y_test.shape )
print('X_train type : ', type(x_train), 'X_test type :',type(x_test) ,'y_train type :', type(y_train), 'y_test type :', type(y_test) )

"""**Scaling**
Standardizing the data, to rescale the features to have a mean of zero and standard deviation of 1
"""

# Feature Scaling
sc = StandardScaler()
x_train_nor = sc.fit_transform(x_train)
x_test_nor= sc.transform(x_test)

"""## **Linear Regressors Models**
1. Linear regression
2. Lasso regression
3. Ridge regression
4. K - Nearest Neighbours

# **1- Using The Linear Regression Model**

1.1 :fit and predict Model
"""

lr = LinearRegression()
#Fit the Model to Training Set
lr.fit(x_train_nor,y_train)
#Predict The Training Set
train_preds_lr = lr.predict(x_train_nor)
#Predict The Testing Set
test_preds_lr = lr.predict(x_test_nor)
#Evaluate the Model by R squared method between Preds and Actual Valuees
print(r2_score(y_train,train_preds_lr))
print(r2_score(y_test,test_preds_lr))

"""**Enhanceing Linear Rregression Model usiong poly features and features Scalling**
1. Build a Code that Try 10 Degrees like from Degree 1 to 10 And Return The Best Degree with the Highest R Squared Value




"""

RSS=[]
for deg in range(1,10):
    #Fit and Transform the Training Features into Poly Training Features
    poly=PolynomialFeatures(degree = deg)
    x_poly=poly.fit_transform(x_train_nor)
    #Transfrom The Testing Features into Poly Testing Feature
    x_poly_test=poly.transform(x_test_nor)
    #Fit the Model to Training Set
    lp=LinearRegression()
    lp.fit(x_poly,y_train)
    #Predict The Testing Set
    lp_preds=lp.predict(x_poly_test)
    #Evaluate the Model by R squared method between Preds and Actual Valuees
    r2=r2_score(y_test , lp_preds)
    RSS.append(r2)
#The Best Degree with the Highest R Squared Value
max_value = max(RSS)
index = RSS.index(max(RSS))
print('the Max R squared method is' , max_value )
index_deg=index+1
print('the best degree is' ,index_deg )

#Fit and Transform the Training Features into Poly Training Features
poly=PolynomialFeatures(degree = index_deg)
x_poly=poly.fit_transform(x_train_nor)
#Transfrom The Testing Features into Poly Testing Feature
x_poly_test=poly.transform(x_test_nor)
#Fit the Model to Training Set
lp=LinearRegression()
lp.fit(x_poly,y_train)
#Predict The Training Set
train_preds_lp = lp.predict(x_poly)
#Predict The Testing Set
test_preds_lp = lp.predict(x_poly_test)
#Evaluate the Model by R squared method between Preds and Actual Valuees
print(r2_score(y_train,train_preds_lp))
print(r2_score(y_test,test_preds_lp))

"""# **2.Using Ridge Model**

 Set Range Of Alphas and Make A function to Select the Best One with resepct to R Squared Metric
"""

lrg=Ridge()
param = {'alpha':[0.001,0.01,0.1,1,5,10,100]}
gs_r = GridSearchCV(lrg,param_grid=param,n_jobs=-1,verbose=4)
#Fit the Model to Training Set
gs_r.fit(x_train_nor,y_train)
#Predict The Training Set
train_preds_r = gs_r.predict(x_train_nor)
#Predict The Testing Set
test_preds_r = gs_r.predict(x_test_nor)
#Evaluate the Model by R squared method between Preds and Actual Valuees
print(r2_score(y_train,train_preds_r))
print(r2_score(y_test,test_preds_r))

alpha_r=gs_r.best_params_
alpha_r=alpha_r['alpha']

gs_r.best_estimator_

RS=[]
for deg in range(1,10):
    #Fit and Transform the Training Features into Poly Training Features
    poly=PolynomialFeatures(degree = deg)
    x_poly=poly.fit_transform(x_train_nor)
    #Transfrom The Testing Features into Poly Testing Feature
    x_poly_test=poly.transform(x_test_nor)
    #Fit the Model to Training Set
    rg=Ridge(alpha=alpha_r)
    rg.fit(x_poly,y_train)
    #Predict The Testing Set
    rg_preds=rg.predict(x_poly_test)
    #Evaluate the Model by R squared method between Preds and Actual Valuees
    r2=r2_score(y_test , rg_preds)
    RS.append(r2)
#The Best Degree with the Highest R Squared Value
max_value = max(RS)
index_r = RS.index(max(RS))
print('the Max R squared method for Ridge is' , max_value )
index_ridge=index_r+1
print('the best degree is' ,index_ridge )

#Fit and Transform the Training Features into Poly Training Features
poly=PolynomialFeatures(degree = index_ridge)
x_poly=poly.fit_transform(x_train_nor)
#Transfrom The Testing Features into Poly Testing Feature
x_poly_test=poly.transform(x_test_nor)
#Fit the Model to Training Set
lrp=Ridge(alpha=alpha_r)
lrp.fit(x_poly,y_train)
#Predict The Training Set
train_preds_lrp = lrp.predict(x_poly)
#Predict The Testing Set
test_preds_lrp = lrp.predict(x_poly_test)
#Evaluate the Model by R squared method between Preds and Actual Valuees
print( r2_score(y_train,train_preds_lrp))
print( r2_score(y_test,test_preds_lrp))

"""# **3.Using Lasso Model**

Set Range Of Alphas and Make A function to Select the Best One with resepct to R Squared Metric
"""

la=Lasso()
param = {'alpha':[0.001,0.01,0.1,1,5,10,100]}
gs_l = GridSearchCV(la,param_grid=param,n_jobs=-1,verbose=4)
#Fit the Model to Training Set
gs_l.fit(x_train_nor,y_train)
#Predict The Training Set
train_preds_l = gs_l.predict(x_train_nor)
#Predict The Testing Set
test_preds_l = gs_l.predict(x_test_nor)
#Evaluate the Model by R squared method between Preds and Actual Valuees
print(r2_score(y_train,train_preds_l))
print(r2_score(y_test,test_preds_l))

alpha_l=gs_l.best_params_
alpha_l=alpha_l['alpha']

gs_l.best_estimator_

las=[]
for deg in range(1,10):
    #Fit and Transform the Training Features into Poly Training Features
    poly=PolynomialFeatures(degree = deg)
    x_poly=poly.fit_transform(x_train_nor)
    #Transfrom The Testing Features into Poly Testing Feature
    x_poly_test=poly.transform(x_test_nor)
    #Fit the Model to Training Set
    la=Lasso(alpha=alpha_l)
    la.fit(x_poly,y_train)
    #Predict The Testing Set
    la_preds=la.predict(x_poly_test)
    #Evaluate the Model by R squared method between Preds and Actual Valuees
    r2=r2_score(y_test , la_preds)
    las.append(r2)
#The Best Degree with the Highest R Squared Value
max_value = max(las)
index_l = las.index(max(las))
print('the Max R squared method for Lasso is' , max_value )
index_lasso=index_l+1
print('the best degree is' ,index_lasso )

#Fit and Transform the Training Features into Poly Training Features
poly=PolynomialFeatures(degree = index_lasso)
x_poly=poly.fit_transform(x_train_nor)
#Transfrom The Testing Features into Poly Testing Feature
x_poly_test=poly.transform(x_test_nor)
#Fit the Model to Training Set
lap=Lasso(alpha=alpha_l)
lap.fit(x_poly,y_train)
#Predict The Training Set
train_preds_lap = lap.predict(x_poly)
#Predict The Testing Set
test_preds_lap = lap.predict(x_poly_test)
#Evaluate the Model by R squared method between Preds and Actual Valuees
print( r2_score(y_train,train_preds_lap))
print( r2_score(y_test,test_preds_lap))

"""# **4.Using K - Nearest Neighbours Model**

"""

from sklearn.neighbors import KNeighborsRegressor
neigh =KNeighborsRegressor()
param = {'n_neighbors':[3,5,7,11]}
gs_kn = GridSearchCV(neigh,param_grid=param,n_jobs=-1,verbose=4)
#Fit the Model to Training Set
gs_kn.fit(x_train_nor,y_train)
#Predict The Training Set
train_preds_kn = gs_kn.predict(x_train_nor)
#Predict The Testing Set
test_preds_kn = gs_kn.predict(x_test_nor)
#Evaluate the Model by R squared method between Preds and Actual Valuees
print(r2_score(y_train,train_preds_kn))
print(r2_score(y_test,test_preds_kn))

kn_n=gs_kn.best_params_
kn_n=kn_n['n_neighbors']

gs_kn.best_params_

kn=[]
for deg in range(1,10):
    #Fit and Transform the Training Features into Poly Training Features
    poly=PolynomialFeatures(degree = deg)
    x_poly=poly.fit_transform(x_train_nor)
    #Transfrom The Testing Features into Poly Testing Feature
    x_poly_test=poly.transform(x_test_nor)
    #Fit the Model to Training Set
    neigh =KNeighborsRegressor(n_neighbors=kn_n)
    neigh.fit(x_poly,y_train)
    #Predict The Testing Set
    la_preds=neigh.predict(x_poly_test)
    #Evaluate the Model by R squared method between Preds and Actual Valuees
    r2=r2_score(y_test , la_preds)
    kn.append(r2)
#The Best Degree with the Highest R Squared Value
max_value = max(kn)
index_kn = kn.index(max(kn))
print('the Max R squared method for Lasso is' , max_value )
index_knn=index_kn+1
print('the best degree is' ,index_knn )

#Fit and Transform the Training Features into Poly Training Features
poly=PolynomialFeatures(degree = index_knn)
x_poly=poly.fit_transform(x_train_nor)
#Transfrom The Testing Features into Poly Testing Feature
x_poly_test=poly.transform(x_test_nor)
#Fit the Model to Training Set
neigh =KNeighborsRegressor(n_neighbors=kn_n)
neigh.fit(x_poly,y_train)
#Predict The Training Set
train_preds_k = neigh.predict(x_poly)
#Predict The Testing Set
test_preds_k = neigh.predict(x_poly_test)
#Evaluate the Model by R squared method between Preds and Actual Valuees
print( r2_score(y_train,train_preds_k))
print( r2_score(y_test,test_preds_k))

models = [lr,gs_r, gs_l,gs_kn ]
names = ["Linear Regression","Ridge Regression",
         "Lasso Regression","KNeighborsRegressor" ]
r2 = []
x_train_nor = sc.fit_transform(x_train)
x_test_nor= sc.transform(x_test)

for model in models:
    r2.append((r2_score(y_test, model.predict(x_test_nor))))

x = np.arange(len(names))
width = 0.3

fig, ax = plt.subplots(figsize=(5,5))
rects = ax.bar(x, r2, width)
ax.set_ylabel('R2-Score')
ax.set_xlabel('Models')
ax.set_title('R2-SCORE with Different Algorithms')
ax.set_xticks(x)
ax.set_xticklabels(names, rotation=45)
fig.tight_layout()
plt.show()

"""# **Results**

**KNeighbors Regressor** is the best choice for this problem with R2-score = 67.8%
"""

models = [lp , lrp, lap ]
names = ["Linear Regression" ,"Ridge Regression",
         "Lasso Regression"]
r2 = []
poly=PolynomialFeatures(degree = 3)
x_poly=poly.fit_transform(x_train_nor)
#Transfrom The Testing Features into Poly Testing Feature
x_poly_test=poly.transform(x_test_nor)

for model in models:
    r2.append((r2_score(y_test, model.predict(x_poly_test))))

x = np.arange(len(names))
width = 0.3

fig, ax = plt.subplots(figsize=(5,5))
rects = ax.bar(x, r2, width)
ax.set_ylabel('R2-Score')
ax.set_xlabel('Models')
ax.set_title('R2-SCORE with Different Algorithms with degree 3')
#ax.set_xticks(x)
#ax.set_xticklabels(names, rotation=45)
fig.tight_layout()
plt.show()

"""# **Results**
**BY using poly features with degree 3**

**Linear Regressor** is the best choice for this problem.with R2-SCORE=88.59%

We can repeat all those steps with drop ['Coarse_Aggregate'] feature

# **GOOD LUCK**
"""

df.drop(['Coarse_Aggregate'],axis = 1, inplace= True)
df