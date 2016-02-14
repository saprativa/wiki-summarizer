import requests #for the http requests and its better than urllib2
import bs4
from bs4 import BeautifulSoup

keyword = raw_input('Search Wikipedia for: ')
prefix = 'https://en.wikipedia.org/wiki/'
url = prefix + keyword.strip().replace(' ', '_')
print 'URL: ' + url

print 'Downloading Wikipedia article...'
#saving the contents of the response into page
page = requests.get(url).content

print 'Analyzing article...'
#making the soup with html.parser
soup = BeautifulSoup(page, 'html.parser')

#printing the title of the wikipedia article
#print soup.h1.string

#printing the first paragraph of the article
#print soup.p.get_text()

#printing the infobox vcard table
def print_infobox_table(table):
        rows = table.find_all('tr')
        for row in rows:
                heading = row.find('th')
                if heading is not None:
                        data = row.find('td')
                        print heading.text.strip() + ': ',
                        print data.text.strip().replace('\n', ', ')

#calling print_infobox_table
print_infobox_table(soup.find('table', class_='infobox vcard'))
