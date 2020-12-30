import getStockData as sd
import time as tm
import numpy as np
import pandas as pd
import openpyxl as op

mData = ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'] #columns containing each type of data
bData = ['J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q']
wData = ['R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y']

# def populate(ticker, stockConstants, rowNumber, sh):
#     for j in mData:
#         sh[j + str(rowNumber)] = stockConstants.loc[mData.index(j),'m']
#     for k in bData:
#         sh[k + str(rowNumber)] = stockConstants.loc[bData.index(k),'b']
#     for l in wData:
#         sh[l + str(rowNumber)] = stockConstants.loc[wData.index(l),'w']
# 
# def learn(tickerList, inter):
#     wb = op.load_workbook(filename = 'stockData.xlsx') #open the workbook
#     sh = wb[inter] #open the worksheet
# 
#     for i in tickerList: #for each of the tickers...
#         print(i)
#         stockConstants = sd.getWeighting(i, inter) #get m (slope), b (intercept), and w (weighting)
#         
#         nameFound = False #used to determine if the stock already exists
#         
#         for cell in sh['A']: #loop through every cell in column 'A'    
#             if(cell.value == i): #if the stock already exists...
#                 rowNumber = cell.row #the row number is the row with the ticker in it
#                 nameFound = True 
#         if nameFound == False: #if the stock does not exist (has never been bought before)...
#             rowNumber = sh.max_row + 1 #the row number is the next empty row
#             sh['A' + str(rowNumber)] = i #enter the ticker name in column 'A'
#         print('(Writing Data to Spreadsheet)\n')
#         populate(i, stockConstants, rowNumber, sh) #populate the row with the data
#         
#     wb.save(filename = 'stockData.xlsx') #save the workbook
# 
# def predict(tickerList, inter):
#     wb = op.load_workbook(filename = 'stockData.xlsx')
#     sh = wb[inter]
#     prediction = []
#     print('\n')
#     
#     for i in tickerList:
#         print(i)
#         x = sd.getCurrent(i, inter)
#         
#         nameFound = False
#         
#         for cell in sh['A']:
#             if(cell.value == i): #if the stock already exists
#                 print('(Reading Data from Spreadsheet)')
#                 m = np.array([sh['B' + str(cell.row)].value,
#                      sh['C' + str(cell.row)].value,
#                      sh['D' + str(cell.row)].value,
#                      sh['E' + str(cell.row)].value,
#                      sh['F' + str(cell.row)].value,
#                      sh['G' + str(cell.row)].value,
#                      sh['H' + str(cell.row)].value,
#                      sh['I' + str(cell.row)].value])
#                 b = np.array([sh['J' + str(cell.row)].value,
#                      sh['K' + str(cell.row)].value,
#                      sh['L' + str(cell.row)].value,
#                      sh['M' + str(cell.row)].value,
#                      sh['N' + str(cell.row)].value,
#                      sh['O' + str(cell.row)].value,
#                      sh['P' + str(cell.row)].value,
#                      sh['Q' + str(cell.row)].value])
#                 w = np.array([sh['R' + str(cell.row)].value,
#                      sh['S' + str(cell.row)].value,
#                      sh['T' + str(cell.row)].value,
#                      sh['U' + str(cell.row)].value,
#                      sh['V' + str(cell.row)].value,
#                      sh['W' + str(cell.row)].value,
#                      sh['X' + str(cell.row)].value,
#                      sh['Y' + str(cell.row)].value])
#                 score = w*(m*x + b)
#                 score = score.sum()
#                 prediction.append(score)
#     allPred = pd.DataFrame({'ticker': tickerList, 'score': prediction})
#     allPred.sort_values('score', inplace = True)
#     return(allPred)

def learn(tickerList, inter):
    wb = op.load_workbook(filename = 'stockData.xlsx') #open the workbook
    sh = wb['test'] #open the worksheet

    for i in tickerList: #for each of the tickers...
        print(i)
        stockConstants = sd.getWeighting(i, inter) #get m (slope), b (intercept), and w (weighting)
        tm.sleep(60)
        
        nameFound = False #used to determine if the stock already exists
        
        for cell in sh['A']: #loop through every cell in column 'A'    
            if(cell.value == i): #if the stock already exists...
                rowNumber = cell.row #the row number is the row with the ticker in it
                nameFound = True 
        if nameFound == False: #if the stock does not exist (has never been bought before)...
            rowNumber = sh.max_row + 1 #the row number is the next empty row
            sh['A' + str(rowNumber)] = i #enter the ticker name in column 'A'
        print('(Writing Data to Spreadsheet)\n')
        stockConstants = stockConstants.tolist()
        sh['B' + str(rowNumber)] = stockConstants[0][0]
        sh['C' + str(rowNumber)] = stockConstants[1][0]
        sh['D' + str(rowNumber)] = stockConstants[2][0]
        sh['E' + str(rowNumber)] = stockConstants[3][0]
        sh['F' + str(rowNumber)] = stockConstants[4][0]
        sh['G' + str(rowNumber)] = stockConstants[5][0]
        sh['H' + str(rowNumber)] = stockConstants[6][0]
        sh['I' + str(rowNumber)] = stockConstants[7][0]
#         sh['J' + str(rowNumber)] = stockConstants[8][0] 
        wb.save(filename = 'stockData.xlsx') #save the workbook

def predict(tickerList, inter):
    wb = op.load_workbook(filename = 'stockData.xlsx')
    sh = wb['test']
    prediction = []
    print('\n')
    
    for i in tickerList:
        print(i)
        x = sd.getCurrent(i, inter)
        tm.sleep(60)
        
        nameFound = False
        
        for cell in sh['A']:
            if(cell.value == i): #if the stock already exists
                print('(Reading Data from Spreadsheet)')
                a = np.array([sh['B' + str(cell.row)].value,
                     sh['C' + str(cell.row)].value,
                     sh['D' + str(cell.row)].value,
                     sh['E' + str(cell.row)].value,
                     sh['F' + str(cell.row)].value,
                     sh['G' + str(cell.row)].value,
                     sh['H' + str(cell.row)].value,
                     sh['I' + str(cell.row)].value])
                score = a*x
                score = score.sum()
#                 score = score.sum() + sh['J' + str(cell.row)].value 
                prediction.append(score)
    allPred = pd.DataFrame({'ticker': tickerList, 'score': prediction})
#     allPred.sort_values('score', inplace = True)
    return(allPred)
    
tickerList = ['IBM', 'NIO', 'TSLA', 'PLUG', 'NKLA', 'MSFT', 'SNE']
inter = 'daily'
print('Estimated Time: %d minutes' %(2*np.size(tickerList)))
# learn(tickerList, inter)
ranking = predict(tickerList, inter)
print(ranking)