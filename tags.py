import re
from bs4 import BeautifulSoup
import requests

# specify the URL of the webpage you want to scrape
url = "https://best-hashtags.com/hashtag/" + "bag" + "/"

# send a request to the URL to retrieve the HTML content
response = requests.get(url)

# create a BeautifulSoup object to parse the HTML content
soup = BeautifulSoup(response.content, 'html.parser')

# find all the text content on the page
text = soup.get_text()

# use regular expressions to find all the hashtags in the text
hashtags = re.findall(r'\#\w+', text)

# print the hashtags
print(hashtags[3:7])
