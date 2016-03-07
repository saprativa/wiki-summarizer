			############################## Wikipedia summarizer ###########################
			#                                                                             #
			###############################################################################

import sys
import requests 
from bs4 import BeautifulSoup

#Function to display items of a list
def display_list(a_list):
	#para_count =5 
	for element in a_list:
		print element
		#para_count -= 1
		#if para_count >= 0:
		#	break


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

#Check for disambiguation page
def disambiguation(soup):
	#print type(soup)
	catlinks = soup.find('div',id='catlinks')	#<div id='mw-normal-catlinks'....> will contain the 'Category: Disambiguation pages'
	#print type(catlinks)
	for cats in catlinks.contents:
		if cats.find('a',title='Category:Disambiguation pages') == None:	#No diambiguation page
			continue
		else:	#Disambiguation page
			return True
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

#Function to extract the first paragraph.
def extract_first_para(soup):
	body = soup.body	#Portion of interest : 'body'
	div1 = body.find('div',id='mw-content-text')
	paras = []	#A list to store each paragraph before the table of contents
	#Search and extract begins
	for c in div1.contents:
		if c.name is None:	#Directly skip
			#print 'check 1'
			continue
		if c.name == 'div':	# <div id='toc'>
			#print 'check 2'
			if c.has_attr('id')==True:
				#print 'check 3'
				if c['id']=="toc":	#Reaching here means we have extracted all paras above the contents table
					#print 'check 4'
					break
		elif c.name == 'p':	#Paragraph zone
			#print 'check 5'
			remove_citations(c)
			paras.append(c.text)			
		else:
			#print 'check 7'
			continue	
	del c

	#print para[1]
	#for c in para:
	#	print c,'*********************************************'
	
	return paras	#List that contains all the extracted paragraphs
#Remove citations from the provided tag
def remove_citations(_tag_):
	for sups in _tag_.contents:	#Inside the current paragraph
		if sups.name in ('sup','img'):	#If 'sup' tag found
			sups.replaceWith('')	#Remove it
	


				############################### Program begins here ##################################
#Display greetings!
for i in range(0,25):
	sys.stdout.write('#')
sys.stdout.write(' WELCOME TO WIKI-SUMMERIZER ')
for i in range(0,25):
	sys.stdout.write('#')
print
sys.stdout.write('#')
for i in range(0,50+len(' WELCOME TO WIKI-SUMMERIZER ')-2):
	sys.stdout.write(' ')
print '#'
for i in range(0,50+len(' WELCOME TO WIKI-SUMMERIZER ')):
	sys.stdout.write('#')

#Start here
print
while True:
	print
	#Asking the user for search keyword
	try:
		keyword = raw_input('Search Wikipedia for: ')
	except EOFError:	#Non-string or ENTER was input
		print '---- You did not enter anything ----'
		print '---- Please retry ----'
		continue
	except KeyboardInterrupt:	#CTRL+C was pressed
		print '---- BYE ----'
		exit()

	#Prefix is the common url part. '/Special:Search/' is used because this links
	#redirects to the correct page(for any article) even if the case is wrong.
	prefix = 'https://en.wikipedia.org/wiki/Special:Search' 

	#Making the complete url prefix + keyword
	url = prefix + '/' + keyword.strip().replace(' ', '_')

	#Printing the url
	print 'Generated URL: ' + url

	print 'Retrieving article...'
	#print 'Analyzing article...'

	#Find the appropriate article. There may disambiguation pages. This means some terminologies may refer to more than one meaning
	while True:
		#Saving the contents of the http response into page
		page = requests.get(url).content
		#Making the soup with html.parser
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
	
	#Printing the title of the wikipedia article
	print '\t***',soup.h1.string,'***'

	#Printing the first paragraph of the article
	#print soup.p.get_text()


	#Calling print_infobox_table
	print_infobox_table(soup.find('table', class_='infobox'))

	print '----------------------------------------------------------'
	#Extract and print first para
	para_list = extract_first_para(soup)
	display_list(para_list)
	for i in range(0,50):
		sys.stdout.write('#')

