from alpha_vantage.techindicators import TechIndicators
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time as tm

apiKey = '63SKE6NA9MIIRXO5'
# apiKey = 'TZPVUS2QURXT3WD5'
# apiKey = 'Q207WCDSVFKS8KOG'
ti = TechIndicators(key=apiKey,output_format='pandas')
tperiod = 20
# ind = ['EMA', 'MACD', 'RSI', 'CCI', 'stoch', 'ADX', 'aroon', 'AD', 'OBV']

class returnVal:
        #Used to return multiple variables from leastSquares fcn
    def __init__(self, m, b, error, corr):
        self.m = m
        self.b = b
        self.error = error
        self.corr = corr
            
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
    error = np.sqrt(np.sum(np.square(b - (m*A1 + b*A2)))) #Computation of euclidian norm
    
    cov = np.sum((xVals - np.mean(xVals))*(yVals - np.mean(yVals)))/np.size(yVals)
    varX = np.sum(np.square(xVals - np.mean(xVals)))/np.size(xVals)
    varY = np.sum(np.square(yVals - np.mean(yVals)))/np.size(yVals)
    corr = cov/(np.sqrt(varY)*np.sqrt(varX))

    if plots == True:
        # Make the plots
        plt.figure(plt.gcf().number + 1)
        plt.gcf().canvas.set_window_title(indicator)
        plt.title('Price Change vs ' + indicator)
        plt.xlabel(indicator)
        plt.ylabel('Price Change ($)')
        plt.figtext(1, 0, "Error: " + str(np.round(error, 2)), horizontalalignment = 'right', fontweight = 'extra bold')
        plt.figtext(1, 0.03, "Correlation: " + str(np.round(corr, 2)), horizontalalignment = 'right', fontweight = 'extra bold')
        plt.scatter(np.asarray(A1), np.asarray(bmat), label = 'Data')
        plt.plot(xpts, ypts, 'r', label = 'Best Fit')
        plt.legend()        

    return returnVal(m, b, error, corr)

def getWeighting (ticker, inter):
    # Get data
    print('1')
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

    print('2')
    # Extract series from dataframe
    EMAVals = EMAData.loc[:,'EMA']
    MACDVals = MACDData.loc[:,'MACD']
    RSIVals = RSIData.loc[:,'RSI']
    CCIVals = CCIData.loc[:,'CCI']
    stochVals = stochData.loc[:, 'SlowD'].rename('stoch', inplace = True)
    ADXVals = ADXData.loc[:,'ADX']
    aroonVals = (aroonData.loc[:,'Aroon Up'] - aroonData.loc[:,'Aroon Down']).rename('aroon', inplace = True)
    ADVals = ADData.loc[:, 'Chaikin A/D'].rename('AD', inplace = True)
    OBVVals = OBVData.loc[:, 'OBV']

    print('3')
    # Create dP/dt data
    closeDiff = -EMAVals.diff(periods = -1)

    print('4')
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

    print('5')
    # Least Squares (individual)
    plots = False
    MACD = leastSquares(MACDTotal['MACD'].to_numpy(), MACDTotal['EMA'].to_numpy(), 'MACD', plots)
    RSI = leastSquares(RSITotal['RSI'].to_numpy(), RSITotal['EMA'].to_numpy(), 'RSI', plots)
    CCI = leastSquares(CCITotal['CCI'].to_numpy(), CCITotal['EMA'].to_numpy(), 'CCI', plots)
    stoch = leastSquares(stochTotal['stoch'].to_numpy(), stochTotal['EMA'].to_numpy(), 'Stochastic', plots)
    ADX = leastSquares(ADXTotal['ADX'].to_numpy(), ADXTotal['EMA'].to_numpy(), 'ADX', plots)
    aroon = leastSquares(aroonTotal['aroon'].to_numpy(), aroonTotal['EMA'].to_numpy(), 'aroon', plots)
    AD = leastSquares(ADTotal['AD'].to_numpy(), ADTotal['EMA'].to_numpy(), 'AD', plots)
    OBV = leastSquares(OBVTotal['OBV'].to_numpy(), OBVTotal['EMA'].to_numpy(), 'OBV', plots)

    print('6')
    # Linear Combination
    w = np.array([MACD.corr, RSI.corr, CCI.corr, stoch.corr, ADX.corr, aroon.corr, AD.corr, OBV.corr])
    w = w/w.sum()
    total = pd.DataFrame({'Indicator': ['MACD', 'RSI', 'CCI', 'stoch', 'ADX', 'aroon', 'AD', 'OBV'],
                          'w': w,
                          'm': [MACD.m, RSI.m, CCI.m, stoch.m, ADX.m, aroon.m, AD.m, OBV.m],
                          'b': [MACD.b, RSI.b, CCI.b, stoch.b, ADX.b, aroon.b, AD.b, OBV.b]})
    
    print('7')
    plt.close(1)
    plt.show()
    
    return total

def getCurrent(ticker, inter):
    # Get data
    print('8')
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
    
    print('9')
    EMAVals = EMAData.loc[:,'EMA']
    MACDVals = MACDData.loc[:,'MACD']
    RSIVals = RSIData.loc[:,'RSI']
    CCIVals = CCIData.loc[:,'CCI']
    stochVals = stochData.loc[:, 'SlowD'].rename('stoch', inplace = True)
    ADXVals = ADXData.loc[:,'ADX']
    aroonVals = (aroonData.loc[:,'Aroon Up'] - aroonData.loc[:,'Aroon Down']).rename('aroon', inplace = True)
    ADVals = ADData.loc[:, 'Chaikin A/D'].rename('AD', inplace = True)
    OBVVals = OBVData.loc[:, 'OBV']
    
    print('10')
    info = np.array([MACDVals.iloc[-1], RSIVals.iloc[-1], CCIVals.iloc[-1], stochVals.iloc[-1], ADXVals.iloc[-1], aroonVals.iloc[-1], ADVals.iloc[-1], OBVVals.iloc[-1]])
    
#     info = pd.DataFrame({'Indicator': ['MACD', 'RSI', 'CCI', 'stoch', 'ADX', 'aroon', 'AD', 'OBV'],
#                          'x':[MACDVals.iloc[-1], RSIVals.iloc[-1], CCIVals.iloc[-1], stochVals.iloc[-1], ADXVals.iloc[-1], aroonVals.iloc[-1], ADVals.iloc[-1], OBVVals.iloc[-1]]})

    return info