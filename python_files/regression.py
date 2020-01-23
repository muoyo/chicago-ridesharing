"""
##### DATA VISUALIZATIONS #####

This module contains our functions for linear regression.

"""


import pandas as pd
import statsmodels.api as sm
import sklearn.linear_model as lm
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.metrics import mean_squared_error, mean_squared_log_error


def OLS(y, X):
    model = sm.OLS(y, X).fit()
    
    return model.summary()

def LinearRegression(X, y, prefix='Training'):
    
    # Fit the model
    linreg = lm.LinearRegression()
    linreg.fit(X, y)

    # Print R2 and MSE
    print(f'{ prefix } r^2:', linreg.score(X, y))
    print(f'{ prefix } MSE:', mean_squared_error(y, linreg.predict(X)))
    
    return linreg


def Lasso(X, y, prefix='Training'):
    
    # Fit the model
    lasso = lm.Lasso(alpha=1) # Lasso is also known as the L1 norm 
    lasso.fit(X, y)

    # Print R2 and MSE
    print(f'{ prefix } r^2:', lasso.score(X, y))
    print(f'{ prefix } MSE:', mean_squared_error(y, lasso.predict(X)))
    
    return lasso


def Ridge(X, y, prefix='Training'):
    
    # Fit the model
    ridge = lm.Ridge(alpha=10) # Ridge is also known as the L2 norm
    ridge.fit(X, y)

    # Print R2 and MSE
    print(f'{ prefix } r^2:', ridge.score(X, y))
    print(f'{ prefix } MSE:', mean_squared_error(y, ridge.predict(X)))

    return ridge

def get_train_test_split(df, test_size=.25):

    # Limit to the columns we are interested in: 
    # 'apparentTemperature', 'start_weekday', 'start_hour', (OR 'start_time_block'), 'pickup_community_area' 

    columns_to_use = ['apparentTemperature', 'start_weekday', 'start_time_block', 'pickup_community_area']
    columns_to_drop = [ col for col in df.columns if col not in columns_to_use ]

    # Use dependent variables listed above to predict the independent variable: 'trip_total' OR 'fare'
    X = df.drop(columns=columns_to_drop)
    y = df['trip_total']

    # deal with any null values
    X['apparentTemperature']=X['apparentTemperature'].fillna(X['apparentTemperature'].median())
    X['pickup_community_area']=X['pickup_community_area'].fillna('0')

    # Split out continuous & categorical variables
    cont_cols = ['apparentTemperature']
    cat_cols = [ col for col in columns_to_use if col not in cont_cols ]

    enc = OneHotEncoder()


    # Split data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size)

    X_train_cont = X_train[cont_cols]
    X_train_cat = X_train[cat_cols]

    # ss = StandardScaler()
    # X_train_cont = pd.DataFrame(ss.fit_transform(X_train_cont))

    # Transform training set
    X_train_enc = enc.fit_transform(X_train_cat, y_train)

    # Convert these columns into a DataFrame 
    columns = enc.get_feature_names(input_features=X_train_cat.columns)
    X_train_cat = pd.DataFrame(X_train_enc.todense(), columns=columns, index=X_train.index)

    # Combine categorical and continuous features into the final dataframe
    X_train = pd.concat([X_train_cont, X_train_cat], axis=1)
    
    return X_train, X_test, y_train, y_test