# Import libraries

import pandas  as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.linear_model import LinearRegression,Lasso
from sklearn.ensemble import RandomForestRegressor
# import data
df = pd.read_csv('data_eda.csv')

# Chose relevant columns
df.columns

df_model = df[['AVR salary','Rating', 'Size', 'Type of ownership','Industry','Sector','Revenue','num_comp','hourly','employer provided','job_state','same_state','age','python_yn','spark','aws', 'excel','job_simp','senority','desc_len']]

# get dummies data
df_dum = pd.get_dummies(df_model)

# train, test split
x = df_dum.drop('AVR salary', axis=1)
y = df_dum['AVR salary'].values

x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=0.2, random_state=42)

# Multiple linear Regression
import statsmodels.api as sm

x_sm = sm.add_constant(x)
model = sm.OLS(y,x_sm)
model.fit().summary()

lm = LinearRegression()
lm.fit(x_train,y_train)

np.mean(cross_val_score(lm,x_train,y_train, scoring = 'neg_mean_absolute_error', cv = 3))
# Lasso Regression
lm_l = Lasso(.13)
np.mean(cross_val_score(lm_l,x_train,y_train, scoring = 'neg_mean_absolute_error', cv = 3))


## Create 2 empty list for alpha and error
alpha = []
error = []

## plot the alpha
for i in range (1,100):
    alpha.append(i/100)
    lml = Lasso(alpha=(i/100))
    error.append(np.mean(cross_val_score(lml,x_train,y_train, scoring = 'neg_mean_absolute_error', cv=3)))

plt.plot(alpha, error)

err = tuple(zip(alpha, error))
df_err = pd.DataFrame(err, columns=['alpha','error'])

df_err[df_err.error == max(df_err.error)]


# Random Forest
rf = RandomForestRegressor()

np.mean(cross_val_score(rf, x_train, y_train, scoring='neg_mean_absolute_error', cv=3))

# Tune Model GridsearchCV
parameters = {'n_estimators':range(10,300,10), 'criterion':('squared_error','absolute_error'), 'max_features':(1.0,'sqrt','log2')}

gs = GridSearchCV(rf, parameters, scoring = 'neg_mean_absolute_error', cv=3)
gs.fit(x_train,y_train)

gs.best_score_
gs.best_estimator_
# test Ensemble
tpred_lm = lm.predict(x_test)
tpred_lml = lm_l.predict(x_test)
tpred_rf = gs.best_estimator_.predict(x_test)


from sklearn.metrics import mean_absolute_error
mean_absolute_error(y_test, tpred_lm)
mean_absolute_error(y_test, tpred_lml)
mean_absolute_error(y_test, rf)

mean_absolute_error(y_test, (tpred_lm + tpred_rf)/2)