import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import matplotlib
from matplotlib.pylab import rcParams

rcParams['figure.figsize'] = 15, 6





dateparse = lambda dates: pd.datetime.strptime(dates, '%Y/%m/%d %H:%M:%S')
data = pd.read_csv('awk_format2.csv', parse_dates=['date'], index_col='date',date_parser=dateparse)
x = data.index
y = data.data
ts = data['data'] 

plt.plot(x,y)
plt.show()
