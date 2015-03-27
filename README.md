*Under construction*
In the future, I will better structure and document my code, but this is functional.

# fxml

This repo contains tools and examples for applying machine learning to trading the Forex market.

## Scraper

*Under construction*

* `scrape_forexite.py` - Scrapes Forex data off of the website forexite.com into 1 text file per day
    * Modify:

        years
		months
		dates
		filedest

* `fxml_forexite.m` - Converts data from text files into MATLAB data files.
    * Must move text files created by `scrape_forexite.py` into MATLAB path
    * Modify:
	
        num_days
