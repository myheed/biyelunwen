from pandas import read_csv

from pandas import datetime

from pandas import DataFrame

from statsmodels.tsa.arima_model import ARIMA

from matplotlib import pyplot

from split import load_data_from_csv

series = load_data_from_csv()

model = ARIMA(series, order=(5, 1, 0))

model_fit = model.fit(disp=0)

print(model_fit.summary())

# plot residual errors

residuals = DataFrame(model_fit.resid)

residuals.plot()

pyplot.show()

residuals.plot(kind='kde')

pyplot.show()

print(residuals.describe())
