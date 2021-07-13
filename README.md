# craigslist-scraper
General scraper for checking for new listings.
Searches and places results in a csv file, updating the file and notifying you if any of the top 5 entries have changed.
Results are returned in ascending order based on listing price.
May include commented out code to send a notifying email with new csv file in the event of a results change. Useful for regular execution with cron.

Usage is as follows:
"craigScrape.py <location> <query> <maxprice> <numproducts>"

Where location is a craigslist city option (ie "sacramento"), query is the search (ie "bicycle wheels"), maxprice is the highest price that will be included in the search, numproducts is the max number of items shown in your search.
