# import the required dependencies.
import pandas as pd
import numpy as np
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

# read the excel file that contains the gradient against temperature dataset by using the panads module
df = pd.read_excel('temp.xlsx')

def pred_temp(data, input):

    x = data[['increments']] # extract the column value of increments (feature)
    y = data.tempwater # extract the column value of temperature of water (label)

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.4, random_state = 5000) # split into a 40-60 training and test set
    regr = linear_model.LinearRegression() # fit the model into a linear regression with 40% of data as the training set
    regr.fit(x_train, y_train)
    
    plt.scatter(x, y) # plotting of graph to show scatter plots and best fit line with labels.
    plt.title('Temperature against gradient')
    plt.xlabel('increments')
    plt.ylabel('Ts(t)')
    x_b = np.array(data['increments']) # conversion of data to array form
    y_b = np.array(data['tempwater'])
    z = np.polyfit(x_b, y_b, 1) 
    w = np.poly1d(z) # to fit it into a poly1d
    plt.plot(x,w(x),"r--") # this is to plot the best fit line
    plt.show()

    y_pred = regr.predict([[input]]) # predict the temperature from the input gradient that is obtained from sensor to the test set
    y_pred2 = regr.predict(x_test) # to find the r^2 value and equation of line
    print(y_test)
    print(y_pred2)

    mse = mean_squared_error(y_test, y_pred2)
    r2 = r2_score(y_test, y_pred2)
    results = {'coefficients': regr.coef_, 'intercept': regr.intercept_, 'mean square error': mse, 'r2 score': r2}
    print(results['coefficients']) # this gives you the gradient
    print(results['intercept']) # this gives you the intercept
    
    return y_pred, results['r2 score'], results['mean square error'] # returns y_pred which is the predicted temperature of water.

print(pred_temp(df, 1))
# r^2 shows the accuracy of our dataset and MSE gives the average of the square of the error
# the closer the r^2 is to 1, the better the relation between the data and the best fit line
# we are also able to obtain and formulate the eqution of y = 19.29787009x 26.806586355170374
# which is then used in our raspberry pi's sensor calculation because we are unable to use/load sklearn/kivy on Rpi smoothly
