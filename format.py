import pandas as pd
import numpy as np
from scipy.interpolate import lagrange
from scipy.interpolate import interp1d
from scipy import interpolate

df=pd.read_csv('data_final.csv')
ts = df.data
for t in df.index:
  
  if ts[t] > 5500:
    print(ts[t])
    ts[t] = 5500
df.data = df.data.astype(int)

df.to_csv('data7.csv',index=0)
