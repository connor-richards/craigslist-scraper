# craigslist-scraper
General scraper for checking for new listings.
Searches and places results in a csv file, updating the file and notifying you if any of the top 5 entries have changed.
Results are returned in ascending order based on listing price.
May include commented out code to send a notifying email with new csv file in the event of a results change. Useful for regular execution with cron.

Usage is as follows:
"python craigScrape.py \<location\> \<category\> \<query\> \<maxprice\> \<numproducts\>"

Where:
  location is a craigslist city option (ie "sacramento")
  category is the craigslist sectionthat you would like to search in (ie "sporting-goods")
  query is the search; it's best to keep this simple because it scrapes for matching words (ie "bicycle")
  maxprice is the highest price that will be included in the search
  numproducts is the max number of items shown in your search
