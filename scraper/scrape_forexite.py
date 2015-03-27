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
    


day = 1;
for i in range(2011,2012):
    for j in range(1,13):
        for k in range(1,32):
            
            date = num2date(k)
            month = num2date(j)
            year = num2date(i-2000)
            
            # example url, Sep 29 2011: "http://www.forexite.com/free_forex_quotes/2011/09/290911.zip"
            url = 'http://www.forexite.com/free_forex_quotes/' + str(i) + '/' + month + '/' + date + month + year + '.zip'
            filename = date + month + year + '.zip'
            filedest = 'C:\\Users\\Scott\\Documents\\Python codes\\pyforex\\'
            filepath = filedest + filename
            urllib.urlretrieve (url, filename)
            
            filesize = os.path.getsize(filepath)
            if filesize > 2000:
                with zipfile.ZipFile(filename, "r") as z:
                    z.extractall('C:\\Users\\Scott\\Documents\\Python codes\\pyforex\\')
                filepathtxt = filepath[:-3] + 'txt'
                new_filepath = filedest + 'fxday' + str(day) + '.txt'
                day +=1
                os.rename(filepathtxt,new_filepath)            
            os.remove(filepath)
                