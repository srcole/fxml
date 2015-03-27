# -*- coding: utf-8 -*-
"""
This is a scraper to retrieve data from the forexite site
"""

import urllib
import zipfile
import os

def num2date(num):
    """Takes a number between 1 and 99 and returns that number as a string of
    length 2.

    Parameters
    ---------
    num : int
        The number that needs to be converted into a string

    Returns
    ------
    date : str
        String of number
    """
    
    if (num >= 1 and num <= 9):
        date = '0' + str(num)
    elif (num >= 10 and num <= 99):
        date = str(num)
        
    return date
    
years = range(2011,2012)
months = range(1,2)
dates = range(1,15)
filedest = 'C:\\fxdata\\'

day = 1;
for i in years:
    year = num2date(i-2000)
    for j in months:
        month = num2date(j)
        for k in dates:
            date = num2date(k)
            
            # example url, Sep 29 2011: "http://www.forexite.com/free_forex_quotes/2011/09/290911.zip"
            url = 'http://www.forexite.com/free_forex_quotes/' + str(i) + '/' + month + '/' + date + month + year + '.zip'
            filename = date + month + year + '.zip'
            filepath = filedest + filename
            urllib.urlretrieve(url, filepath)
            
            filesize = os.path.getsize(filepath)
            if filesize > 2000:
                with zipfile.ZipFile(filepath, "r") as z:
                    z.extractall(filedest)
                filepathtxt = filepath[:-3] + 'txt'
                new_filepath = filedest + 'fxday' + str(day) + '.txt'
                day +=1
                os.rename(filepathtxt,new_filepath)            
            os.remove(filepath)