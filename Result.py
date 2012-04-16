#!/usr/bin/python
"""
	TODO: write this as a list type
	A class to manage results, this helps gooDork display results
	in a more effective manner
"""
class Result:
	"""
		URL 			<type 'str'>  --- the URL to the dork result
		anchor_tags <type 'list'> --- a list of the anchor tags from the page
		form_tags 	<type 'list'> --- a list of the form tags on the page
		HTML			<type 'str'>  --- one massive string saving all the HTML serverd from this server
		headers		<type 'list'> --- the list of headers this server responded with
		
		I've 	suggested types for every argument, but the types are interchangable (where 'list' is specified)!
		you use lists everywhere in the arguments if you wish, or just strings
		this makes this object quite flexible, also, generators should work
	"""
	"""This __init__ method is part of the next version
	def __init__(self,URL,
					anchor_tags,
					script_tags,
					form_tags,
					title_tag,
					input_tags,
					style_tags,
					texts):
		self.url = URL
		self.anchor_tags = anchor_tags
		self.script_tags = script_tags
		self.form_tags = form_tags
		self.input_tags = input_tags
		self.style_tags = style_tags
		self.title_tag = title_tag
		self.texts = texts
	"""
	def __init__(self,URL,
					anchor_tags,
					title_tag,texts,
					HTML):
		self.url = URL #URL
		self.anchor_tags = anchor_tags #anchor tags
		self.title_tag = title_tag #title tag
		self.texts = texts #displayable text strings
		self.spaces = 5
		self.mega_list = [self.anchor_tags,self.title_tag,self.texts] # i suspect that i may not need to do this 0_o
		self.HTML = HTML #i think i should start making use of this object now,
		self.headers = []
		self.summary = ""
	"""Retuns a printable string of the whatever the result object is
		param --- an attribute of the parameter, this will either be a string, or a list of strings

		*I do thought expect to start working with generators instead of lists for this method very soon
		since we no longer need to suffer the memory overhead of a list here ;)
	"""
	def setTitle(self,title):
		self.title=title
	def setAnchors(self,anchors):
		self.anchor_tags=anchors
	def addAnchor(self,anchor):
		self.anchor_tags.append(anchors) #I likely wont use this, but its good to be prepared
	def setText(self,text):
		self.texts=text
	def setURL(self,url):
		self.url=URL
	def setHTML(self,HTML):
		self.HTML=HTML
	"""Sets the Summary of the result to be displayed with the result
	"""
	def setSummary(self,summary):
		self.summary=summary

	"""Sets the attribute that saves the response headers of a server query
	"""
	def setHeaders(self,headers):
		self.headers = headers
	"""Returns a screen friendly version of a string
		if a string exceeds 20chars its cut down to string[:20]+"..."
	"""
	def cut_string(self,string):
		#return len(string) >20 ? string[:20]+"...":string 
		#wish it was thtat simple! java memories...
		if len(string)>20:
			return string[:20]+"..."
		return string
	def _printable(self,param):
		print_string = ""
		if type(param) == type([]) or type((i for i in [])): #just a quick hack to make it more flexible
			print_string = ''.join([">"+" "*self.spaces+self.cut_string(res)+"\n" for res in param])
		else:
			print_string = ">"+" "*self.spaces+self.cut_string(param)+"\n"
		return print_string
	def __print__(self): #i was hopping this would be picked up by the print command but its not :/
		print_string="<"+self.url
		if sum([len(i) for i in self.mega_list]) > 0:
			print_string+="\n"
		else:
			print_string+=">"
		for param in self.mega_list:
			print_string+=self._printable(param)
		return print_string+">"
	def getSummary(self):
		return self.Summary
if __name__ == "__main__":
	try: #interesting...need to read more about how python calls objects, could maybe hack something to overload an object
		p = Result(["anchor1","anchor2","anchor3"],"titlasdfasdfasdfasdfasdfadsfasdfe",["a","b","c"])
	except TypeError:
		p = Result("http://wewon.com",["anchor1","anchor2","anchor3"],"titlasdfasdfasdfasdfasdfadsfasdfe",["a","b","c"])
	p.__print__()
