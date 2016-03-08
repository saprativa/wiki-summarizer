import sys
import requests 
from bs4 import BeautifulSoup

#function for getting the disambiguated url
def get_disambiguation_suffix(soup):
	div = soup.find('div', id = 'mw-content-text')

	urls = []

	i = 0

	edits = div.select(".mw-editsection")
	for edit in edits:
        	edit.decompose()

	for tag in div.children:
        	if tag.name == 'h2':
                	if tag.span['id'] == 'See_also':
                        	break
                	else:
                        	print '\n', tag.text
        	elif tag.name == 'h3':
                	print '\n', tag.text
        	elif tag.name == 'p':
                	print '\n', tag.text
        	elif tag.name == 'ul':
                	for li in tag.find_all('li'):
                        	i = i+1
                        	print i,
                        	print li.text
                        	urls.append(li.a['href'])
	choice = int(raw_input('Enter your choice: '))
	return urls[choice-1]
	del urls

#function for identifying disambiguation page
def check_disambiguation(soup):
	if soup.find('table', id = 'disambigbox') is not None:
		return True
	else:
		return False

#function for printing the infobox table
def print_infobox_table(table):
	if table is None:
		return -1
	rows = table.find_all('tr')
	for row in rows:
                if row.find('table') is None:
                        ths = row.find_all('th')
                        tds = row.find_all('td')
                        #if len(ths) is not 0:
                        for i, th in enumerate(ths):
                                #For the Heading part inside the table
                                if (len(ths) is 1) and (len(tds) is 0):
                                        print '::' + th.text.strip() + '::'
                                        continue
                                elif (i == (len(ths) - 1)) and (len(tds) is 0):
                                        print th.text.strip() + ':'
                                elif i == (len(ths) - 1):
                                        print th.text.strip() + ':',
                                else:
                                        print th.text.strip() + ',',
                        for i, td in enumerate(tds):
                                if td.text.strip() == '':
                                        continue
                                if i == (len(tds) - 1):
                                        print td.text.strip().replace('\n', ', ') + '.'
                                else:
                                        print td.text.strip().replace('\n', ', ') + ',',	

	return 0

#function for printing the top paragraphs
def print_top_paras(body):
	div = body.find('div',id='mw-content-text')
	for tag in div.contents:
		if tag.name is None:
			continue
		elif tag.name == 'div':
			if tag.has_attr('id') == True:
				if tag['id'] == "toc":
					break
		elif tag.name == 'p':
			remove_citations(tag)
			print tag.text			
		else:
			continue	
	del tag

#function for removing citations
def remove_citations(_tag_):
	for sups in _tag_.contents:	#Inside the current paragraph
		if sups.name in ('sup','img'):	#If 'sup' tag found
			sups.replaceWith('')	#Remove it

#program starts here
while True:
	#asking the user for the search keyword
	try:
		keyword = raw_input('Search Wikipedia for: ')
	#if non-string or enter is input
	except EOFError:	
		print '---- You did not enter anything ----'
		print '---- Please retry ----'
		continue
	#if ctrl+c is pressed
	except KeyboardInterrupt:
		print '---- BYE ----'
		exit()

	#pefix is the common url part, '/Special:Search/' is used to make keyword case-insensitive
	prefix = 'https://en.wikipedia.org/wiki/Special:Search/' 

	#making the complete url: prefix + keyword
	url = prefix + keyword.strip().replace(' ', '_')

	#printing the url
	print 'Generated URL: ' + url
	print 'Retrieving article...'

	#saving the contents of the http response into page
	page = requests.get(url).content
	#making the soup
	soup = BeautifulSoup(page)

	if check_disambiguation(soup) == True:
		print "Redirecting to the disambiguaion page."
		prefix = 'https://en.wikipedia.org'
		suffix = get_disambiguation_suffix(soup)
		url = prefix + suffix
		print 'Generated URL: ' + url
	        print 'Retrieving article...'
		page = requests.get(url).content
        	soup = BeautifulSoup(page)
	
	#printing the title of the wikipedia article
	print '***',soup.h1.string,'***'

	#calling the function for printing the infobox table
	print_infobox_table(soup.find('table', class_='infobox'))

	print '-' * 80

	#calling the function for printing the top paragraphs
	print_top_paras(soup.body)
