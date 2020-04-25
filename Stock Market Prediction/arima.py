#!/usr/bin/env python
# coding: utf-8

# In[1]:


from datetime import datetime
import numpy as np             #for numerical computations like log,exp,sqrt etc
import pandas as pd            #for reading & storing data, pre-processing
import matplotlib.pylab as plt #for visualization
#for making sure matplotlib plots are generated in Jupyter notebook itself
get_ipython().run_line_magic('matplotlib', 'inline')
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.stattools import acf, pacf
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.arima_model import ARIMA
from matplotlib.pylab import rcParams
rcParams['figure.figsize'] = 10, 6


# In[2]:


path = "/Users/lavidhaliwal/Downloads/sandp500/individual_stocks_5yr/individual_stocks_5yr/GOOG_data.csv" 
df = pd.read_csv(path)


# In[3]:


df=df.drop(columns=['open','high','low','volume','Name'])
df.date=pd.to_datetime(df.date)
# Resampling to daily,monthly,annual and quarterly frequency
df.index = df.date
df = df.resample('D').mean()
df_M = df.resample('M').mean()
df_Y = df.resample('A-DEC').mean()
df_Q = df.resample('Q-DEC').mean()


# In[4]:


df_M=df_M.dropna()
df_Y=df_Y.dropna()
df_Q = df_Q.dropna()
df=df.dropna()


# In[5]:


# PLOTS
fig = plt.figure(figsize=[14, 6])
plt.suptitle('Stock price', fontsize=22)

plt.subplot(221)
plt.plot(df.close, '-', label='Daily')
plt.legend()

plt.subplot(222)
plt.plot(df_M.close, '-', label='Monthly')
plt.legend()

plt.subplot(223)
plt.plot(df_Q.close, '-', label='Quarterly')
plt.legend()

plt.subplot(224)
plt.plot(df_Y.close, '-', label='Yearly')
plt.legend()

# plt.tight_layout()
plt.show()


# In[6]:


#splitting
splitpoint=int(df_M.size*0.8)

indexed_dataset=df_M[0:splitpoint]
df_test=df_M[splitpoint-1:]


# In[7]:


#Determining averages
roll_avg = indexed_dataset.rolling(window=12).mean() #window size 12 denotes 12 months, giving rolling mean at yearly level
roll_std_dev = indexed_dataset.rolling(window=12).std()
#print(roll_avg,roll_std_dev)


# In[8]:


#Plot rolling statistics
orig = plt.plot(indexed_dataset, color='blue', label='Original')
mean = plt.plot(roll_avg, color='red', label='Rolling average')
std = plt.plot(roll_std_dev, color='black', label='Rolling Standard deviation')
plt.legend(loc='best')
plt.title('Rolling mean & Standard Deviation')
plt.show(block=False)


# In[9]:


#Augmented-Dickey-Fuller-test():
print('Dickey-Fuller-Test::')
test = adfuller(indexed_dataset['close'], autolag='AIC')

d_output = pd.Series(test[0:4], index=['Test-stats','p-value','Lags','Observations used'])
for key,value in test[4].items():
    d_output['Critical-Value (%s)'%key] = value
    
print(d_output)


# In[10]:


#Trend estimation and data transformation
indexed_dataset_logScale = np.log(indexed_dataset)

plt.plot(indexed_dataset_logScale)


# In[ ]:





# In[ ]:





# In[11]:


def test_stationarity(time_series):
    
    #Determine rolling statistics
    moving_avg = time_series.rolling(window=12).mean()
    moving_std = time_series.rolling(window=12).std()
    
    #Plot rolling statistics
    orig = plt.plot(time_series, color='blue', label='Original')
    mean = plt.plot(moving_avg, color='red', label='Rolling Mean')
    std = plt.plot(moving_std, color='black', label='Rolling Std')
    plt.legend(loc='best')
    plt.title('Rolling Mean & Standard Deviation')
    plt.show(block=False)
    
    #Perform Dickey–Fuller test:
    print('Dickey-Fuller-Test::')
    dftest = adfuller(time_series['close'], autolag='AIC')
    d_output = pd.Series(dftest[0:4], index=['Test-stats','p-value','Lags','Observations used'])
    for key,value in dftest[4].items():
        d_output['Critical Value (%s)'%key] = value
    print(d_output)
    


# In[ ]:





# In[12]:


datasetLogDiffShifting = indexed_dataset_logScale - indexed_dataset_logScale.shift(1)
plt.plot(datasetLogDiffShifting)


# In[13]:


datasetLogDiffShifting.dropna(inplace=True)
test_stationarity(datasetLogDiffShifting)


# In[14]:


decomposition = seasonal_decompose(indexed_dataset_logScale) 

trend = decomposition.trend
seasonal = decomposition.seasonal
residual = decomposition.resid

plt.subplot(411)
plt.plot(indexed_dataset_logScale, label='Original')
plt.legend(loc='best')

plt.subplot(412)
plt.plot(trend, label='Trend')
plt.legend(loc='best')

plt.subplot(413)
plt.plot(seasonal, label='Seasonality')
plt.legend(loc='best')

plt.subplot(414)
plt.plot(residual, label='Residuals')
plt.legend(loc='best')

plt.tight_layout()


# In[15]:



lag_acf = acf(datasetLogDiffShifting, nlags=20)
lag_pacf = pacf( datasetLogDiffShifting, nlags=20, method='ols')

#Plot ACF:
plt.subplot(121)
plt.plot(lag_acf)
plt.axhline(y=0, linestyle='--', color='gray')
plt.axhline(y=-1.96/np.sqrt(len(datasetLogDiffShifting)), linestyle='--', color='gray')
plt.axhline(y=1.96/np.sqrt(len(datasetLogDiffShifting)), linestyle='--', color='gray')
plt.title('Autocorrelation Function')            

#Plot PACF
plt.subplot(122)
plt.plot(lag_pacf)
plt.axhline(y=0, linestyle='--', color='gray')
plt.axhline(y=-1.96/np.sqrt(len(datasetLogDiffShifting)), linestyle='--', color='gray')
plt.axhline(y=1.96/np.sqrt(len(datasetLogDiffShifting)), linestyle='--', color='gray')
plt.title('Partial Autocorrelation Function')
            
plt.tight_layout()          


# In[ ]:





# In[16]:


#AR Model

model = ARIMA(indexed_dataset_logScale, order=(2,1,0))
results_AR = model.fit(disp=-1)
plt.plot(datasetLogDiffShifting)
plt.plot(results_AR.fittedvalues, color='red')
plt.title('MSE: %.4f'%sum((results_AR.fittedvalues - datasetLogDiffShifting['close'])**2))
print('Plotting AR model')


# In[17]:


#MA Model
model = ARIMA(indexed_dataset_logScale, order=(0,1,2))
results_MA = model.fit(disp=-1)
plt.plot(datasetLogDiffShifting)
plt.plot(results_MA.fittedvalues, color='red')
plt.title('MSE: %.4f'%sum((results_MA.fittedvalues - datasetLogDiffShifting['close'])**2))
print('Plotting MA model')


# In[18]:


#AR+I+MA = ARIMA model
model = ARIMA(indexed_dataset_logScale, order=(2,1,2))
results_ARIMA = model.fit(disp=-1)
plt.plot(datasetLogDiffShifting)
plt.plot(results_ARIMA.fittedvalues, color='red')
plt.title('MSE: %.4f'%sum((results_ARIMA.fittedvalues - datasetLogDiffShifting['close'])**2))
print('Plotting ARIMA model')


# In[19]:


# visualising the results on original scale
fig=results_ARIMA.plot_predict('2014','2018')


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




