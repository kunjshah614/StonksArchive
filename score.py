import leastSquares as ls
import time as tm
import numpy as np
import pandas as pd
import openpyxl as op


def learn(tickerList):
    wb = op.load_workbook(filename = 'stockData.xlsx')
    sh = wb['stockData']

    for i in tickerList:
        print(i)
        
        vals = ls.getWeighting(i, 'daily')
        tm.sleep(60)
        
        nameFound = False
        
        for cell in sh['A']:     
            if(cell.value == i): #if the stock already exists
                sh['B' + str(cell.row)] = vals.loc[0,'m']
                sh['C' + str(cell.row)] = vals.loc[1,'m']
                sh['D' + str(cell.row)] = vals.loc[2,'m']
                sh['E' + str(cell.row)] = vals.loc[3,'m']
                sh['F' + str(cell.row)] = vals.loc[4,'m']
                sh['G' + str(cell.row)] = vals.loc[5,'m']
                sh['H' + str(cell.row)] = vals.loc[6,'m']
                sh['I' + str(cell.row)] = vals.loc[7,'m']
                sh['J' + str(cell.row)] = vals.loc[0,'b']
                sh['K' + str(cell.row)] = vals.loc[1,'b']
                sh['L' + str(cell.row)] = vals.loc[2,'b']
                sh['M' + str(cell.row)] = vals.loc[3,'b']
                sh['N' + str(cell.row)] = vals.loc[4,'b']
                sh['O' + str(cell.row)] = vals.loc[5,'b']
                sh['P' + str(cell.row)] = vals.loc[6,'b']
                sh['Q' + str(cell.row)] = vals.loc[7,'b']
                sh['R' + str(cell.row)] = vals.loc[0,'w']
                sh['S' + str(cell.row)] = vals.loc[1,'w']
                sh['T' + str(cell.row)] = vals.loc[2,'w']
                sh['U' + str(cell.row)] = vals.loc[3,'w']
                sh['V' + str(cell.row)] = vals.loc[4,'w']
                sh['W' + str(cell.row)] = vals.loc[5,'w']
                sh['X' + str(cell.row)] = vals.loc[6,'w']
                sh['Y' + str(cell.row)] = vals.loc[7,'w']
                nameFound = True
        if nameFound == False: #if the stock does not exist (has never been bought before)
            currRow = sh.max_row + 1
            sh['A' + str(currRow)] = i
            sh['B' + str(currRow)] = vals.loc[0,'m']
            sh['C' + str(currRow)] = vals.loc[1,'m']
            sh['D' + str(currRow)] = vals.loc[2,'m']
            sh['E' + str(currRow)] = vals.loc[3,'m']
            sh['F' + str(currRow)] = vals.loc[4,'m']
            sh['G' + str(currRow)] = vals.loc[5,'m']
            sh['H' + str(currRow)] = vals.loc[6,'m']
            sh['I' + str(currRow)] = vals.loc[7,'m']
            sh['J' + str(currRow)] = vals.loc[0,'b']
            sh['K' + str(currRow)] = vals.loc[1,'b']
            sh['L' + str(currRow)] = vals.loc[2,'b']
            sh['M' + str(currRow)] = vals.loc[3,'b']
            sh['N' + str(currRow)] = vals.loc[4,'b']
            sh['O' + str(currRow)] = vals.loc[5,'b']
            sh['P' + str(currRow)] = vals.loc[6,'b']
            sh['Q' + str(currRow)] = vals.loc[7,'b']
            sh['R' + str(currRow)] = vals.loc[0,'w']
            sh['S' + str(currRow)] = vals.loc[1,'w']
            sh['T' + str(currRow)] = vals.loc[2,'w']
            sh['U' + str(currRow)] = vals.loc[3,'w']
            sh['V' + str(currRow)] = vals.loc[4,'w']
            sh['W' + str(currRow)] = vals.loc[5,'w']
            sh['X' + str(currRow)] = vals.loc[6,'w']
            sh['Y' + str(currRow)] = vals.loc[7,'w']
        
    wb.save(filename = 'stockData.xlsx')

def scores(tickerList):
    wb = op.load_workbook(filename = 'stockData.xlsx')
    sh = wb['stockData']
    prediction = []

    for i in tickerList:
        print(i)
        
        x = ls.getCurrent(i, 'daily')
        tm.sleep(60)
        
        nameFound = False
        
        for cell in sh['A']:     
            if(cell.value == i): #if the stock already exists
                m = np.array([sh['B' + str(cell.row)].value,
                     sh['C' + str(cell.row)].value,
                     sh['D' + str(cell.row)].value,
                     sh['E' + str(cell.row)].value,
                     sh['F' + str(cell.row)].value,
                     sh['G' + str(cell.row)].value,
                     sh['H' + str(cell.row)].value,
                     sh['I' + str(cell.row)].value])
                b = np.array([sh['J' + str(cell.row)].value,
                     sh['K' + str(cell.row)].value,
                     sh['L' + str(cell.row)].value,
                     sh['M' + str(cell.row)].value,
                     sh['N' + str(cell.row)].value,
                     sh['O' + str(cell.row)].value,
                     sh['P' + str(cell.row)].value,
                     sh['Q' + str(cell.row)].value])
                w = np.array([sh['R' + str(cell.row)].value,
                     sh['S' + str(cell.row)].value,
                     sh['T' + str(cell.row)].value,
                     sh['U' + str(cell.row)].value,
                     sh['V' + str(cell.row)].value,
                     sh['W' + str(cell.row)].value,
                     sh['X' + str(cell.row)].value,
                     sh['Y' + str(cell.row)].value])
                score = w*(m*x + b)
                score = score.sum()
                prediction.append(score)
    allPred = pd.DataFrame({'ticker': tickerList, 'score': prediction})
    allPred.sort_values('score', inplace = True)
    return(allPred)
    
tickerList = ['PLUG', 'NIO', 'RIDE', 'FUV', 'FCEL', 'CBAT', 'BLNK', 'SPY']
print('Estimated Time: %d minutes' %(5*np.size(tickerList)))
learn(tickerList)
tm.pause(60)
ranking = scores(tickerList)
print(ranking)