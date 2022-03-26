# Steam web page data scraping

The goal is to grab game data from Steam page, specifically from the "popular new releases" section. The user will be presented 
with the list of games and related info(title, price, tags and platforms) of the section.

## Libraries
- requests: Used to open the URL. Could have used only 'lxml', it's not granted to work well for all web pages;
- lxml: This library powers both of the two more famous and most used python libraries for web scraping, 'BeautifulSoup' and 'Scrapy'. Used here to show the basics of XPaths and how to extract data from HTML documents;