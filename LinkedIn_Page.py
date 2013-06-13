# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib 

def strip_non_ascii(string):
    ''' Returns the string without non ASCII characters'''
    stripped = (c for c in string if 0 < ord(c) < 127)
    return ''.join(stripped)

content = ["Type","Company Size","Website","Industry","Founded"]     
text = '"LinkedInId","Name","Type","Company Size","Website","Industry","Founded","Headquarters", \n '
f = open('companylist_(1-10000).csv', 'a') 
f.write(text) 
for j in range(1006,10000) :
	temp ='';
	sock = urllib.urlopen("http://www.linkedin.com/companies/%s"%(j)) 
	htmlSource =sock.read()            
	sock.close()      
	soup_body = BeautifulSoup(htmlSource)
	htmlSource = str(soup_body.find("div", { "class" : "basic-info" }))
	soup = BeautifulSoup(htmlSource)
	if(soup.text != 'None') :
		tag ={}
		temp = '" %s ",'%(j)
		temp = temp + '"'+ soup_body.h1.text.strip()+'",'
		tag_header = soup.findAll("dt")
		tag_content = soup.findAll("dd")
		for i in range(len(tag_header)) :
			tag[tag_header[i].text.strip()]=tag_content[i].text.strip()
		for i in range(5) :
			if content[i] in tag :
				temp = temp + '"'+tag[content[i]]+'",'
			else :
				temp = temp + '"Not Filled",'
		address = soup_body.find("div", { "class" : "adr" })
		if(address != None) :
			temp = temp+'"'+address.text.strip()+'",'
		else :
			temp = temp + '" Not Filled ",'
		temp = temp +'\n'
		temp= strip_non_ascii(temp)
		f.write(temp) 
	print "Completed %s"%(j)
