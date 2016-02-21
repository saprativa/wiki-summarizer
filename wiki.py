############################## Wikipedia summarizer ###########################
#
#

import requests 
from bs4 import BeautifulSoup

#asking the user for search keyword
keyword = raw_input('Search Wikipedia for: ')

#prefix is the common url part
prefix = 'https://en.wikipedia.org/wiki/'

#making the complete url prefix + keyword
url = prefix + keyword.strip().replace(' ', '_')

#printing the url
print 'URL: ' + url

print 'Downloading Wikipedia article...'
#saving the contents of the http response into page
page = requests.get(url).content

print 'Analyzing article...'
#making the soup with html.parser
soup = BeautifulSoup(page, 'html.parser')

#printing the title of the wikipedia article
print soup.h1.string

#printing the first paragraph of the article
#print soup.p.get_text()

#function for printing the infobox table
def print_infobox_table(table):
	rows = table.find_all('tr')
	for row in rows:
		if row.find('table') is None:
			ths = row.find_all('th')
			tds = row.find_all('td')	
			if len(ths) is not 0:
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
					if i == (len(tds) - 1):
						print td.text.strip().replace('\n', ', ') + '.'
					else:
						print td.text.strip().replace('\n', ', ') + ',',


#Function to extract and display the first paragraph.
def print_first_para(soup):
	body = soup.body	#Portion of interest : 'body'
	div1 = body.find(id='mw-content-text')
	para = []	#A list to store each paragraph before contents table
	stop_f = False	#Flag for stopping the traversing process
	#Search and extract begins
	for c in div1.contents:
		if c.name is None:	#Directly skip
			#print 'check 1'
			continue
		if c.name == 'div':
			#print 'check 2'
			if c.has_attr('id')==True:
				#print 'check 3'
				if c['id']=="toc":
					#print 'check 4'
					break
		elif c.name == 'p':
			#print 'check 5'
			para.append(c.text)
		else:
			#print 'check 6'
			continue	
	del c
	#print para[1]
	for c in para:
		print c,'*********************************************'

#calling print_infobox_table
#print_infobox_table(soup.find('table', class_='infobox'))
print_first_para(soup)
