from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time as tm

class returnVal:
    #Used to return multiple variables from leastSquares fcn
    def __init__(self, m, b, error, cov):
        self.m = m
        self.b = b
        self.error = error
        self.cov = cov
        
def leastSquares(xVals, yVals, indicator, plots):
    #Ax = b where A = [A1 A2] and A = QR
    A1 = np.transpose(np.asmatrix(xVals))
    A2 = np.transpose(np.asmatrix(np.ones(np.size(A1))))
    A = np.concatenate((A1, A2), axis = 1) #Formation of A matrix
    Q, R = np.linalg.qr(A, mode = 'complete') #QR factorization to avoid a computationally expensive inverse
    bmat = np.transpose(np.asmatrix(yVals)) #Formation of b vector
    x = np.matmul(np.linalg.pinv(R),np.transpose(Q)*bmat) #Computation of m and b in y = mx + b
    m = x[0, 0]
    b = x[1, 0]
    xpts = [np.min(A1), np.max(A1)] #x pts for best fit line
    ypts = [m*xpts[0] + b, m*xpts[1] + b] #y pts for best fit line
    error = np.round(np.sqrt(np.sum(np.square(b - (m*A1 + b*A2)))),2) #Computation of euclidian norm
    
    cov = np.round(np.sum((xVals - np.mean(xVals))*(yVals - np.mean(yVals)))/np.size(yVals),2) #this doesn't seem to be right...

    if plots == True:
        # Make the plots
        plt.figure(plt.gcf().number + 1)
        plt.gcf().canvas.set_window_title(indicator)
        plt.title('Price Change vs ' + indicator)
        plt.xlabel(indicator)
        plt.ylabel('Price Change ($)')
        plt.figtext(1, 0, "Error: " + str(error), horizontalalignment = 'right', fontweight = 'extra bold')
        plt.figtext(1, 0.03, "Covariance: " + str(cov), horizontalalignment = 'right', fontweight = 'extra bold')
        plt.scatter(np.asarray(A1), np.asarray(bmat), label = 'Data')
        plt.plot(xpts, ypts, 'r', label = 'Best Fit')
        plt.legend()        

    return returnVal(m, b, error, cov)

apiKey = 'TZPVUS2QURXT3WD5'

ts = TimeSeries(key=apiKey,output_format='pandas')
ti = TechIndicators(key=apiKey,output_format='pandas')

inter = 'daily'
ticker = 'TSLA'
tperiod = 20

# Get data
EMAData, _ = ti.get_ema(symbol = ticker, interval = inter, time_period = tperiod, series_type = 'close')
MACDData, _ = ti.get_macd(symbol = ticker, interval = inter, series_type = 'close')
RSIData, _ = ti.get_rsi(symbol = ticker, interval = inter, time_period = tperiod, series_type = 'close')
CCIData, _ = ti.get_cci(symbol = ticker, interval = inter, time_period = tperiod)
tm.sleep(60)
stochData, _ = ti.get_stoch(symbol = ticker, interval = inter)
ADXData, _ = ti.get_adx(symbol = ticker, interval = inter, time_period = tperiod)
aroonData, _ = ti.get_aroon(symbol = ticker, interval = inter, time_period = tperiod)
ADData, _ = ti.get_ad(symbol = ticker, interval = inter)
OBVData, _ = ti.get_obv(symbol = ticker, interval = inter)

# Extract series from dataframe
EMAVals = EMAData.loc[:,'EMA']
MACDVals = MACDData.loc[:,'MACD']
RSIVals = RSIData.loc[:,'RSI']
CCIVals = CCIData.loc[:,'CCI']
stochVals = stochData.loc[:, 'SlowD']
stochVals.rename('stoch', inplace = True)
ADXVals = ADXData.loc[:,'ADX']
aroonVals = aroonData.loc[:,'Aroon Up'] - aroonData.loc[:,'Aroon Down']
aroonVals.rename('aroon', inplace = True)
ADVals = ADData.loc[:, 'Chaikin A/D']
ADVals.rename('AD', inplace = True)
OBVVals = OBVData.loc[:, 'OBV']

# Create dP/dt data
closeDiff = -EMAVals.diff(periods = -1)

# Line up all the data
MACDTotal = pd.concat([closeDiff, MACDVals], axis = 1)
MACDTotal.dropna(inplace = True)
RSITotal = pd.concat([closeDiff, RSIVals], axis = 1)
RSITotal.dropna(inplace = True)
CCITotal = pd.concat([closeDiff, CCIVals], axis = 1)
CCITotal.dropna(inplace = True)
stochTotal = pd.concat([closeDiff, stochVals], axis = 1)
stochTotal.dropna(inplace = True)
ADXTotal = pd.concat([closeDiff, ADXVals], axis = 1)
ADXTotal.dropna(inplace = True)
aroonTotal = pd.concat([closeDiff, aroonVals], axis = 1)
aroonTotal.dropna(inplace = True)
ADTotal = pd.concat([closeDiff, ADVals], axis = 1)
ADTotal.dropna(inplace = True)
OBVTotal = pd.concat([closeDiff, OBVVals], axis = 1)
OBVTotal.dropna(inplace = True)

# Least Squares
plots = True
MACD = leastSquares(MACDTotal['MACD'].to_numpy(), MACDTotal['EMA'].to_numpy(), 'MACD', plots)
RSI = leastSquares(RSITotal['RSI'].to_numpy(), RSITotal['EMA'].to_numpy(), 'RSI', plots)
CCI = leastSquares(CCITotal['CCI'].to_numpy(), CCITotal['EMA'].to_numpy(), 'CCI', plots)
stoch = leastSquares(stochTotal['stoch'].to_numpy(), stochTotal['EMA'].to_numpy(), 'Stochastic', plots)
ADX = leastSquares(ADXTotal['ADX'].to_numpy(), ADXTotal['EMA'].to_numpy(), 'ADX', plots)
aroon = leastSquares(aroonTotal['aroon'].to_numpy(), aroonTotal['EMA'].to_numpy(), 'aroon', plots)
AD = leastSquares(ADTotal['AD'].to_numpy(), ADTotal['EMA'].to_numpy(), 'AD', plots)
OBV = leastSquares(OBVTotal['OBV'].to_numpy(), OBVTotal['EMA'].to_numpy(), 'OBV', plots)

plt.close(1)
plt.show()