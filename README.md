vertafore-scraper
=================

This is a simple scraper designed to parse very specific data from Sircon.

Ideally, it will take a CSV of search queries (e.g. SSN, last name) and output a CSV of license and appointment info. At present, the script simply takes credentials and a single SSN and last name from the command line.

Setup
-----

This has been tested with Python 2.7.5. The author makes no guarantees that the script will work with other versions of Python. Before running the script, install the prerequisites:

    % pip install -r requirements.txt


Usage
-----
Pass your credentials and search query on the command line:

    % python scrape.py <ACCOUNT-ID> <USERNAME> <PASSWORD> <SSN> <LAST_NAME>
