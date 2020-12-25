#Script to backtest trades

#Update checkDayTrades fcn
#Update buy fcn to update "stocks" sheet (most recent buy)
#Add function to return the amount of a given stock (used outside of "backtest.py"

from yahoo_fin import stock_info as si
from datetime import datetime as dt
import openpyxl as op
import numpy as np

testing = True #override trading hours restriction  

def record(time, ticker, price, quantity): #if all checks pass, record the trade
    wb = op.load_workbook(filename = 'log.xlsx')
    
    sh = wb['Trades']
    prevrow = sh.max_row
    currRow = prevrow + 1
    
    sh['A' + str(currRow)] = time
    sh['B' + str(currRow)] = ticker
    sh['C' + str(currRow)] = price
    sh['D' + str(currRow)] = quantity
    sh['E' + str(currRow)] = np.round(sh['E' + str(prevrow)].value - sh['C' + str(currRow)].value*quantity, 2)
    
    sh = wb['Stocks'] #add stock to spreadsheet
    nameFound = False

    for cell in sh['A']:
        if(cell.value == ticker):
            if quantity < 0:
                sh['B' + str(cell.row)] = time
            sh['C' + str(cell.row)] = sh['C' + str(cell.row)].value + quantity
            nameFound = True
    if nameFound == False:
        currRow = sh.max_row + 1
        sh['A' + str(currRow)] = ticker
    
    wb.save(filename = 'log.xlsx')

def checkHours(t): #check trading hours
    wb = op.load_workbook(filename = 'log.xlsx')
        
    if (t.hour >= 9 and t.hour <= 16) or(t.hour == 16 and t.minute < 30) or testing == True:
        return True
    else:
        print('Outside of Trading Hours')
        sh = wb['Errors']
        sh['A1'] = 'YES'
        wb.save(filename = 'log.xlsx')
        return False

def checkBalance(price, quantity): #check balance
    wb = op.load_workbook(filename = 'log.xlsx')
    sh = wb['Trades']
    prevrow = sh.max_row
    
    if  price*quantity <= sh['E' + str(prevrow)].value:
        return True
    else:
        print('Insufficient Funds')
        sh = wb['Errors']
        sh['A2'] = 'YES'
        wb.save(filename = 'log.xlsx')
        return False
    
def checkQty(ticker, quantity): #PREVENTING TRADE FROM GOING THROUGH
    wb = op.load_workbook(filename = 'log.xlsx')
    sh = wb['Stocks'] #add stock to spreadsheet
    nameFound = False

    for cell in sh['A']:
        if(cell.value == ticker):
            if sh['C' + str(cell.row)].value >= quantity:
                return True
            else:
                print('Insufficient Stock Quantity')
                sh = wb['Errors']
                sh['A3'] = 'YES'
                wb.save(filename = 'log.xlsx')
                return False
            nameFound = True
    if nameFound == False:
        print('Insufficient Stock Quantity')
        sh = wb['Errors']
        sh['A3'] = 'YES'
        wb.save(filename = 'log.xlsx')
        return False

def checkDayTrades(ticker): #FINISH THIS
    return True
    
def buy(ticker, quantity):
    #check trading hours, balance
    
    t = dt.now()
    price = si.get_live_price(ticker)
    
    if checkHours(t): #check trading hours
        if checkBalance(price, quantity): #check balance
            record(t, ticker, price, quantity) #record the trade
            
def sell(ticker, quantity):
    #check trading hours, quantity of stocks to be sold, day trades
    
    t = dt.now()
    price = si.get_live_price(ticker)
    
    if checkHours(t): #check trading hours
        if checkQty(ticker, quantity): #check quantity of stocks
            if checkDayTrades(ticker): #check day trades
                record(t, ticker, price, -quantity) #record the trade

sell('NIO', 45)