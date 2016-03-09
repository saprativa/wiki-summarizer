import requests 
from bs4 import BeautifulSoup

#function for checking whether the page exists or not
def page_does_not_exist(soup):
	if soup.find('p', class_='mw-search-nonefound') is not None:
		return True
	else:
		return False

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
				if li.find('ul') is not None:
					li.ul.clear()
                        	i = i+1
                        	print str(i) + '.',
                        	print li.text.strip()
                        	urls.append(li.a['href'])

	while True:
		choice = int(raw_input('\nEnter your choice (1-' + str(len(urls)) + '):'))
		if choice >= 1 and choice <= len(urls):
			break
		else:
			print 'Wrong choice. Please enter a valid choice.'
			continue

	return urls[choice-1]

#function for identifying disambiguation page
def disambiguation(soup):
	if soup.find('table', id = 'disambigbox') is not None:
		return True
	else:
		return False

#function for printing the infobox table
def print_infobox_table(table):
	if table is None:
		return
	remove_citations(table)
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
	print '-' * 80

#function for printing the top paragraphs
def print_top_paragraphs(body):
	div = body.find('div',id='mw-content-text')
	for tag in div.contents:
		if tag.name == 'div':
			if tag.has_attr('id') == True:
				if tag['id'] == "toc":
					break
		elif tag.name == 'p':
			remove_citations(tag)
			print tag.text			

#function for removing citations
def remove_citations(tag):
	citations = tag.select("sup.reference")
	for citation in citations:
		citation.decompose()
	
#program starts here
while True:
	#asking the user for the search keyword
	try:
		keyword = raw_input('Search Wikipedia for: ')
	#if ctrl+c or ctrl+d is pressed
	except EOFError:
		print '---- BYE ----'
		exit()
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

	if(page_does_not_exist(soup)):
		print 'Whoa! You searched for something that even Wikipedia does not know about.'
		print 'Please try again.'
		continue

	if(disambiguation(soup)):
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

	#calling the function for printing the top paragraphs
	print_top_paragraphs(soup.body)
