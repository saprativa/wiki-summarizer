import sys
import requests 
from bs4 import BeautifulSoup

#Display the list of option for a disambiguation page
def get_specific_link(soup):
	mw = soup.find('div',id='mw-content-text')	#First get the target division
	remove_citations(mw)
	
	l = tuple(mw.contents)	#Make a list of mw's children and then convert it to tuple so that we can index each items(This step may be redundant)
	#Remove items with value u'\n'(i.e. NoneType) from the tuple using filtering technique...coz tuples are immutable
	l = [x for x in l if x != u'\n']	# l is I guess converted to a <type 'list'> now, yielded by the effect of tuple filtering. Not a problem
	
	#Find <ul> tag
	for ul in l:
		if ul == u'ul':
			soup = BeautifulSoup(ul,'html.parser')
			break
		#May require else case in the future.(Unexpected)

	options = tuple(soup.ul.contents)	#Generate options<li> to be displayed
	options = [x for x in options if x != u'\n']

	#Display options as a menu
	while True:
		print
		print "Select any of the options below that you are interested in:"
		for i in range(0,len(options)):
			print str(i+1) + ". " + str(options[i].text)
		#Check for blank input
		try:
			opt = int(raw_input("> "))
			if opt not in range(1,len(options)+1):	#Wrong option
				print '------- Wrong option! Please try again ------'
				print '\tThere are only',len(options),'options available. Please select any one of them.'
				continue
			break
		except ValueError:
			print "------- ?? YOU MAY HAVE PRESSED AN INVALID KEY ?? -------"
			print "\tSELECT ANY ONE OF THE OPTION WITH THEIR SLNO (or)"
			print "\tPRESS CTRL+C TO QUIT"

	return str(options[opt-1].a['href'])	#Returns the link of the target article

#function for identifying disambiguation page
def disambiguation(soup):
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
	prefix = 'https://en.wikipedia.org/wiki/Special:Search' 

	#making the complete url: prefix + keyword
	url = prefix + '/' + keyword.strip().replace(' ', '_')

	#printing the url
	print 'Generated URL: ' + url

	print 'Retrieving article...'

	while True:
		#saving the contents of the http response into page
		page = requests.get(url).content
		#making the soup with html.parser
		soup = BeautifulSoup(page, 'html5lib')

		#print '#Check for disambiguation page'
		if disambiguation(soup) == True:
			print "#Disambiguation found"
			#Get that new specific article's link and regenerate soup object with new content
			prefix = 'https://en.wikipedia.org' 
			specific_link = get_specific_link(soup).replace("#","/")
			if specific_link.find("/wiki") != -1:
				url = prefix + get_specific_link(soup).replace("#","/")
			else:
				url = prefix + "/wiki" + get_specific_link(soup).replace("#","/")
			print "---------" + url
		else:	#Done
			break
	
	#printing the title of the wikipedia article
	print '***',soup.h1.string,'***'

	#calling the function for printing the infobox table
	print_infobox_table(soup.find('table', class_='infobox'))

	print '-' * 80

	#calling the function for printing the top paragraphs
	print_top_paras(soup.body)
