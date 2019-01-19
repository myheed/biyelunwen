from math import sqrt

from pandas import read_csv

from pandas import datetime

from pandas import DataFrame

from statsmodels.tsa.arima_model import ARIMA

from matplotlib import pyplot

from split import load_data_from_csv
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

series = load_data_from_csv()
X = series.values
size = int(len(X) * 0.66)
test_len = len(X) - size
train, test = X[0:size], X[size:len(X)]

history = [x for x in train]
predictions = list()
count = 0
for t in range(len(test)):
    count += 1
    model = ARIMA(history, order=(5, 1, 0))
    model_fit = model.fit(disp=0)
    output = model_fit.forecast()
    yhat = output[0]
    predictions.append(yhat)
    obs = test[t]
    history.append(obs)
    print('progress={}/{}; predicted={}; expected={}'.format(count, test_len, yhat, obs))

mae = mean_absolute_error(test, predictions)
mse = mean_squared_error(test, predictions)
rmse = sqrt(mse)
r2error = r2_score(test, predictions)

print('Test MSE: %.3f' % mse)
print('Test RMSE:%.3f' % rmse)
print('Test r2: %.5f' % r2error)

# plot

pyplot.plot(test)
pyplot.plot(predictions, color='red')
pyplot.show()
