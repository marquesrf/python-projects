import requests
import lxml.html

# Open the web page
html = requests.get('https://store.steampowered.com/explore/new/')

# Pass the request's response to lxml.html.formstring so it can provide an object of HtmlElement type.
# This object has the 'xpath' method to be used to query the HTML document.
doc = lxml.html.fromstring(html.content)

#
# This statement uses xpath to return a list of all the 'divs' which have an id of 'tab_newreleases_content'.
# Since we know that there is only one div on this page with this id, we can take out the first element from the list([0]).
# Explaining the statement:
# '//' - these double forward slashes tell lxml to search for ALL tags which match our requirements/filter. If we have used
# '/' instead, only the immediate child tag that match our requirements/filter would be returned;
# 'div' - tell lxml to search for div tags;
# '[@id="tab_newreleases_content"] - tells lxml that we are only interested in those divs with 'tab_newreleases_content' as id. This is our filter;
#
new_releases = doc.xpath('//div[@id="tab_newreleases_content"]')[0]

#
# This statement uses xpath to return a list with the titles values
# Explaining the statement:
# '.' - tells lxml that we are only interested in tags which are children of the 'new_releases' tag;
# 'div' - tell lxml to search for div tags;
# '[@class="tab_item_name"]' - Similar to the id filter. In this case, we filter by class name;
# '/text()' - tells lxml that we want the text contained within the tag;
#
# The same explanation applies to the next statement
#
titles = new_releases.xpath('.//div[@class="tab_item_name"]/text()')
prices = new_releases.xpath('.//div[@class="discount_final_price"]/text()')

#
# This loop goes through the list if the tags for each title and return only
# the text contained within the tag. Then, it appends it to the 'tags' array;
# Finally, we separate the tags in a list, so each tag is a separate element.
#
tags = []
for tag in new_releases.xpath('.//div[@class="tab_item_top_tags"]'):
    tags.append(tag.text_content())

tags = [tag.split(', ') for tag in tags]

#
# The platforms names are not contained as text within a tag, they are part
# of the class name, as the second class name.
# So we loop through then, filter the first class name (common to all),
# discard it and get the second class name, that is the platform.
#
platforms_div = new_releases.xpath('.//div[@class="tab_item_details"]')
total_platforms = []

for game in platforms_div:
    temp = game.xpath('.//span[contains(@class, "platform_img")]')
    platforms = [t.get('class').split(' ')[-1] for t in temp]
    if 'hmd_separator' in platforms:
        platforms.remove('hmd_separator')
    total_platforms.append(platforms)

#
# This loop puts everything together:
# We use the 'zip' function to iterate over all the lists in parallel;
# Then we create a dictionary for to represent each game info;
# We append the the dictionary to the 'output' list;
# Finally, we return(print) the list to the user;
#
output = []
for info in zip(titles, prices, tags, total_platforms):
    resp = {}
    resp['title'] = info[0]
    resp['price'] = info[1] if info[1] else "N/A"
    resp['tags'] = info[2]
    resp['platforms'] = info[3]
    output.append(resp)

print(output)
