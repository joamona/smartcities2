'''
Created on 15 jun 2023

@author: joamona
'''
from typing import Union
import tkinter
import tkinter.filedialog

class ReadCsv(object):
    '''
    classdocs
    '''
    def __init__(self, csvFileName:str=None, 
                 csvSeparator:str=',', 
                 csvHasHeader:bool=True) ->None:
        '''
        Constructor  
        '''
        if csvFileName is None:
            self.csvFileName=tkinter.filedialog.askopenfilename(title="Open csv file", filetypes=[('CSV files', '.csv .CSV')])
        else:
            self.csvFileName=csvFileName
        
        self.csvSeparator:str=csvSeparator
        self.csvHasHeader:bool=csvHasHeader
        self.csvHeader:list=[]
        self.csvData:list=[]
        self.csvNumberOfRows:int=0
        self.readCsv()
        self.csvNumberOfRows=len(self.csvData)
        
    def printConfig(self):
        print("csvFilename: " + self.csvFileName)
        print("csvSeparator: " + self.csvSeparator)
        print('csvHasHeader: ' + str(self.csvHasHeader))
        print('csvHeader: ', self.csvHeader)
        print('csvNumberOfRows: ' + str(self.csvNumberOfRows))
    
    def printData(self):
        print(self.csvData)
        
    def _convert(self,string:str):
        """
        Convert the string to int, or float, or let the string as string if it can't be 
        converted to either of int or float
        """
        value=string
        if string.isdigit():
            value=int(string)
        else:
            try:
                value=float(string)
            except:
                pass
        return value
    
    def readCsv(self):
        with open(self.csvFileName, 'rt') as f:
            records = f.readlines()
        
        #print(records)
        #header
        offset=0
        if self.csvHasHeader is True:
            offset=1
            header=records[0].upper().strip().split(self.csvSeparator)
            self.csvHeader=header
        data=[]
        r=range(offset,len(records))
        for i in r:
            values=[]
            record=records[i]
            for field in record.strip().split(self.csvSeparator):
                values.append(self._convert(field))
            data.append(values)
        self.csvData=data
        return(data)
    
