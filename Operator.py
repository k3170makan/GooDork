#!/usr/bin/python
import re
import sys
import urlparse
from bs4 import BeautifulSoup as soup
import sre_constants
import netlib
import URLStripper
import Result
"""Some changes,
	*I'm coding while watching reruns of the Office Season 6 lols
	*Operator Works in Result objects now
"""
class Operator:
	"""
		Operator: the object that does all of dorks dirty work for it
			*applies URLStripper calls
			*applies all the neccesary netlib calls
			*performs the dorks
				>inurl,intext....
			and returns them to Dork, where all the boolean logic will be performed
	"""
	def __init__(self):
		self.netlib = netlib.netlib("Internet Explorer 6.0")
		self.stripper = URLStripper.URLStripper()
		self.ResList = dict() #a results list to keep the final list
	"""Get the HTML of the page from the supplied url
		url --- the Resource locator of the page

		returns a single str containing the HTML
	"""
	def setUserAgent(self,UA): #set the user-agent header for all page requests
		self.netlib = netlib.netlib(UA)
	def setTimeOut(self,timeout): #set the time_out for net requests
		self.netlib.set_timeOut(timeout)
	def setGoogleResLimit(self,limit): #set the maximum result limit
		self.netlib.set_googleResLimit(limit)
	def getHTML(self,url):
		page = self.netlib.getPage(url)
	#	print page[1]
		if page[0] == False:
			sys.stderr.write("Problem fetching page...[%s]" % (url))
			return False
	"""Google Search the given query

		returns the links that google replied with corresponding to the query
	"""
	def goosearch(self,start,query):
		page = self.netlib.googleSearch(start,query)
		if page[0] == False:
			sys.stderr.write("Problem fetching page...[%s]" % (query))
			return False
		links = self.stripper.strip(page[1])
		return links
	def buildResults(self,links): #builds a list of resutls, prevents redundant calls to servers
		#simply gets the HTML for the page, and appends it to a results list
		#I could have bs4 implemented in the Result obj, but i feel its not neccessary now
		if self.ResList or len(self.ResList) == 0:
			for link in links:
				HTML = self.getHTML(link) #I must remeber to add the response headers to the result object
				res = Result.Result(link,[],"",[],HTML) #i know its a lil redundant to have the link in the Result object aswell
				#but I intend ot use this object as an easy way to dump info to a database/XML file later
				self.ResList[link] = res #add this to the results dictionary
				#print self.ResList[link].HTML
				#I decided on a dictionary because its easier for GooDork to work with
	"""Search the displayable text of a page for a given regex pattern
			pattern
		url --- the Resource locator of the page
		pattern  --- the regex pattern to apply

		returns True if the regex form appears in the page
		returns False if it does not
	"""
	def _intext(self,pattern,url):
		hasPat = False
		try:
			res = self.Res_list[url]
		except KeyError:
			return False #the url does not exist in the dictionary
		for string in soup(res.HTML):
			if re.search(pattern,HTML) != None:
				res.Summary += "*\n".join(re.match(pattern,res.HTML))
				hasPat = True
		return hasPat
	def intext(self,pattern,url):
		print "Searching in text of %s for %s" % (url,pattern)
		#html = self.getHTML(url) #this is the kind of thing I want to prevent
		html = self.ResList[url].HTML
		if html == False or html == "":
			return html
		#now we search the text of the page
		try:
			for string in soup(html).strings:
				#print string
				if re.search(pattern,string) != None:
					return True
		except: #this happend when the file is not HTML!, I'm gonna fix this later , so you can search SQL/XML files aswell
			return re.search(pattern,html) != None #there i fix!!
		return False
	"""Search the url supplied for the given regex pattern
		url		 --- the Resource locator to search
		pattern   --- the regex pattern to apply

		returns True if the pattern does appear in the url supplied
		returns False if not
	"""
	def _inurl(self,pattern,url): #the new methods, implimenting the Result object
		try:
			res = self.Res_list[url]
		except KeyError:
			return False
		hasPat=(re.search(pattern,res.URL) != None)
		if hasPat:
			res.Summary += '*\n'.join(re.match(pattern,res.URL))
		return hasPat
	def inurl(self,pattern,url):
		 #i should let them just use regex!, need to read up on python regex
		#print "re.search(%s,%s)" % (pattern,url)
		try:
			res = re.search(pattern,url)
		except sre_constants.error,e:
			print "Problem with your regex pattern < %s >" % (pattern)
			sys.exit()
		#print res
		return res != None
	"""Search the title tag of a page for the given regex pattern
		url --- the Resource locator (URL) to the page
		pattern --- the regex pattern to apply

		returns True if the regex does appear in the title of the page
		returns False if it does not
	"""
	def _intitle(self,pattern,url):
		try:
			res = self.Res_list[url]
		except KeyError:
			return False
		hasPat=(re.search(pattern,res.title) != None)
		if hasPat:
			res.Summary += '*\n'.join(re.split(pattern,res.title))
		return hasPat
	def intitle(self,pattern,
					url):
		html = self.ResList[url].HTML
		try:
			title = soup(html).title
		except:
			return False
		return re.search(pattern,title.string) != None
	def _inanchor(self,pattern,
					url):
		try:
			res = self.Res_list[url]
		except KeyError:
			return False
		hasPat=False
		for anchor in (res.HTML).findAll("a"):
			href = anchor.get("href")
			if re.search(pattern,href) != None:
				res.Summary += "*\n".join(re.match(pattern,href))
				hasPat=True
		return hasPat
	def inanchor(self,pattern,
					 url):
		isFound = False
		html = self.ResList[url].HTML
		if html == False:
			return html
		try:
			anchors = soup(html).findAll("a")
			for anchor in anchors:
				href = anchor.get("href")
				if self.inurl(pattern,href):
					isFound=True
		except:
			return isFound
		return isFound
	def inscript(self,pattern,
						url):
		html = self.ResList[url].HTML	
		if html == False:
			return html
		try:
			script_tags = soup(html).findAll("script")
			for tag in script_tags:
				if re.search(pattern,str(tag.contents)):
					return True
		except Exception, e:
			print e
	"""This has yet to be implemented
		I hope to be able to have users supply a dork and return have Operator return all the URLs 'related' to the urls from the dork query
		e.g
			dork .php?*wp-content*=* -related
		will return all the URLS that are related to the results returned from the dork
	"""
	def related(self): #this is gonna take a lil thought to apply properly, will be quite powerful!
		return
	"""This has yet to be implemented
		This will apply the regex pattern to the domain of the given url string
	"""
	def site(self,url,
				pattern):
		return
	#def cache(self):
	#	return
	"""Search the <input> tags of a page for the supplied regex pattern 
		in the vales of the supplied attribute
		e.g
		 "	ininput(example.com,type,hidden) " will return True if the are input tags 
			where the attribute type is set to hidden i.e <input type=hidden>
		 "	-ininput [\w]=[\d] " will return True if there are any input tags
			where any attributes set to integer data  i.e <input abcdefgh123456709=1>

		url --- the Resource locator to the page
		attr --- the name of the attribute
		pattern --- the regex pattern to be applied
		
		returns True if the pattern does appear in the value of the attribute of the input tags
		returns False if it does not
	"""
	def ininput(self,url
					,attr,pattern):
		return
	"""the same as above but applied to the <form> tag
	"""
	def inform(self,url,
				  attr,pattern):
		return
	"""the same as above but applied to the <img> tag
	
	*PROTIP: this will help you find sites that have been XSSed
	"""
	def inimg(self,url,
				 attr,pattern):
		return
	"""Search the contents of the script tags on a page for the supplied pattern
		url --- the Resouce locator of the page
		pattern -- the regex to be applied to the tag
	Returns True if the pattern was found the contents of the script tag
	Returns False if not
	*PROTIP: this will help you find sites that have been XSSed
	"""
	def inscript_tag(self,url,
						  pattern):
		return
	#I used these methods to test the implementations ;)
	def inanchor_(self,html,pattern):
		f = open(html,"r")
		html = f.read()
		anchors = soup(html).findAll("a")
		for anchor in anchors:
			if re.search(pattern,str(anchor.get("href"))) != None:
				print "Found :",anchor
				return True
		return False
	def intext_(self,html,pattern):
		f = open(html,"r")
		html = f.read()
		for string in soup(html).strings:
			if re.search(pattern,string) != None:
				print "Found :",string
				return True
		return False
	def _inscript(self,
				  pattern):

		f = open('Sample2.html',"r")
		html = f.read() 
		if html == False:
			return html
		try:
			script_tags = soup(html).findAll("script")
			for tag in script_tags:
				if re.search(pattern,str(tag.contents)):
					print "Found :",tag		
					return True
		except Exception, e:
			print e
if __name__ == "__main__":
	op = Operator()
	op._inscript(sys.argv[1])
