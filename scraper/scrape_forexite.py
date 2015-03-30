"""Scraper to retrieve historical forex data"""
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

# User-specified range of data to download
start_date = [26, 2, 2011] #date, month, year
end_date = [4, 3, 2011] #date, month, year
filedest = 'C:\\gh\\fxdata\\' # destination directory for the data

# Define variables for looping through each day
years = range(start_date[2],end_date[2]+1)
Y = len(years)
maxM = 13
maxD = 32
day = 0

for y in years:
    year = num2date(y-2000)
    
    # Define which months are of interest for this year
    if Y == 1:
        months = range(start_date[1],end_date[1]+1)
    elif y == min(years):
        months = range(start_date[1],maxM)
    elif y == max(years):
        months = range(1,end_date[1]+1)
    else:
        months = range(1,maxM)
    M = len(months)
    
    for m in months:
        month = num2date(m)

        # Define which days are of interest for this month
        if M == 1:
            dates = range(start_date[0],end_date[0]+1)
        elif m == min(months):
            dates = range(start_date[0],maxD)
        elif m == max(months):
            dates = range(1,end_date[0]+1)
        else:
            dates = range(1,maxD)
            
        for d in dates:
            date = num2date(d)
            
            # Retrieve data from forexite
            # example url, Sep 29 2011: "http://www.forexite.com/free_forex_quotes/2011/09/290911.zip"
            url = 'http://www.forexite.com/free_forex_quotes/' + str(y) + '/' + month + '/' + date + month + year + '.zip'
            filepath = filedest + date + month + year + '.zip'
            urllib.urlretrieve(url, filepath)
            
            # Only create a file if there was forex data for that day
            filesize = os.path.getsize(filepath)
            if filesize > 2000:
                with zipfile.ZipFile(filepath, "r") as z:
                    z.extractall(filedest)
                filepathtxt = filepath[:-3] + 'txt'
                new_filepath = filedest + 'd' + str(day) + '.txt'
                day += 1
                os.rename(filepathtxt,new_filepath)            
            os.remove(filepath)