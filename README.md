# fxml

This repo will contain tools and examples for applying machine learning to currency trading.

## Scraper

* `scrape_forexite.py` - Scrapes 1-minute resolution Forex data off of the website forexite.com 
into 1 text file per day
    * Modify:
        * start and end dates
        * file destination
	* Libraries required:
		* urllib, zipfile

* `format_fxdata.py` - Converts data from text files into .hdf5 data files
	* Modify this script if close, high, and/or low prices are desired.
    * Can visualize EURUSD exchange rate with `plot_fxdata.py`
    * Modify:
        * file path
        * number of days scraped
	* Libraries required:
		* h5py